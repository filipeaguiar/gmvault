/**
 * Dice+ bridge for the Owlbear character sheet extension.
 *
 * Manages the postMessage bridge between the shell and the character
 * iframe, and integrates with the Owlbear Dice+ channels.
 *
 * Lifecycle:
 *   1. Call initBridge(OBR) once after OBR.onReady.
 *   2. Call bindIframe(iframe) after a character iframe loads.
 *   3. Call unbindIframe() before changing character or unloading.
 *   4. Call destroyBridge() on extension close.
 */

import {
  SOURCE,
  PROTOCOL_VERSION,
  MessageType,
  DicePlusChannel,
  READY_TIMEOUT_MS,
  READY_RETRY_MS,
  ROLL_TIMEOUT_MS,
  createEnvelope,
  validateEnvelope,
  validateNotation,
  generateId,
} from "./protocol.js";

// ── Internal state ──────────────────────────────────────────────────

let _obr = null;
let _player = null;
let _iframeWindow = null;
let _expectedOrigin = null;
let _diceReady = false;
let _readyCheckTimer = null;
let _diceReadyUnsub = null;
let _pendingReadyId = null;
let _pendingRolls = new Map(); // rollId → { timerId, iframeWindow, targetOrigin }
let _messageHandler = null;
let _diceResultUnsub = null;
let _diceErrorUnsub = null;
let _onDiceReadyChange = null; // external callback
let _onDiagnostic = null; // external diagnostic callback

// ── Public API ──────────────────────────────────────────────────────

/**
 * Validate and normalize the Owlbear player identity used by Dice+.
 * @returns {{ id: string, name: string } | null}
 */
export function normalizePlayerIdentity(id, name) {
  if (
    typeof id !== "string" || id.trim() === "" ||
    typeof name !== "string" || name.trim() === ""
  ) {
    return null;
  }
  return { id: id.trim(), name: name.trim() };
}

/**
 * Initialize the bridge with the Owlbear SDK instance.
 *
 * @param {object} obr - The OBR SDK instance.
 * @param {object} player - { id, name } from OBR.player.
 * @param {function} [onDiceReadyChange] - Called with (boolean) when
 *   Dice+ readiness changes.
 * @param {function} [onDiagnostic] - Called with a safe diagnostic message.
 */
export function initBridge(obr, player, onDiceReadyChange, onDiagnostic) {
  _obr = obr;
  _player = player;
  _onDiceReadyChange = onDiceReadyChange || null;
  _onDiagnostic = onDiagnostic || null;
  _diagnose("Ponte Dice+ inicializada.");

  // Subscribe to Dice+ result and error channels (once, for all rolls).
  _diceResultUnsub = _obr.broadcast.onMessage(
    DicePlusChannel.ROLL_RESULT,
    _handleDiceResult
  );
  _diceErrorUnsub = _obr.broadcast.onMessage(
    DicePlusChannel.ROLL_ERROR,
    _handleDiceError
  );
}

/**
 * Bind the bridge to a specific character iframe.
 * Unbinds any previous iframe first.
 *
 * @param {HTMLIFrameElement} iframe - The character iframe element.
 */
export function bindIframe(iframe) {
  unbindIframe();

  _iframeWindow = iframe.contentWindow;
  _expectedOrigin = new URL(iframe.src).origin;
  _diagnose(`Ficha vinculada; origem: ${_expectedOrigin}.`);

  // Listen for messages from the iframe.
  _messageHandler = (event) => _handleIframeMessage(event);
  window.addEventListener("message", _messageHandler);

  // Check Dice+ readiness for this binding.
  _checkDiceReady();
}

/**
 * Unbind from the current iframe. Clears listeners, pending rolls,
 * and timers associated with the iframe.
 */
export function unbindIframe() {
  if (_messageHandler) {
    window.removeEventListener("message", _messageHandler);
    _messageHandler = null;
  }

  // Clear readiness check.
  if (_readyCheckTimer) {
    clearTimeout(_readyCheckTimer);
    _readyCheckTimer = null;
  }
  if (_diceReadyUnsub) {
    _diceReadyUnsub();
    _diceReadyUnsub = null;
  }
  _pendingReadyId = null;

  // Clear all pending rolls.
  for (const [, entry] of _pendingRolls) {
    clearTimeout(entry.timerId);
  }
  _pendingRolls.clear();
  _diagnose("Pendências de rolagem descartadas durante unbind.");

  _iframeWindow = null;
  _expectedOrigin = null;
  _diceReady = false;
}

