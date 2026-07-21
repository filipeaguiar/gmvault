/**
 * Dice+ Roll Engine for GM Vault.
 * 
 * Manages click listeners on [data-roll-notation] elements.
 * - Inside an iframe, posts a ROLL_REQUEST message to parent window.
 * - Outside an iframe, calculates the roll locally and pops a modern toast.
 * - Automatically parses text nodes inside monster statblocks to make formulas clickable.
 */
(function() {
  "use strict";

  const SOURCE = "io.github.filipeaguiar.character-sheet";
  const PROTOCOL_VERSION = 1;

  // Initialize roll engine
  function init() {
    // 1. Parse text nodes to auto-add roll notations
    parsePageTexts();

    // 2. Bind click event delegation to all rollable elements
    document.addEventListener("click", handleRollClick);
    document.addEventListener("keydown", handleRollKeydown);

    // 3. Mark enhanced items visually
    markEnhancedElements();
  }

  // Find and enhance all [data-roll-notation] elements
  function markEnhancedElements() {
    document.querySelectorAll("[data-roll-notation]").forEach(el => {
      if (!el.classList.contains("roll-ready")) {
        el.classList.add("roll-ready");
        el.setAttribute("role", "button");
        el.setAttribute("tabindex", "0");
        const label = el.getAttribute("data-roll-label") || "Rolagem";
        const notation = el.getAttribute("data-roll-notation");
        el.setAttribute("aria-label", `Rolar ${label}: ${notation}`);
      }
    });
  }

  // Handle keyboard activation (Enter / Space)
  function handleRollKeydown(e) {
    if (e.key === "Enter" || e.key === " ") {
      const el = e.target.closest("[data-roll-notation]");
      if (el) {
        e.preventDefault();
        triggerRoll(el);
      }
    }
  }

  // Handle click activation
  function handleRollClick(e) {
    const el = e.target.closest("[data-roll-notation]");
    if (el) {
      e.preventDefault();
      triggerRoll(el);
    }
  }

  // Trigger the roll request or local roll
  function triggerRoll(element) {
    if (element.classList.contains("roll-pending")) return;

    const notation = element.getAttribute("data-roll-notation");
    const label = element.getAttribute("data-roll-label") || "Rolagem";

    if (!notation) return;

    // Check if running inside iframe (VTT)
    if (window.self !== window.top) {
      // Send roll request to parent shell (Owlbear VTT Bridge)
      element.classList.add("roll-pending");
      const requestId = Math.random().toString(36).substring(2, 9);
      
      const payload = {
        source: SOURCE,
        version: PROTOCOL_VERSION,
        type: "roll-request",
        payload: {
          requestId: requestId,
          notation: notation,
          label: label
        }
      };

      try {
        const parentOrigin = new URL(document.referrer || window.location.href).origin;
        window.parent.postMessage(payload, parentOrigin);
      } catch (err) {
        window.parent.postMessage(payload, "*");
      }

      // Reset pending state after a timeout
      setTimeout(() => {
        element.classList.remove("roll-pending");
      }, 3000);
    } else {
      // Roll locally
      executeLocalRoll(notation, label);
    }
  }

  // Perform local roll calculation and show toast
  function executeLocalRoll(notation, label) {
    try {
      const result = parseAndRoll(notation);
      showRollToast(label, notation, result);
    } catch (e) {
      console.error("Erro ao rolar dados localmente:", e);
    }
  }

  // Parse notation and roll dice (e.g. 1d20+5, 2d6, 1d12-1)
  function parseAndRoll(notation) {
    const cleanNotation = notation.replace(/\s+/g, "").toLowerCase();
    
    // Support flat rolls (+5, -2) -> 1d20+5, 1d20-2
    let parsedNotation = cleanNotation;
    if (cleanNotation.startsWith("+") || cleanNotation.startsWith("-")) {
      parsedNotation = "1d20" + cleanNotation;
    } else if (/^\d+$/.test(cleanNotation)) {
      parsedNotation = "1d20+" + cleanNotation;
    }

    const diceRegex = /(\d+)d(\d+)/g;
    const parts = [];
    let match;
    let index = 0;
    
    // Find all dice pools
    while ((match = diceRegex.exec(parsedNotation)) !== null) {
      const count = parseInt(match[1], 10);
      const faces = parseInt(match[2], 10);
      const rolls = [];
      let poolSum = 0;
      
      for (let i = 0; i < count; i++) {
        const roll = Math.floor(Math.random() * faces) + 1;
        rolls.push(roll);
        poolSum += roll;
      }
      
      parts.push({
        type: "dice",
        text: match[0],
        rolls: rolls,
        sum: poolSum,
        start: match.index,
        end: diceRegex.lastIndex
      });
    }

    // Get the remaining string modifiers (e.g., +5, -1)
    let modifier = 0;
    let modText = parsedNotation;
    parts.forEach(p => {
      modText = modText.replace(p.text, "");
    });

    if (modText) {
      // Evaluate basic modifiers like +5, -2
      try {
        modifier = eval(modText) || 0;
      } catch (err) {
        modifier = parseInt(modText, 10) || 0;
      }
    }

    // Calculate total sum
    const totalSum = parts.reduce((sum, p) => sum + p.sum, 0) + modifier;

    // Build details text
    const diceDetails = parts.map(p => `[${p.rolls.join(", ")}]`).join(" + ");
    const modDetailSign = modifier >= 0 ? "+" : "-";
    const details = diceDetails + (modifier !== 0 ? ` ${modDetailSign} ${Math.abs(modifier)}` : "");

    return {
      total: totalSum,
      details: details
    };
  }

  // Render a toast notification for rolls
  function showRollToast(label, notation, result) {
    let container = document.querySelector(".roll-toast-container");
    if (!container) {
      container = document.createElement("div");
      container.className = "roll-toast-container";
      document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.className = "roll-toast";
    
    toast.innerHTML = `
      <div class="roll-toast-header">${label}</div>
      <div class="roll-toast-formula">Fórmula: ${notation}</div>
      <div class="roll-toast-result">Resultado: ${result.total}</div>
      <div class="roll-toast-details">Rolado: ${result.details}</div>
    `;

    container.appendChild(toast);

    // Auto-remove toast after 4s
    setTimeout(() => {
      toast.style.transition = "opacity 0.5s ease-out, transform 0.5s ease-out";
      toast.style.opacity = "0";
      toast.style.transform = "translateY(-10px)";
      setTimeout(() => {
        toast.remove();
        if (container.children.length === 0) {
          container.remove();
        }
      }, 500);
    }, 4000);
  }

  // Recursively parse text nodes to enhance text formulas
  function parsePageTexts() {
    // Only run on statblocks and content areas to prevent breaking site UI
    const targets = document.querySelectorAll(".stat-block, .content-body, .char-list-item");
    if (targets.length === 0) return;

    // Matches dice formulas (e.g. 2d6+5, 1d12, 1d20 - 1)
    const diceRegex = /(\b\d+d\d+(?:\s*[+-]\s*\d+)?\b)/gi;
    
    // Matches attack bonuses (e.g. +9 to hit, +9 para acertar)
    const attackRegex = /([+-]\d+)\s*(?:para acertar|to hit|no ataque|de bônus de ataque)/gi;

    targets.forEach(target => {
      enhanceTextInElement(target, diceRegex, "Dano");
      enhanceTextInElement(target, attackRegex, "Ataque", true);
      
      // Parse saves and skills in details block
      const details = target.querySelector(".stat-details");
      if (details) {
        const modRegex = /([+-]\d+)\b/g;
        enhanceTextInElement(details, modRegex, "Modificador", true);
      }
    });
  }

  // Walk element children and replace text matches
  function enhanceTextInElement(element, regex, label, isModifier = false) {
    const walk = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, {
      acceptNode: function(node) {
        // Skip already enhanced elements and form fields
        const parent = node.parentElement;
        if (!parent) return NodeFilter.FILTER_REJECT;
        const tag = parent.tagName.toUpperCase();
        if (tag === "SCRIPT" || tag === "STYLE" || tag === "A" || tag === "BUTTON" || tag === "INPUT" || tag === "TEXTAREA" || parent.hasAttribute("data-roll-notation")) {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    });

    const nodes = [];
    let node;
    while (node = walk.nextNode()) {
      nodes.push(node);
    }

    nodes.forEach(node => {
      const text = node.nodeValue;
      if (!regex.test(text)) return;
      
      regex.lastIndex = 0; // reset regex index
      const fragment = document.createDocumentFragment();
      let lastIndex = 0;
      let match;

      while ((match = regex.exec(text)) !== null) {
        // Add preceding text
        if (match.index > lastIndex) {
          fragment.appendChild(document.createTextNode(text.substring(lastIndex, match.index)));
        }

        // Create rollable span
        const span = document.createElement("span");
        span.className = "roll-ready";
        
        let matchText = match[0];
        let notation = matchText;

        if (isModifier) {
          // If match is just a modifier (like "+9"), notation becomes "1d20+9"
          const val = match[1];
          notation = `1d20${val}`;
        } else {
          // If match has a prefix like "(3d6 + 5)", strip parens for notation
          notation = notation.replace(/[()]/g, "").trim();
        }

        span.setAttribute("data-roll-notation", notation);
        span.setAttribute("data-roll-label", `${label} (${document.title})`);
        span.textContent = matchText;

        fragment.appendChild(span);
        lastIndex = regex.lastIndex;
      }

      // Add remaining text
      if (lastIndex < text.length) {
        fragment.appendChild(document.createTextNode(text.substring(lastIndex)));
      }

      node.parentNode.replaceChild(fragment, node);
    });
  }

  // Start engine on DOM load
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
