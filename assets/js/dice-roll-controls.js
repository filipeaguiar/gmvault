import { createDicePlusClient } from "./dice-plus-bridge.js";

const CONTROL_SELECTOR = "[data-dice-roll]";
const DEFAULT_ROLL_TARGET = "everyone";

function setState(button, state, message) {
  button.dataset.diceState = state;
  button.disabled = state !== "ready" && state !== "error" && state !== "completed";
  button.setAttribute("aria-busy", state === "rolling" ? "true" : "false");
  if (message) {
    const output = button.closest("[data-dice-action]")?.querySelector("[data-dice-result]");
    if (output) output.textContent = message;
  }
}

function getTargetOrigin(root) {
  return root.dataset.gmvaultTargetOrigin || undefined;
}

function showResult(button, payload) {
  const output = button.closest("[data-dice-action]")?.querySelector("[data-dice-result]");
  if (!output) return;
  const result = payload?.result || {};
  const total = typeof result.totalValue === "number" ? String(result.totalValue) : "Resultado recebido";
  const summary = typeof result.rollSummary === "string" && result.rollSummary.length > 0
    ? `: ${result.rollSummary}`
    : "";
  output.textContent = `${total}${summary}`;
}

async function initializeDiceRollControls(root = document) {
  const buttons = [...root.querySelectorAll(CONTROL_SELECTOR)];
  if (buttons.length === 0) return null;

  const client = createDicePlusClient({ targetOrigin: getTargetOrigin(root.documentElement || root) });
  for (const button of buttons) setState(button, "preparing", "Verificando Dice+...");

  if (!client.available || !(await client.checkAvailability())) {
    for (const button of buttons) setState(button, "unavailable", "Dice+ indisponível nesta sala.");
    client.destroy();
    return null;
  }

  for (const button of buttons) {
    setState(button, "ready", "Pronto para rolar.");
    button.addEventListener("click", async () => {
      if (button.dataset.diceState !== "ready" && button.dataset.diceState !== "error" && button.dataset.diceState !== "completed") return;
      const notation = button.dataset.diceNotation;
      const label = button.dataset.diceLabel || button.textContent.trim();
      const rollTarget = button.dataset.diceTarget || DEFAULT_ROLL_TARGET;
      setState(button, "rolling", "Rolando...");
      try {
        const result = await client.requestRoll({
          diceNotation: notation,
          label,
          rollTarget,
          showResults: button.dataset.diceShowResults !== "false",
        });
        showResult(button, result);
        setState(button, "completed");
      } catch (error) {
        setState(button, "error", error instanceof Error ? error.message : "Não foi possível rolar.");
      }
    });
  }

  return client;
}

if (typeof window !== "undefined") {
  window.GMVaultDiceControls = { initializeDiceRollControls };
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => initializeDiceRollControls());
  } else {
    initializeDiceRollControls();
  }
}

export { initializeDiceRollControls };
