const PROTOCOL_VERSION = 1;
const CHANNEL = "gm-vault/dice";
const DEFAULT_TIMEOUT_MS = 15000;
const DEFAULT_READY_TIMEOUT_MS = 1000;
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

function getDefaultTargetOrigin(windowRef) {
  if (windowRef && windowRef.location && windowRef.location.origin !== "null") {
    const configured = windowRef.GMVaultDiceConfig?.targetOrigin;
    if (configured) return configured;
    try {
      if (windowRef.document?.referrer) {
        return new URL(windowRef.document.referrer).origin;
      }
      return null;
    } catch {
      return null;
    }
  }
  return null;
}

function isValidTargetOrigin(targetOrigin) {
  if (!targetOrigin || targetOrigin === "*") return false;
  try {
    return new URL(targetOrigin).origin === targetOrigin;
  } catch {
    return false;
  }
}

function isValidDiceNotation(value) {
  return typeof value === "string" && DICE_NOTATION_PATTERN.test(value.trim());
}

function isValidRollTarget(value) {
  return ROLL_TARGETS.has(value);
}

function isValidEnvelope(data, type) {
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

function createDicePlusClient(options = {}) {
  const windowRef = options.windowRef || (typeof window !== "undefined" ? window : null);
  const parentWindow = options.parentWindow || windowRef?.parent;
  const targetOrigin = options.targetOrigin || getDefaultTargetOrigin(windowRef);
  const timeoutMs = options.timeoutMs || DEFAULT_TIMEOUT_MS;
  const readyTimeoutMs = options.readyTimeoutMs || DEFAULT_READY_TIMEOUT_MS;
  const pending = new Map();
  const listeners = new Set();
  let destroyed = false;

  const canCommunicate = Boolean(
    windowRef &&
      parentWindow &&
      parentWindow !== windowRef &&
      isValidTargetOrigin(targetOrigin),
  );

  function rejectPending(error) {
    for (const entry of pending.values()) {
      clearTimeout(entry.timer);
      entry.reject(error);
    }
    pending.clear();
  }

  function handleMessage(event) {
    if (destroyed || !canCommunicate) return;
    if (event.source !== parentWindow || event.origin !== targetOrigin) return;

    const data = event.data;
    if (!data || data.channel !== CHANNEL || data.version !== PROTOCOL_VERSION) return;

    if (data.type === MESSAGE_TYPES.AVAILABILITY_RESPONSE) {
      if (!isValidEnvelope(data, MESSAGE_TYPES.AVAILABILITY_RESPONSE)) return;
      const entry = pending.get(data.requestId);
      if (!entry || entry.kind !== "availability") return;
      pending.delete(data.requestId);
      clearTimeout(entry.timer);
      entry.resolve(data.ready === true);
      return;
    }

    if (data.type !== MESSAGE_TYPES.ROLL_RESULT && data.type !== MESSAGE_TYPES.ROLL_ERROR) return;
    if (!isValidEnvelope(data, data.type)) return;
    if (data.type === MESSAGE_TYPES.ROLL_RESULT && typeof data.rollId !== "string") return;
    if (data.rollId !== undefined && data.rollId !== null && typeof data.rollId !== "string") return;

    const entry = pending.get(data.requestId);
    if (!entry || entry.kind !== "roll") return;
    if (typeof data.rollId === "string" && entry.rollId !== data.rollId) return;
    pending.delete(data.requestId);
    clearTimeout(entry.timer);

    if (data.type === MESSAGE_TYPES.ROLL_RESULT) {
      entry.resolve({ rollId: data.rollId, result: data.result });
    } else {
      const error = new Error(typeof data.error === "string" ? data.error : "Dice+ retornou um erro.");
      error.code = "DICE_PLUS_ERROR";
      error.rollId = data.rollId;
      entry.reject(error);
    }

    for (const listener of listeners) listener(data);
  }

  function request(type, payload, kind, timeoutMsForRequest) {
    if (destroyed) return Promise.reject(new Error("A ponte de dados foi destruída."));
    if (!canCommunicate) return Promise.reject(new Error("A ponte gm-vault não está disponível."));

    const requestId = createId("request");
    const envelope = { channel: CHANNEL, version: PROTOCOL_VERSION, type, requestId, ...payload };

    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        pending.delete(requestId);
        reject(new Error("A ponte gm-vault não respondeu dentro do prazo."));
      }, timeoutMsForRequest);
      pending.set(requestId, { kind, rollId: payload.rollId, resolve, reject, timer });
      parentWindow.postMessage(envelope, targetOrigin);
    });
  }

  function checkAvailability() {
    return request(
      MESSAGE_TYPES.AVAILABILITY_REQUEST,
      { timestamp: Date.now() },
      "availability",
      readyTimeoutMs,
    ).catch(() => false);
  }

  function requestRoll(requestData) {
    if (!requestData || !isValidDiceNotation(requestData.diceNotation)) {
      return Promise.reject(new Error("A notação de dados não é válida."));
    }
    const rollTarget = requestData.rollTarget || "everyone";
    if (!isValidRollTarget(rollTarget)) {
      return Promise.reject(new Error("O destino da rolagem não é válido."));
    }

    const rollId = requestData.rollId || createId("roll");
    return request(
      MESSAGE_TYPES.ROLL_REQUEST,
      {
        rollId,
        request: {
          diceNotation: requestData.diceNotation.trim(),
          rollTarget,
          showResults: requestData.showResults !== false,
          label: typeof requestData.label === "string" ? requestData.label.slice(0, 120) : undefined,
        },
      },
      "roll",
      timeoutMs,
    );
  }

  function subscribe(listener) {
    if (typeof listener !== "function") return () => {};
    listeners.add(listener);
    return () => listeners.delete(listener);
  }

  function destroy() {
    if (destroyed) return;
    destroyed = true;
    windowRef?.removeEventListener("message", handleMessage);
    rejectPending(new Error("A ponte de dados foi destruída."));
    listeners.clear();
  }

  if (canCommunicate) windowRef.addEventListener("message", handleMessage);

  return Object.freeze({
    available: canCommunicate,
    checkAvailability,
    requestRoll,
    subscribe,
    destroy,
  });
}

const api = Object.freeze({
  CHANNEL,
  MESSAGE_TYPES,
  PROTOCOL_VERSION,
  ROLL_TARGETS,
  createDicePlusClient,
  isValidDiceNotation,
  isValidRollTarget,
});

if (typeof window !== "undefined") window.GMVaultDice = api;

export {
  CHANNEL,
  MESSAGE_TYPES,
  PROTOCOL_VERSION,
  ROLL_TARGETS,
  createDicePlusClient,
  isValidDiceNotation,
  isValidRollTarget,
};
