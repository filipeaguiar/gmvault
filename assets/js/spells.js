document.addEventListener("DOMContentLoaded", () => {
    const spellManager = document.querySelector(".spell-manager");
    if (!spellManager) {
        return;
    }

    const searchInput = document.getElementById("spell-search");
    const readySpellsList = document.getElementById("ready-spells-list");
    const managementSpellsList = document.getElementById("management-spells-list");
    const levelButtons = Array.from(spellManager.querySelectorAll(".spell-level-filter"));
    const slotGroups = Array.from(spellManager.querySelectorAll(".spell-slots-tracker .slot-level-group"));
    const readyCounter = spellManager.querySelector('[data-spell-counter-value="ready"]');
    const storageKey = `gmvault.spell-manager:${window.location.pathname}`;

    let activeLevel = "all";
    let searchQuery = "";

    const hasStorage = (() => {
        try {
            const probeKey = `${storageKey}:probe`;
            window.localStorage.setItem(probeKey, "1");
            window.localStorage.removeItem(probeKey);
            return true;
        } catch (error) {
            return false;
        }
    })();

    function getSpellCards() {
        return Array.from(spellManager.querySelectorAll(".spell-card"));
    }

    function getReadyRefs() {
        if (!readySpellsList) {
            return [];
        }
        return Array.from(readySpellsList.querySelectorAll(".spell-card"))
            .map((card) => card.getAttribute("data-spell-ref"))
            .filter(Boolean);
    }

    function updateReadyCounter() {
        if (readyCounter) {
            readyCounter.textContent = String(getReadyRefs().length);
        }
    }

    function updateCollectionState(collection) {
        if (!collection) {
            return;
        }

        collection.querySelectorAll(".spell-level-group").forEach((group) => {
            const cards = Array.from(group.querySelectorAll(".spell-card"));
            group.classList.toggle("is-empty", cards.length === 0);
            group.hidden = cards.length === 0 || cards.every((card) => card.style.display === "none");
        });

        const section = collection.closest(".spell-collection");
        const emptyMessage = section ? section.querySelector(".spell-empty-message") : null;
        if (emptyMessage) {
            emptyMessage.classList.toggle("is-hidden", collection.querySelectorAll(".spell-card").length > 0);
        }
    }

    function applyFilters() {
        getSpellCards().forEach((card) => {
            const name = (card.getAttribute("data-spell-name") || "").toLowerCase();
            const level = card.getAttribute("data-spell-level") || "";
            const matchesSearch = !searchQuery || name.includes(searchQuery);
            const matchesLevel = activeLevel === "all" || level === activeLevel;
            card.style.display = matchesSearch && matchesLevel ? "" : "none";
        });
        updateCollectionState(readySpellsList);
        updateCollectionState(managementSpellsList);
    }

    function setActiveButton(targetButton) {
        levelButtons.forEach((button) => {
            button.classList.toggle("is-active", button === targetButton);
        });
    }

    function destinationFor(card, ready) {
        const collection = ready ? readySpellsList : managementSpellsList;
        if (!collection) {
            return null;
        }
        const level = card.getAttribute("data-spell-level") || "";
        return Array.from(collection.querySelectorAll("[data-spell-level-list]"))
            .find((list) => list.getAttribute("data-spell-level-list") === level) || null;
    }

    function moveSpellCard(card, ready) {
        const destination = destinationFor(card, ready);
        if (!destination) {
            return;
        }

        // Move the existing node: Dice+ classes and every data-roll-* attribute stay intact.
        destination.appendChild(card);
        card.classList.toggle("ready-spell-item", ready);
        card.classList.toggle("management-spell-item", !ready);

        const checkbox = card.querySelector(".prepare-spell-checkbox");
        if (checkbox) {
            checkbox.checked = ready;
        }
        const text = card.querySelector(".prepare-spell-text");
        if (text) {
            text.textContent = ready ? "Remover preparo" : "Preparar";
        }
    }

    function snapshotSlotState() {
        const slotState = {};
        slotGroups.forEach((group) => {
            const level = group.getAttribute("data-slot-level") || "";
            slotState[level] = Array.from(group.querySelectorAll(".spell-slot-checkbox"))
                .map((checkbox) => checkbox.checked);
        });
        return slotState;
    }

    function applySlotState(slotState) {
        if (!slotState) {
            return;
        }
        slotGroups.forEach((group) => {
            const savedState = slotState[group.getAttribute("data-slot-level") || ""];
            if (!Array.isArray(savedState)) {
                return;
            }
            Array.from(group.querySelectorAll(".spell-slot-checkbox")).forEach((checkbox, index) => {
                checkbox.checked = Boolean(savedState[index]);
            });
        });
    }

    function readState() {
        if (!hasStorage) {
            return null;
        }
        try {
            const parsed = JSON.parse(window.localStorage.getItem(storageKey) || "null");
            if (!parsed || typeof parsed !== "object") {
                return null;
            }
            return {
                readyRefs: Array.isArray(parsed.readyRefs) ? parsed.readyRefs.filter(Boolean) : null,
                slotState: parsed.slotState && typeof parsed.slotState === "object" ? parsed.slotState : null,
            };
        } catch (error) {
            return null;
        }
    }

    function saveState() {
        if (!hasStorage) {
            return;
        }
        try {
            window.localStorage.setItem(storageKey, JSON.stringify({
                readyRefs: getReadyRefs(),
                slotState: snapshotSlotState(),
            }));
        } catch (error) {
            // Ignore storage failures (private mode, quota, etc.).
        }
    }

    function syncReadyState(readyRefs) {
        const readySet = new Set((readyRefs || []).filter(Boolean));
        getSpellCards().forEach((card) => {
            if (card.getAttribute("data-spell-can-prepare") !== "true") {
                return;
            }
            const ref = card.getAttribute("data-spell-ref");
            moveSpellCard(card, Boolean(ref && readySet.has(ref)));
        });
        updateReadyCounter();
        applyFilters();
        saveState();
    }

    if (searchInput) {
        searchInput.addEventListener("input", (event) => {
            searchQuery = event.target.value.trim().toLowerCase();
            applyFilters();
        });
    }

    levelButtons.forEach((button) => {
        button.addEventListener("click", () => {
            activeLevel = button.getAttribute("data-level-filter") || "all";
            setActiveButton(button);
            applyFilters();
        });
    });

    spellManager.addEventListener("change", (event) => {
        const checkbox = event.target.closest(".prepare-spell-checkbox");
        if (!checkbox) {
            return;
        }
        const card = checkbox.closest(".spell-card");
        if (!card) {
            return;
        }
        moveSpellCard(card, checkbox.checked);
        updateReadyCounter();
        applyFilters();
        saveState();
    });

    slotGroups.forEach((group) => group.addEventListener("change", saveState));

    const savedState = readState();
    if (savedState && Array.isArray(savedState.readyRefs)) {
        syncReadyState(savedState.readyRefs);
    } else {
        updateReadyCounter();
        applyFilters();
        saveState();
    }
    applySlotState(savedState ? savedState.slotState : null);
});
