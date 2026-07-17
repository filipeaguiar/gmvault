/**
 * Character sheet Dice+ client.
 *
 * Runs inside the character iframe (Hugo page). Communicates with the
 * parent extension shell via postMessage using the versioned bridge
 * protocol. Does NOT import the Owlbear SDK.
 *
 * Progressive enhancement flow:
 *   1. On load, send nothing — wait for the parent to notify readiness.
 *   2. On DICE_READY(true), find all [data-roll-notation] elements and
 *      transform them into clickable/keyboard-accessible roll controls.
 *   3. On roll activation, send ROLL_REQUEST to parent and show pending state.
 *   4. On ROLL_RESULT or ROLL_ERROR, return the originating value to ready state.
 *      Dice+ remains responsible for displaying roll results and errors.
 *   5. On unload, clean up listeners and reject pending requests.
 */

(function () {
  "use strict";

  // ── Protocol constants (inlined to avoid cross-origin import issues) ──

  const SOURCE = "io.github.filipeaguiar.character-sheet";
  const PROTOCOL_VERSION = 1;

  const MessageType = Object.freeze({
    DICE_READY: "dice-ready",
    ROLL_REQUEST: "roll-request",
    ROLL_RESULT: "roll-result",
    ROLL_ERROR: "roll-error",
  });

  // ── State ─────────────────────────────────────────────────────────────

  let _parentWindow = window.parent;
  let _parentOrigin = null;
  let _diceReady = false;
  let _pendingRequests = new Map(); // requestId → { element, timerId }
  let _enhancedElements = [];

  const REQUEST_TIMEOUT_MS = 12000; // Client-side timeout (slightly longer than shell's)

  // ── Initialization ────────────────────────────────────────────────────

  /**
   * Detect if running inside an iframe with a parent that could be the
   * extension shell.
   */
  function init() {
    if (window.self === window.top) {
      // Not in an iframe — no enhancement possible. Values stay as text.
      return;
    }

    // Calculate expected parent origin from referrer or assume same origin.
    try {
      _parentOrigin = new URL(document.referrer || window.location.href).origin;
    } catch {
      _parentOrigin = window.location.origin;
    }

    // Listen for messages from the parent shell.
    window.addEventListener("message", _handleMessage);

    // Clean up on unload.
    window.addEventListener("beforeunload", _destroy);
  }

  // ── Message handling ──────────────────────────────────────────────────

  function _handleMessage(event) {
    // Validate source is the parent window.
    if (event.source !== _parentWindow) return;

    const data = event.data;
    if (!data || typeof data !== "object") return;
    if (data.source !== SOURCE) return;
    if (data.version !== PROTOCOL_VERSION) return;

    switch (data.type) {
      case MessageType.DICE_READY:
        _handleDiceReady(data.payload);
        break;
      case MessageType.ROLL_RESULT:
        _handleRollResult(data.payload);
        break;
      case MessageType.ROLL_ERROR:
        _handleRollError(data.payload);
        break;
    }
  }

  // ── Dice readiness ────────────────────────────────────────────────────

  function _handleDiceReady(payload) {
    const wasReady = _diceReady;
    _diceReady = payload && payload.ready === true;
    if (_diceReady && !wasReady) {
      _enhanceRollValues();
    } else if (!_diceReady && wasReady) {
      _removeEnhancements();
    }
  }

  // ── Progressive enhancement (task 4.3) ────────────────────────────────

  /**
   * Find all elements with [data-roll-notation] and transform them into
   * interactive roll controls. The visible text (the number or formula)
   * becomes the clickable control — no separate "Roll" button is added.
   */
  function _enhanceRollValues() {
    const elements = document.querySelectorAll("[data-roll-notation]");

    elements.forEach((el) => {
      const notation = el.getAttribute("data-roll-notation");
      if (!notation || notation.trim().length === 0) return;

      const label =
        el.getAttribute("data-roll-label") || el.textContent.trim();

      // Mark as enhanced.
      el.classList.add("roll-enhanced", "roll-ready");
      el.setAttribute("role", "button");
      el.setAttribute("tabindex", "0");
      el.setAttribute(
        "aria-label",
        `Rolar ${label}: ${notation}`
      );
      el.style.cursor = "pointer";

      // Click handler.
      const clickHandler = (e) => {
        e.preventDefault();
        _requestRoll(el, notation, label);
      };

      // Keyboard handler (Enter / Space).
      const keyHandler = (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          _requestRoll(el, notation, label);
        }
      };

      el.addEventListener("click", clickHandler);
      el.addEventListener("keydown", keyHandler);

      _enhancedElements.push({
        element: el,
        clickHandler,
        keyHandler,
      });
    });
  }

  /**
   * Remove enhancements from all previously enhanced elements.
   */
  function _removeEnhancements() {
    _enhancedElements.forEach(({ element, clickHandler, keyHandler }) => {
      element.classList.remove(
        "roll-enhanced",
        "roll-ready",
        "roll-pending"
      );
      element.removeAttribute("role");
      element.removeAttribute("tabindex");
      element.removeAttribute("aria-label");
      element.style.cursor = "";
      element.removeEventListener("click", clickHandler);
      element.removeEventListener("keydown", keyHandler);

    });
    _enhancedElements = [];
  }

  // ── Roll request ──────────────────────────────────────────────────────

  function _requestRoll(element, notation, label) {
    // Prevent duplicate activation while pending.
    if (element.classList.contains("roll-pending")) return;

    const requestId = _generateId();

    // Set pending state (task 4.4).
    element.classList.remove("roll-ready");
    element.classList.add("roll-pending");
    element.setAttribute("aria-busy", "true");

    // Client-side timeout.
    const timerId = setTimeout(() => {
      _pendingRequests.delete(requestId);
      _finishRoll(element);
      console.warn("[Character Sheet] Dice+ roll timed out", { requestId, notation });
    }, REQUEST_TIMEOUT_MS);

    _pendingRequests.set(requestId, { element, timerId });

    // Send roll request to parent shell.
    _sendToParent(MessageType.ROLL_REQUEST, {
      requestId,
      notation,
      label,
    });
  }

  // ── Roll completion handlers (task 4.4) ──────────────────────────────

  function _handleRollResult(payload) {
    const requestId = payload.requestId;
    if (!requestId) return;

    const pending = _pendingRequests.get(requestId);
    if (!pending) return;

    clearTimeout(pending.timerId);
    _pendingRequests.delete(requestId);

    _finishRoll(pending.element);
  }

  function _handleRollError(payload) {
    const requestId = payload.requestId;
    if (!requestId) return;

    const pending = _pendingRequests.get(requestId);
    if (!pending) return;

    clearTimeout(pending.timerId);
    _pendingRequests.delete(requestId);

    _finishRoll(pending.element);
    console.warn("[Character Sheet] Dice+ roll failed", {
      requestId,
      error: payload.error || "Unknown error",
    });
  }

  // ── UI pending-state management (task 4.4) ───────────────────────────

  function _finishRoll(element) {
    element.classList.remove("roll-pending");
    element.classList.add("roll-ready");
    element.removeAttribute("aria-busy");
  }

  // ── Communication helpers ─────────────────────────────────────────────

  function _sendToParent(type, payload) {
    if (!_parentWindow || !_parentOrigin) return;

    _parentWindow.postMessage(
      {
        source: SOURCE,
        version: PROTOCOL_VERSION,
        type,
        payload,
      },
      _parentOrigin
    );
  }

  function _generateId() {
    return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
  }

  // ── Cleanup ───────────────────────────────────────────────────────────

  function _destroy() {
    window.removeEventListener("message", _handleMessage);

    // Clear all pending requests.
    for (const [, entry] of _pendingRequests) {
      clearTimeout(entry.timerId);
    }
    _pendingRequests.clear();

    _removeEnhancements();
  }

  // ── Start ─────────────────────────────────────────────────────────────

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
