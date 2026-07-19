/**
 * Protocol constants for the character sheet ↔ extension bridge.
 *
 * Shared between the shell (bridge.js) and the character page client
 * (sheet-client.js). Both import this module via ESM.
 *
 * Channel/source namespace: io.github.filipeaguiar.character-sheet
 * This MUST NOT use the external "gm-vault" identifier.
 */

/** Stable source identifier for Dice+ messages and bridge envelopes. */
export const SOURCE = "io.github.filipeaguiar.character-sheet";

/** Protocol version – bump on breaking envelope changes. */
export const PROTOCOL_VERSION = 1;

/**
 * Message types exchanged between the shell and the character iframe.
 * Direction is noted in the comment.
 */
export const MessageType = Object.freeze({
  /** Shell → iframe: Dice+ is ready (or not). */
  DICE_READY: "dice-ready",

  /** Iframe → shell: request a Dice+ roll. */
  ROLL_REQUEST: "roll-request",

  /** Shell → iframe: roll completed successfully. */
  ROLL_RESULT: "roll-result",

  /** Shell → iframe: roll failed or timed out. */
  ROLL_ERROR: "roll-error",
});

/**
 * Dice+ broadcast channels used by the shell.
 */
export const DicePlusChannel = Object.freeze({
  IS_READY: "dice-plus/isReady",
  ROLL_REQUEST: "dice-plus/roll-request",
  ROLL_RESULT: `${SOURCE}/roll-result`,
  ROLL_ERROR: `${SOURCE}/roll-error`,
});

/** Default timeout (ms) waiting for Dice+ readiness response. */
export const READY_TIMEOUT_MS = 3000;

/** Delay before retrying readiness while the character iframe remains open. */
export const READY_RETRY_MS = 1000;

/** Default timeout (ms) waiting for a roll result after request. */
export const ROLL_TIMEOUT_MS = 10000;

/** Maximum allowed length for a dice notation string. */
export const MAX_NOTATION_LENGTH = 64;

/**
 * Regex for validating dice notation. Allows standard patterns like:
 * 1d20+5, 2d6+3, 1d20, +7, -1, 4d8-2, 1d12+1d6+3
 */
export const NOTATION_PATTERN = /^[+\-]?\d*d?\d+([+\-]\d*d?\d+)*$/i;

/**
 * Create a versioned bridge message envelope.
 *
 * @param {string} type - One of MessageType values.
 * @param {object} payload - Message-specific data.
 * @returns {object} Envelope with source, version, type, and payload.
 */
export function createEnvelope(type, payload = {}) {
  return {
    source: SOURCE,
    version: PROTOCOL_VERSION,
    type,
    payload,
  };
}

/**
 * Validate an incoming bridge message envelope.
 *
 * @param {object} data - The parsed message data.
 * @param {string[]} [allowedTypes] - If provided, restrict to these types.
 * @returns {{ valid: boolean, reason?: string }}
 */
export function validateEnvelope(data, allowedTypes) {
  if (!data || typeof data !== "object") {
    return { valid: false, reason: "not an object" };
  }
  if (data.source !== SOURCE) {
    return { valid: false, reason: "wrong source" };
  }
  if (data.version !== PROTOCOL_VERSION) {
    return { valid: false, reason: "unsupported version" };
  }
  if (!data.type || typeof data.type !== "string") {
    return { valid: false, reason: "missing type" };
  }
  if (allowedTypes && !allowedTypes.includes(data.type)) {
    return { valid: false, reason: "unexpected type" };
  }
  return { valid: true };
}

/**
 * Validate a dice notation string.
 *
 * @param {string} notation
 * @returns {{ valid: boolean, reason?: string }}
 */
export function validateNotation(notation) {
  if (typeof notation !== "string") {
    return { valid: false, reason: "notation must be a string" };
  }
  const trimmed = notation.trim();
  if (trimmed.length === 0) {
    return { valid: false, reason: "notation is empty" };
  }
  if (trimmed.length > MAX_NOTATION_LENGTH) {
    return { valid: false, reason: "notation too long" };
  }
  if (!NOTATION_PATTERN.test(trimmed)) {
    return { valid: false, reason: "invalid notation format" };
  }
  return { valid: true };
}

/**
 * Generate a unique ID suitable for requestId / rollId.
 * @returns {string}
 */
export function generateId() {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}