/**
 * Destroy the bridge entirely. Call on extension unload.
 */
export function destroyBridge() {
  unbindIframe();

  if (_diceResultUnsub) {
    _diceResultUnsub();
    _diceResultUnsub = null;
  }
  if (_diceErrorUnsub) {
    _diceErrorUnsub();
    _diceErrorUnsub = null;
  }

  _obr = null;
  _player = null;
  _onDiceReadyChange = null;
  _onDiagnostic = null;
}

/**
 * Whether Dice+ is currently available.
 * @returns {boolean}
 */
export function isDiceReady() {
  return _diceReady;
}

// ── Dice+ readiness ─────────────────────────────────────────────────

function _checkDiceReady() {
  if (!_obr) return;

  _pendingReadyId = generateId();
  const requestPayload = {
    requestId: _pendingReadyId,
    timestamp: Date.now(),
  };

  // Subscribe before sending so a fast Dice+ response cannot win the race.
  if (_diceReadyUnsub) _diceReadyUnsub();
  _diceReadyUnsub = _obr.broadcast.onMessage(
    DicePlusChannel.IS_READY,
    (event) => {
      const message = event?.data;
      if (!message || message.requestId !== _pendingReadyId) return;

      // Owlbear broadcasts the request back to subscribers. It has no
      // ready:true field and must not be interpreted as a Dice+ response.
      if (message.ready !== true) return;

      _diagnose("Dice+ respondeu que está disponível.");
      _pendingReadyId = null;
      _setDiceReady(true);
      if (_diceReadyUnsub) {
        _diceReadyUnsub();
        _diceReadyUnsub = null;
      }
      if (_readyCheckTimer) {
        clearTimeout(_readyCheckTimer);
        _readyCheckTimer = null;
      }
    }
  );

  _diagnose("Verificando disponibilidade do Dice+.");
  _obr.broadcast.sendMessage(
    DicePlusChannel.IS_READY,
    requestPayload,
    { destination: "ALL" }
  ).catch(() => {
    _diagnose("Não foi possível enviar a verificação ao Dice+; tentando novamente.");
    _retryDiceReadyCheck(requestPayload.requestId);
  });

  // Dice+ can finish loading after this extension, particularly on mobile
  // Chromium. Keep probing while this iframe is active instead of treating a
  // single early timeout as a permanent absence.
  _readyCheckTimer = setTimeout(() => {
    _retryDiceReadyCheck(requestPayload.requestId);
  }, READY_TIMEOUT_MS);
}

function _retryDiceReadyCheck(requestId) {
  // A later request may already be active, or the iframe may have changed.
  if (!_iframeWindow || _pendingReadyId !== requestId) return;

  if (_diceReadyUnsub) {
    _diceReadyUnsub();
    _diceReadyUnsub = null;
  }
  if (_readyCheckTimer) {
    clearTimeout(_readyCheckTimer);
    _readyCheckTimer = null;
  }
  _pendingReadyId = null;
  _diagnose("Dice+ não respondeu; nova tentativa em breve.");
  _setDiceReady(false);

  _readyCheckTimer = setTimeout(() => {
    _readyCheckTimer = null;
    if (_iframeWindow && !_diceReady) _checkDiceReady();
  }, READY_RETRY_MS);
}

function _setDiceReady(ready) {
  _diceReady = ready;
  _diagnose(ready ? "Estado Dice+: conectado." : "Estado Dice+: desconectado.");

  // Notify the iframe.
  if (_iframeWindow && _expectedOrigin) {
    _iframeWindow.postMessage(
      createEnvelope(MessageType.DICE_READY, { ready }),
      _expectedOrigin
    );
  }

  // Notify external callback.
  if (_onDiceReadyChange) {
    _onDiceReadyChange(ready);
  }
}

function _diagnose(message) {
  if (_onDiagnostic) _onDiagnostic(message);
}

// ── Iframe message handling ─────────────────────────────────────────

function _handleIframeMessage(event) {
  // 3.3: Validate event.source matches the active iframe window.
  if (event.source !== _iframeWindow) return;

  // 3.3: Validate origin matches the expected character page origin.
  if (event.origin !== _expectedOrigin) return;

  const data = event.data;

  // 3.3: Validate envelope structure, version, and source.
  const validation = validateEnvelope(data, [MessageType.ROLL_REQUEST]);
  if (!validation.valid) return;

  // Handle roll request from the iframe.
  if (data.type === MessageType.ROLL_REQUEST) {
    _handleRollRequest(data.payload);
  }
}

// ── Roll request handling ───────────────────────────────────────────

