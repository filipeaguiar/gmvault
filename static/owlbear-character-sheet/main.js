/**
 * Owlbear Character Sheet Extension — Main Module
 *
 * Namespace: io.github.filipeaguiar.character-sheet
 * SDK imported via ESM CDN with fixed version.
 * Vanilla JavaScript, no frameworks, no bundler.
 */

import { initBridge, bindIframe, unbindIframe, destroyBridge, isDiceReady } from "./bridge.js";

// ---------------------------------------------------------------------------
// SDK Import
// ---------------------------------------------------------------------------

let OBR = null;
let obrReady = false;
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

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------

let catalog = [];

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

  characterIframe.src = url;

  // Bind bridge after iframe loads (task 3.2).
  characterIframe.onload = () => {
    if (obrReady) {
      bindIframe(characterIframe);
    }
  };
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

    // Check for saved selection.
    const saved = loadSelection();
    if (saved && catalogHasUrl(saved)) {
      showSheet(saved);
      setStatus("Ficha carregada", "ok");
    } else {
      // Discard stale selection if any.
      if (saved) clearSelection();
      setStatus("Selecione um personagem", "ok");
    }
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

async function initOBR() {
  try {
    const module = await import(
      "https://cdn.jsdelivr.net/npm/@owlbear-rodeo/sdk@2.5.0/dist/index.mjs"
    );
    OBR = module.default || module;

    OBR.onReady(async () => {
      obrReady = true;
      try {
        const name = await OBR.player.getName();
        const id = await OBR.player.getId();
        playerInfo = { id, name };
        setStatus(`Conectado: ${name}`, "ok");
      } catch {
        setStatus("Conectado ao Owlbear", "ok");
      }

      // Initialize Dice+ bridge (task 3.2).
      initBridge(OBR, playerInfo, (ready) => {
        if (ready) {
          setStatus(`Conectado: ${playerInfo.name || "Owlbear"} — Dice+ ativo`, "ok");
        }
      });

      // Re-fetch catalog now that we have a player ID for localStorage key.
      await fetchCatalog();
    });
  } catch {
    // Running outside Owlbear — degrade gracefully.
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
  destroyBridge();
});

// ---------------------------------------------------------------------------
// Bootstrap
// ---------------------------------------------------------------------------

initOBR();
