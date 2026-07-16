const CONTROL_SELECTOR = "[data-dice-roll]";
const DEFAULT_ROLL_TARGET = "everyone";
const STATUS_ID = "gmvault-dice-status";
const LOG_PREFIX = "[GM Vault Dice]";

function logInfo(...args) {
  console.info(LOG_PREFIX, ...args);
}

function logWarn(...args) {
  console.warn(LOG_PREFIX, ...args);
}

function logError(...args) {
  console.error(LOG_PREFIX, ...args);
}

function getStatusContainer(root) {
  const container = root.querySelector?.(".char-sheet-container") || root.body || root.documentElement || root;
  let status = container.querySelector?.(`#${STATUS_ID}`);
  if (!status && container.appendChild) {
    status = document.createElement("div");
    status.id = STATUS_ID;
    status.className = "dice-roll-status";
    container.prepend(status);
  }
  return status;
}

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
  const html = root.documentElement || root;
  return html?.dataset?.gmvaultTargetOrigin || undefined;
}

function describeAvailability(reason) {
  const labels = {
    "window-unavailable": "janela indisponível",
    "no-parent": "sem janela pai",
    "invalid-target-origin": "origem do iframe inválida",
    "bridge-unavailable": "ponte gm-vault indisponível",
    timeout: "sem resposta do host",
    "postmessage-failed": "falha ao enviar mensagem ao host",
    "dice-plus-unavailable": "Dice+ respondeu indisponível",
    ready: "pronto",
  };
  return labels[reason] || reason || "motivo desconhecido";
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

function collectDiagnostics(root = document) {
  const bridge = globalThis.GMVaultDice || null;
  const status = getStatusContainer(root)?.textContent || null;
  const buttons = [...root.querySelectorAll(CONTROL_SELECTOR)].map((button, index) => ({
    index,
    text: button.textContent.trim(),
    notation: button.dataset.diceNotation || null,
    label: button.dataset.diceLabel || null,
    target: button.dataset.diceTarget || null,
    state: button.dataset.diceState || null,
    disabled: Boolean(button.disabled),
  }));

  return {
    href: root.location?.href || location.href,
    origin: root.location?.origin || location.origin,
    referrer: root.referrer || document.referrer || null,
    isIframe: window.self !== window.top,
    hasParent: window.parent && window.parent !== window,
    readyState: document.readyState,
    targetOrigin: getTargetOrigin(root),
    bridgeReady: Boolean(bridge && typeof bridge.createDicePlusClient === "function"),
    resolvedTargetOrigin: bridge?.resolvedTargetOrigin || null,
    scripts: [...document.scripts].map((script) => script.src).filter(Boolean).filter((src) => src.includes("dice")),
    globals: {
      GMVaultDice: Boolean(window.GMVaultDice),
      GMVaultDiceControls: Boolean(window.GMVaultDiceControls),
      GMVaultDiceHost: Boolean(window.GMVaultDiceHost),
    },
    buttons,
    status,
  };
}

async function runDiagnostics(root = document) {
  const diagnostics = collectDiagnostics(root);
  console.group(LOG_PREFIX, "Diagnóstico");
  console.log(diagnostics);
  console.groupEnd();

  const bridge = globalThis.GMVaultDice;
  if (bridge?.createDicePlusClient) {
    const client = bridge.createDicePlusClient({ targetOrigin: getTargetOrigin(root) || "*" });
    diagnostics.bridgeResolvedTargetOrigin = client.resolvedTargetOrigin;
    try {
      diagnostics.availability = typeof client.checkAvailabilityDetailed === "function"
        ? await client.checkAvailabilityDetailed()
        : { ready: await client.checkAvailability(), reason: "legacy-check" };
      console.info(LOG_PREFIX, "Disponibilidade detalhada", diagnostics.availability);
    } catch (error) {
      diagnostics.availabilityError = error instanceof Error ? error.message : String(error);
      console.error(LOG_PREFIX, "Erro no diagnóstico de disponibilidade", error);
    } finally {
      client.destroy();
    }
  }

  return diagnostics;
}

async function initializeDiceRollControls(root = document) {
  const buttons = [...root.querySelectorAll(CONTROL_SELECTOR)];
  if (buttons.length === 0) return null;

  const bridge = globalThis.GMVaultDice;
  const targetOrigin = getTargetOrigin(root);
  logInfo("Inicializando controles", { buttons: buttons.length, targetOrigin, bridgeReady: Boolean(bridge && typeof bridge.createDicePlusClient === "function") });

  if (!bridge || typeof bridge.createDicePlusClient !== "function") {
    const status = getStatusContainer(root);
    const message = "Ponte Dice+ indisponível.";
    if (status) status.textContent = message;
    for (const button of buttons) setState(button, "unavailable", message);
    logError(message, { bridge });
    return null;
  }

  const status = getStatusContainer(root);
  const client = bridge.createDicePlusClient({ targetOrigin });
  logInfo("Ponte resolvida", { targetOrigin: client.resolvedTargetOrigin });
  for (const button of buttons) setState(button, "preparing", "Verificando Dice+...");
  if (status) status.textContent = "Verificando Dice+...";

  const availability = typeof client.checkAvailabilityDetailed === "function"
    ? await client.checkAvailabilityDetailed()
    : { ready: await client.checkAvailability(), reason: "legacy-check" };

  if (!availability.ready) {
    const reason = describeAvailability(availability.reason);
    const message = `Dice+ indisponível nesta sala (${reason}).`;
    for (const button of buttons) setState(button, "unavailable", message);
    if (status) status.textContent = message;
    logWarn(message, { availability, targetOrigin, resolvedTargetOrigin: client.resolvedTargetOrigin });
    client.destroy();
    return null;
  }

  if (status) status.textContent = "Dice+ disponível.";
  logInfo("Dice+ disponível", { targetOrigin, resolvedTargetOrigin: client.resolvedTargetOrigin });

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
  window.GMVaultDiceControls = { initializeDiceRollControls, runDiagnostics };
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => initializeDiceRollControls());
  } else {
    initializeDiceRollControls();
  }
}

export { initializeDiceRollControls };
