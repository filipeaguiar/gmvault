/**
 * Owlbear Character Sheet Extension — Main Module
 *
 * Namespace: io.github.filipeaguiar.character-sheet
 * SDK imported via ESM CDN with fixed version.
 * Vanilla JavaScript, no frameworks, no bundler.
 */

const {
  initBridge,
  bindIframe,
  unbindIframe,
  destroyBridge,
  isDiceReady,
  normalizePlayerIdentity,
} = await import(`./bridge.js?cache=${Date.now()}`);

// ---------------------------------------------------------------------------
// SDK Import
// ---------------------------------------------------------------------------

let OBR = null;
let bridgeInitialized = false;
let playerInfo = { id: null, name: null };

const CATALOG_URL = "/gmvault/character-catalog.json";
const STORAGE_KEY_PREFIX = "character-sheet-selection";

// ---------------------------------------------------------------------------
// DOM References
// ---------------------------------------------------------------------------

const statusBar = document.getElementById("status-bar");
const characterSelector = document.getElementById("character-selector");
const characterList = document.getElementById("character-list");
const sheetContainer = document.getElementById("sheet-container");
const changeBtn = document.getElementById("change-character-btn");
const characterIframe = document.getElementById("character-iframe");
const debugLog = document.getElementById("debug-log");

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------

let catalog = [];
let obrConnectionPromise = null;
let obrProbeTimer = null;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function storageKey() {
  const suffix = playerInfo.id || "local";
  return `${STORAGE_KEY_PREFIX}-${suffix}`;
}

function setStatus(text, type) {
  statusBar.textContent = text;
  statusBar.className = "";
  if (type === "error") statusBar.classList.add("status-error");
  else if (type === "ok") statusBar.classList.add("status-ok");
  else if (type === "connected") statusBar.classList.add("status-connected");
  else if (type === "disconnected") statusBar.classList.add("status-disconnected");
}

function addDebugLog(message) {
  if (!debugLog) return;
  const time = new Date().toLocaleTimeString("pt-BR");
  const lines = `${debugLog.textContent}${debugLog.textContent ? "\n" : ""}[${time}] ${message}`
    .split("\n")
    .slice(-40);
  debugLog.textContent = lines.join("\n");
  debugLog.scrollTop = debugLog.scrollHeight;
}

function replayEarlyObrReadyMessages() {
  const messages = Array.isArray(window.__gmvaultEarlyObrReady)
    ? window.__gmvaultEarlyObrReady.splice(0)
    : [];
  if (messages.length === 0) return;

  addDebugLog(`Recuperando ${messages.length} mensagem(ns) OBR_READY recebida(s) antes do SDK.`);
  for (const message of messages) {
    window.dispatchEvent(new MessageEvent("message", {
      data: message.data,
      origin: message.origin,
    }));
  }
}

function saveSelection(url) {
  try {
    localStorage.setItem(storageKey(), url);
  } catch {
    // localStorage may be unavailable; silently ignore.
  }
}

function loadSelection() {
  try {
    return localStorage.getItem(storageKey());
  } catch {
    return null;
  }
}

function clearSelection() {
  try {
    localStorage.removeItem(storageKey());
  } catch {
    // Ignore.
  }
}

function isValidEntry(entry) {
  return entry && typeof entry.title === "string" && entry.title.trim() !== "" &&
         typeof entry.url === "string" && entry.url.trim() !== "";
}

function catalogHasUrl(url) {
  return catalog.some((entry) => entry.url === url);
}

// ---------------------------------------------------------------------------
// Rendering
// ---------------------------------------------------------------------------

function renderCatalog() {
  characterList.innerHTML = "";

  if (catalog.length === 0) {
    const empty = document.createElement("div");
    empty.className = "state-empty";
    empty.textContent = "Nenhum personagem disponível.";
    characterList.appendChild(empty);
    return;
  }

  for (const entry of catalog) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "character-card";

    const nameSpan = document.createElement("span");
    nameSpan.className = "card-name";
    nameSpan.textContent = entry.title;
    btn.appendChild(nameSpan);

    if (entry.campaign) {
      const campaignSpan = document.createElement("span");
      campaignSpan.className = "card-campaign";
      campaignSpan.textContent = entry.campaign;
      btn.appendChild(campaignSpan);
    }

    if (entry.summary) {
      const summarySpan = document.createElement("span");
      summarySpan.className = "card-summary";
      summarySpan.textContent = entry.summary;
      btn.appendChild(summarySpan);
    }

    btn.addEventListener("click", () => selectCharacter(entry.url));
    characterList.appendChild(btn);
  }
}

function showSelector() {
  characterSelector.hidden = false;
  sheetContainer.hidden = true;
}

function showSheet(url) {
  characterSelector.hidden = true;
  sheetContainer.hidden = false;

  // Unbind previous bridge binding before changing src.
  unbindIframe();

  // Bind bridge after iframe loads (task 3.2). Register before changing
  // src so a cached character page cannot win the load-event race.
  characterIframe.onload = () => {
    if (bridgeInitialized) {
      bindIframe(characterIframe);
    }
  };

  characterIframe.src = url;
}

// ---------------------------------------------------------------------------
// Selection Logic
// ---------------------------------------------------------------------------

function selectCharacter(url) {
  saveSelection(url);
  showSheet(url);
  setStatus("Ficha carregada", "ok");
}

function changeCharacter() {
  showSelector();
  setStatus("Selecione um personagem", "ok");
}

function applySavedSelection() {
  const saved = loadSelection();
  if (saved && catalogHasUrl(saved)) {
    showSheet(saved);
    setStatus("Ficha carregada", "ok");
    return true;
  }

  if (saved) {
    clearSelection();
  }

  setStatus("Selecione um personagem", "ok");
  return false;
}