function _handleRollRequest(payload) {
  if (!_diceReady || !_obr || !_player) {
    _sendToIframe(MessageType.ROLL_ERROR, {
      requestId: payload.requestId,
      rollId: null,
      error: "Dice+ not available",
      retryable: false,
    });
    return;
  }

  const playerIdentity = normalizePlayerIdentity(_player.id, _player.name);
  if (!playerIdentity) {
    _sendToIframe(MessageType.ROLL_ERROR, {
      requestId: payload.requestId,
      rollId: null,
      error: "Owlbear player identity unavailable",
      retryable: false,
    });
    return;
  }

  // 3.3: Validate notation.
  const notationCheck = validateNotation(payload.notation);
  if (!notationCheck.valid) {
    _sendToIframe(MessageType.ROLL_ERROR, {
      requestId: payload.requestId,
      rollId: null,
      error: `Invalid notation: ${notationCheck.reason}`,
      retryable: false,
    });
    return;
  }

  // 3.5: Build the Dice+ roll request.
  const rollId = generateId();
  const rollRequest = {
    rollId,
    source: SOURCE,
    playerName: playerIdentity.name,
    playerId: playerIdentity.id,
    rollTarget: "everyone",
    diceNotation: payload.notation.trim(),
    showResults: true,
    timestamp: Date.now(),
  };

  // Set up timeout for this roll.
  const timerId = setTimeout(() => {
    _pendingRolls.delete(rollId);
    _sendToIframe(MessageType.ROLL_ERROR, {
      requestId: payload.requestId,
      rollId,
      error: "Roll timed out",
      retryable: true,
    });
  }, ROLL_TIMEOUT_MS);

  // Track the pending roll.
  _pendingRolls.set(rollId, {
    timerId,
    requestId: payload.requestId,
    iframeWindow: _iframeWindow,
    targetOrigin: _expectedOrigin,
  });

  // 3.5: Send to Dice+.
  _obr.broadcast.sendMessage(
    DicePlusChannel.ROLL_REQUEST,
    rollRequest,
    { destination: "ALL" }
  ).catch((error) => {
    const pending = _pendingRolls.get(rollId);
    if (!pending) return;
    clearTimeout(pending.timerId);
    _pendingRolls.delete(rollId);
    _sendToIframe(MessageType.ROLL_ERROR, {
      requestId: pending.requestId,
      rollId,
      error: error instanceof Error ? error.message : "Unable to send roll",
      retryable: true,
    });
  });
}

// ── Dice+ result/error handlers ─────────────────────────────────────

function _handleDiceResult(event) {
  const message = event?.data;
  const rollId = message?.rollId;
  const result = message?.result;
  if (!rollId || !result) return;

  const pending = _pendingRolls.get(rollId);
  if (!pending) {
    _diagnose(`Resultado órfão ignorado: ${rollId}.`);
    return; // Unknown or already completed rollId.
  }

  clearTimeout(pending.timerId);
  _pendingRolls.delete(rollId);

  // 3.6: Send result only to the iframe that made the request.
  if (pending.iframeWindow && pending.targetOrigin) {
    const resultEnvelope = createEnvelope(MessageType.ROLL_RESULT, {
      requestId: pending.requestId,
      rollId,
      total: result.totalValue,
      summary: result.rollSummary,
      groups: Array.isArray(result.groups) ? result.groups : [],
    });
    pending.iframeWindow.postMessage(resultEnvelope, pending.targetOrigin);
  }
}

function _handleDiceError(event) {
  const message = event?.data;
  const rollId = message?.rollId;
  if (!rollId) return;

  const pending = _pendingRolls.get(rollId);
  if (!pending) {
    _diagnose(`Erro órfão ignorado: ${rollId}.`);
    return; // Unknown or already completed rollId.
  }

  clearTimeout(pending.timerId);
  _pendingRolls.delete(rollId);

  // 3.6: Send error to the originating iframe.
  if (pending.iframeWindow && pending.targetOrigin) {
    const errorEnvelope = createEnvelope(MessageType.ROLL_ERROR, {
      requestId: pending.requestId,
      rollId,
      error: message.error || "Unknown Dice+ error",
      retryable: true,
    });
    pending.iframeWindow.postMessage(errorEnvelope, pending.targetOrigin);
  }
}

// ── Helpers ─────────────────────────────────────────────────────────

function _sendToIframe(type, payload) {
  if (_iframeWindow && _expectedOrigin) {
    _iframeWindow.postMessage(createEnvelope(type, payload), _expectedOrigin);
  }
}
