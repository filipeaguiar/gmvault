const PROTOCOL_VERSION = 1;
const CHANNEL = "gm-vault/dice";
const DICE_PLUS_READY_CHANNEL = "dice-plus/isReady";
const DICE_PLUS_ROLL_CHANNEL = "dice-plus/roll-request";
const DEFAULT_EXTENSION_ID = "gm-vault";
const DEFAULT_READY_TIMEOUT_MS = 1000;
const DEFAULT_ROLL_TIMEOUT_MS = 15000;
const ROLL_TARGETS = new Set(["everyone", "self", "dm", "gm_only"]);
const MESSAGE_TYPES = Object.freeze({
  AVAILABILITY_REQUEST: "availability-request",
  AVAILABILITY_RESPONSE: "availability-response",
  ROLL_REQUEST: "roll-request",
  ROLL_RESULT: "roll-result",
  ROLL_ERROR: "roll-error",
});
const DICE_NOTATION_PATTERN = /^[0-9dDkKhHlLrRoOxX+\-*/().%{}\[\]#_:, ]{1,200}$/;

function createId(prefix) {
  if (globalThis.crypto && typeof globalThis.crypto.randomUUID === "function") {
    return `${prefix}_${globalThis.crypto.randomUUID()}`;
  }
  return `${prefix}_${Date.now()}_${Math.random().toString(36).slice(2, 11)}`;
}

function validNotation(value) {
  return typeof value === "string" && DICE_NOTATION_PATTERN.test(value.trim());
}

function validOrigin(origin) {
  if (!origin || origin === "*") return false;
  try {
    return new URL(origin).origin === origin;
  } catch {
    return false;
  }
}

function validEnvelope(data, type) {
  return Boolean(
    data &&
      typeof data === "object" &&
      data.channel === CHANNEL &&
      data.version === PROTOCOL_VERSION &&
      data.type === type &&
      typeof data.requestId === "string" &&
      data.requestId.length > 0,
  );
}

function createDicePlusHost(options = {}) {
  const OBR = options.OBR;
  const hostWindow = options.hostWindow || (typeof window !== "undefined" ? window : null);
  const iframeWindow = options.iframeWindow;
  const iframeOrigin = options.iframeOrigin;
  const extensionId = options.extensionId || DEFAULT_EXTENSION_ID;
  const readyTimeoutMs = options.readyTimeoutMs || DEFAULT_READY_TIMEOUT_MS;
  const rollTimeoutMs = options.rollTimeoutMs || DEFAULT_ROLL_TIMEOUT_MS;
  const pendingRolls = new Map();
  let destroyed = false;
  let unsubscribeResult = null;
  let unsubscribeError = null;

  if (!OBR?.broadcast || !OBR?.player) throw new Error("O SDK do Owlbear não foi fornecido.");
  if (!hostWindow || !iframeWindow || !validOrigin(iframeOrigin)) {
    throw new Error("A janela e a origem do iframe precisam ser configuradas.");
  }

  function postToIframe(message, origin = iframeOrigin) {
    if (!destroyed) iframeWindow.postMessage({ channel: CHANNEL, version: PROTOCOL_VERSION, ...message }, origin);
  }

  function isTrustedEvent(event) {
    return event.source === iframeWindow && event.origin === iframeOrigin;
  }

  function removePending(rollId) {
    const entry = pendingRolls.get(rollId);
    if (!entry) return null;
    clearTimeout(entry.timer);
    pendingRolls.delete(rollId);
    return entry;
  }

  function handleResult(event) {
    const data = event.data;
    if (!data || typeof data.rollId !== "string") return;
    const entry = removePending(data.rollId);
    if (!entry) return;
    postToIframe({
      type: MESSAGE_TYPES.ROLL_RESULT,
      requestId: entry.requestId,
      rollId: data.rollId,
      result: data.result,
    });
  }

  function handleError(event) {
    const data = event.data;
    if (!data || typeof data.rollId !== "string") return;
    const entry = removePending(data.rollId);
    if (!entry) return;
    postToIframe({
      type: MESSAGE_TYPES.ROLL_ERROR,
      requestId: entry.requestId,
      rollId: data.rollId,
      error: typeof data.error === "string" ? data.error : "A rolagem falhou.",
    });
  }

  async function checkDicePlusReady() {
    const requestId = createId("ready");
    return new Promise((resolve) => {
      let settled = false;
      const unsubscribe = OBR.broadcast.onMessage(DICE_PLUS_READY_CHANNEL, (event) => {
        const data = event.data;
        if (!data || data.requestId !== requestId || data.ready !== true || settled) return;
        settled = true;
        clearTimeout(timer);
        unsubscribe();
        resolve(true);
      });
      const timer = setTimeout(() => {
        if (settled) return;
        settled = true;
        unsubscribe();
        resolve(false);
      }, readyTimeoutMs);

      OBR.broadcast.sendMessage(
        DICE_PLUS_READY_CHANNEL,
        { requestId, timestamp: Date.now() },
        { destination: "ALL" },
      ).catch(() => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        unsubscribe();
        resolve(false);
      });
    });
  }

  async function getPlayerIdentity() {
    const playerId = await OBR.player.getId();
    const playerName = await OBR.player.getName();
    if (typeof playerId !== "string" || typeof playerName !== "string") {
      throw new Error("Não foi possível identificar o jogador no Owlbear Rodeo.");
    }
    return { playerId, playerName };
  }

  async function handleAvailability(data) {
    const ready = await checkDicePlusReady();
    postToIframe({
      type: MESSAGE_TYPES.AVAILABILITY_RESPONSE,
      requestId: data.requestId,
      ready,
    });
  }

  async function handleRoll(data) {
    if (
      typeof data.requestId !== "string" ||
      !data.request ||
      !validNotation(data.request.diceNotation) ||
      !ROLL_TARGETS.has(data.request.rollTarget || "everyone")
    ) return;

    const ready = await checkDicePlusReady();
    if (!ready) {
      postToIframe({
        type: MESSAGE_TYPES.ROLL_ERROR,
        requestId: data.requestId,
        rollId: null,
        error: "Dice+ não está disponível nesta sala.",
      });
      return;
    }

    const rollId = typeof data.rollId === "string" && data.rollId.length > 0
      ? data.rollId
      : createId("roll");
    let identity;
    try {
      identity = await getPlayerIdentity();
    } catch (error) {
      postToIframe({
        type: MESSAGE_TYPES.ROLL_ERROR,
        requestId: data.requestId,
        rollId,
        error: error instanceof Error ? error.message : "Não foi possível identificar o jogador.",
      });
      return;
    }
    const rollTarget = data.request.rollTarget || "everyone";
    const timer = setTimeout(() => {
      const entry = removePending(rollId);
      if (entry) {
        postToIframe({
          type: MESSAGE_TYPES.ROLL_ERROR,
          requestId: entry.requestId,
          rollId,
          error: "Dice+ não respondeu dentro do prazo.",
        });
      }
    }, rollTimeoutMs);

    pendingRolls.set(rollId, { requestId: data.requestId, timer });
    try {
      await OBR.broadcast.sendMessage(
        DICE_PLUS_ROLL_CHANNEL,
        {
          rollId,
          ...identity,
          rollTarget,
          diceNotation: data.request.diceNotation.trim(),
          showResults: data.request.showResults !== false,
          timestamp: Date.now(),
          source: extensionId,
        },
        { destination: "ALL" },
      );
    } catch (error) {
      const entry = removePending(rollId);
      if (entry) {
        postToIframe({
          type: MESSAGE_TYPES.ROLL_ERROR,
          requestId: entry.requestId,
          rollId,
          error: error instanceof Error ? error.message : "Não foi possível enviar a rolagem.",
        });
      }
    }
  }

  function handleMessage(event) {
    if (destroyed || !isTrustedEvent(event)) return;
    const data = event.data;
    if (!data || data.channel !== CHANNEL || data.version !== PROTOCOL_VERSION) return;

    if (data.type === MESSAGE_TYPES.AVAILABILITY_REQUEST && validEnvelope(data, data.type)) {
      void handleAvailability(data);
    } else if (data.type === MESSAGE_TYPES.ROLL_REQUEST && validEnvelope(data, data.type)) {
      void handleRoll(data);
    }
  }

  function start() {
    hostWindow.addEventListener("message", handleMessage);
    unsubscribeResult = OBR.broadcast.onMessage(`${extensionId}/roll-result`, handleResult);
    unsubscribeError = OBR.broadcast.onMessage(`${extensionId}/roll-error`, handleError);
    return api;
  }

  function destroy() {
    if (destroyed) return;
    destroyed = true;
    hostWindow.removeEventListener("message", handleMessage);
    unsubscribeResult?.();
    unsubscribeError?.();
    for (const entry of pendingRolls.values()) clearTimeout(entry.timer);
    pendingRolls.clear();
  }

  const api = Object.freeze({ start, destroy, checkDicePlusReady });
  return api;
}

const api = Object.freeze({
  CHANNEL,
  DEFAULT_EXTENSION_ID,
  DICE_PLUS_READY_CHANNEL,
  DICE_PLUS_ROLL_CHANNEL,
  MESSAGE_TYPES,
  PROTOCOL_VERSION,
  createDicePlusHost,
});

if (typeof window !== "undefined") window.GMVaultDiceHost = api;

export {
  CHANNEL,
  DEFAULT_EXTENSION_ID,
  DICE_PLUS_READY_CHANNEL,
  DICE_PLUS_ROLL_CHANNEL,
  MESSAGE_TYPES,
  PROTOCOL_VERSION,
  createDicePlusHost,
};