async function loadPlayerInfo() {
  if (!OBR?.isAvailable) return false;

  try {
    const [name, id] = await Promise.all([
      OBR.player.getName(),
      OBR.player.getId(),
    ]);
    const identity = normalizePlayerIdentity(id, name);
    if (!identity) return false;
    // Preserve the object reference passed to the Dice+ bridge.
    Object.assign(playerInfo, identity);
    return true;
  } catch {
    return false;
  }
}

// ---------------------------------------------------------------------------
// Catalog Fetch
// ---------------------------------------------------------------------------

async function fetchCatalog() {
  setStatus("Carregando catálogo...", "");

  characterList.innerHTML = "";
  const loader = document.createElement("div");
  loader.className = "loading-indicator";
  loader.textContent = "Buscando personagens...";
  characterList.appendChild(loader);

  try {
    const resp = await fetch(CATALOG_URL);
    if (!resp.ok) {
      throw new Error(`HTTP ${resp.status}`);
    }
    const data = await resp.json();

    // Accept both array and object with a "characters" key.
    const raw = Array.isArray(data) ? data : (Array.isArray(data.characters) ? data.characters : []);
    catalog = raw.filter(isValidEntry);

    renderCatalog();

    if (catalog.length === 0) {
      setStatus("Nenhum personagem encontrado no catálogo.", "");
      return;
    }

    applySavedSelection();
  } catch (err) {
    characterList.innerHTML = "";
    const errDiv = document.createElement("div");
    errDiv.className = "state-error";
    errDiv.textContent = `Erro ao carregar catálogo: ${err.message}`;
    characterList.appendChild(errDiv);
    setStatus("Erro ao carregar catálogo", "error");
  }
}

// ---------------------------------------------------------------------------
// OBR SDK Initialization
// ---------------------------------------------------------------------------

async function connectOwlbear(trigger) {
  if (bridgeInitialized) return true;
  if (obrConnectionPromise) return obrConnectionPromise;

  obrConnectionPromise = (async () => {
    addDebugLog(`Tentando conexão Owlbear (${trigger}).`);
    const playerLoaded = await loadPlayerInfo();
    if (!playerLoaded) {
      addDebugLog("Nome ou ID do jogador ainda não está disponível.");
      return false;
    }

    addDebugLog(`Jogador identificado: ${playerInfo.name}.`);
    setStatus(`Conectado: ${playerInfo.name} — Dice+ desconectado`, "disconnected");
    initBridge(OBR, playerInfo, (ready) => {
      if (ready) {
        setStatus(`Conectado: ${playerInfo.name || "Owlbear"} — Dice+ ativo`, "connected");
      } else {
        setStatus(`Conectado: ${playerInfo.name || "Owlbear"} — Dice+ desconectado`, "disconnected");
      }
    }, addDebugLog);
    bridgeInitialized = true;

    if (obrProbeTimer) {
      clearInterval(obrProbeTimer);
      obrProbeTimer = null;
    }
    if (!sheetContainer.hidden && characterIframe.getAttribute("src")) {
      bindIframe(characterIframe);
    }
    await fetchCatalog();
    return true;
  })();

  try {
    return await obrConnectionPromise;
  } finally {
    obrConnectionPromise = null;
  }
}

async function initOBR() {
  try {
    const module = await import(
      "https://esm.sh/@owlbear-rodeo/sdk@3.1.0"
    );
    OBR = module.default || module;
    replayEarlyObrReadyMessages();
    addDebugLog(`SDK Owlbear carregado; disponível: ${Boolean(OBR.isAvailable)}; pronto: ${Boolean(OBR.isReady)}`);

    if (!OBR.isAvailable) {
      setStatus("Modo local (sem Owlbear)", "");
      await fetchCatalog();
      return;
    }

    addDebugLog("Aguardando OBR.onReady.");
    OBR.onReady(() => {
      addDebugLog("OBR.onReady recebido.");
      void connectOwlbear("OBR.onReady");
    });

    // Chrome Android can report isAvailable before dispatching onReady. Keep
    // the catalog usable and probe the player API for up to 15 seconds.
    setTimeout(() => {
      if (bridgeInitialized) return;
      addDebugLog("OBR.onReady não respondeu em 1,5 s; iniciando diagnóstico alternativo.");
      void fetchCatalog();
      let attempts = 0;
      obrProbeTimer = setInterval(() => {
        attempts += 1;
        void connectOwlbear(`tentativa alternativa ${attempts}/15`);
        if (attempts >= 15 && obrProbeTimer) {
          clearInterval(obrProbeTimer);
          obrProbeTimer = null;
          addDebugLog("Owlbear não disponibilizou a identidade após 15 tentativas.");
        }
      }, 1000);
    }, 1500);
  } catch (error) {
    console.error("[Character Sheet] Falha ao inicializar SDK Owlbear", error);
    addDebugLog("Falha ao carregar o SDK Owlbear.");
    setStatus("Modo local (sem Owlbear)", "");
    await fetchCatalog();
  }
}

// ---------------------------------------------------------------------------
// Event Listeners
// ---------------------------------------------------------------------------

changeBtn.addEventListener("click", changeCharacter);

// Clean up bridge on extension unload (task 3.7).
window.addEventListener("beforeunload", () => {
  if (obrProbeTimer) clearInterval(obrProbeTimer);
  destroyBridge();
});

// ---------------------------------------------------------------------------
// Bootstrap
// ---------------------------------------------------------------------------

initOBR();
