document.addEventListener("DOMContentLoaded", () => {
    const spellManager = document.querySelector(".spell-manager");
    if (!spellManager) {
        return;
    }

    const searchInput = document.getElementById("spell-search");
    const preparedSpellsList = document.getElementById("prepared-spells-list");
    const classSpellsList = document.getElementById("class-spells-list");
    const levelButtons = Array.from(spellManager.querySelectorAll(".spell-level-filter"));
    const slotGroups = Array.from(spellManager.querySelectorAll(".spell-slots-tracker .slot-level-group"));
    const preparedCounter = spellManager.querySelector('[data-spell-counter="prepared"] [data-spell-counter-value="prepared"]');
    const preparedLimitCounter = spellManager.querySelector('[data-spell-counter="prepared"] [data-spell-counter-limit="prepared"]');
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

    const basePreparedTemplates = new Map();
    const classSpellTemplates = new Map();

    function safeEscape(value) {
        if (window.CSS && typeof window.CSS.escape === "function") {
            return window.CSS.escape(value);
        }
        return String(value).replace(/\\/g, "\\\\").replace(/"/g, '\\"');
    }

    function getSpellCards() {
        return Array.from(spellManager.querySelectorAll(".spell-card"));
    }

    function getPreparedRefs() {
        if (!preparedSpellsList) {
            return [];
        }
        return Array.from(preparedSpellsList.querySelectorAll(".prepared-spell-item"))
            .map((card) => card.getAttribute("data-spell-ref"))
            .filter(Boolean);
    }

    function updatePreparedCounter() {
        if (!preparedCounter) {
            return;
        }
        preparedCounter.textContent = String(getPreparedRefs().length);
        if (preparedLimitCounter && preparedLimitCounter.textContent.trim() === "") {
            preparedLimitCounter.textContent = "0";
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
    }

    function setActiveButton(targetButton) {
        levelButtons.forEach((button) => {
            button.classList.toggle("is-active", button === targetButton);
        });
    }

    function snapshotPreparedTemplates() {
        if (preparedSpellsList) {
            preparedSpellsList.querySelectorAll(".prepared-spell-item").forEach((card) => {
                const ref = card.getAttribute("data-spell-ref");
                if (ref && !basePreparedTemplates.has(ref)) {
                    basePreparedTemplates.set(ref, card.cloneNode(true));
                }
            });
        }

        if (classSpellsList) {
            classSpellsList.querySelectorAll(".class-spell-item").forEach((card) => {
                const ref = card.getAttribute("data-spell-ref");
                if (ref && !classSpellTemplates.has(ref)) {
                    classSpellTemplates.set(ref, card.cloneNode(true));
                }
            });
        }
    }

    function getTemplateForSpell(ref) {
        return basePreparedTemplates.get(ref) || classSpellTemplates.get(ref) || null;
    }

    function buildPreparedCard(ref) {
        const template = getTemplateForSpell(ref);
        if (!template) {
            return null;
        }

        const preparedCard = template.cloneNode(true);
        preparedCard.classList.remove("class-spell-item");
        preparedCard.classList.add("prepared-spell-item");
        preparedCard.style.borderLeftColor = "var(--accent-color)";
        preparedCard.setAttribute("data-spell-ref", ref);

        const checkboxContainer = preparedCard.querySelector(".prepare-spell-label");
        if (checkboxContainer) {
            checkboxContainer.outerHTML = `<span class="prepared-spell-badge"><i class="ra ra-health"></i> Preparada</span>`;
        }

        const details = preparedCard.querySelector(".spell-details-accordion");
        if (details) {
            details.removeAttribute("open");
        }

        return preparedCard;
    }

    function syncClassCheckboxes(preparedRefs) {
        if (!classSpellsList) {
            return;
        }

        const preparedSet = new Set(preparedRefs);
        classSpellsList.querySelectorAll(".prepare-spell-checkbox").forEach((checkbox) => {
            const spellRef = checkbox.getAttribute("data-spell-ref");
            checkbox.checked = Boolean(spellRef && preparedSet.has(spellRef));
        });
    }

    function snapshotSlotState() {
        const slotState = {};

        slotGroups.forEach((group) => {
            const level = group.getAttribute("data-slot-level") || "";
            slotState[level] = Array.from(group.querySelectorAll(".spell-slot-checkbox")).map((checkbox) => checkbox.checked);
        });

        return slotState;
    }

    function applySlotState(slotState) {
        if (!slotState) {
            return;
        }

        slotGroups.forEach((group) => {
            const level = group.getAttribute("data-slot-level") || "";
            const savedState = slotState[level];
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
            const raw = window.localStorage.getItem(storageKey);
            if (!raw) {
                return null;
            }

            const parsed = JSON.parse(raw);
            if (!parsed || typeof parsed !== "object") {
                return null;
            }

            return {
                preparedRefs: Array.isArray(parsed.preparedRefs) ? parsed.preparedRefs.filter(Boolean) : null,
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
                preparedRefs: getPreparedRefs(),
                slotState: snapshotSlotState(),
            }));
        } catch (error) {
            // Ignore storage failures (private mode, quota, etc.).
        }
    }

    function renderPreparedList(preparedRefs) {
        if (!preparedSpellsList) {
            return;
        }

        const uniqueRefs = Array.from(new Set((preparedRefs || []).filter(Boolean)));
        const fragment = document.createDocumentFragment();

        uniqueRefs.forEach((ref) => {
            const card = buildPreparedCard(ref);
            if (card) {
                fragment.appendChild(card);
            }
        });

        preparedSpellsList.innerHTML = "";
        if (fragment.childNodes.length > 0) {
            preparedSpellsList.appendChild(fragment);
        } else {
            preparedSpellsList.innerHTML = `<p class="no-prepared-msg" style="color:var(--text-muted); font-style:italic;">Nenhuma magia preparada no momento.</p>`;
        }
    }

    function syncPreparedState(preparedRefs) {
        if (!preparedSpellsList) {
            return;
        }

        const currentRefs = Array.from(new Set((preparedRefs || []).filter(Boolean)));
        renderPreparedList(currentRefs);
        syncClassCheckboxes(currentRefs);
        updatePreparedCounter();
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

    if (classSpellsList && preparedSpellsList) {
        classSpellsList.addEventListener("change", (event) => {
            const checkbox = event.target.closest(".prepare-spell-checkbox");
            if (!checkbox) {
                return;
            }

            const spellRef = checkbox.getAttribute("data-spell-ref");
            if (!spellRef) {
                return;
            }

            const nextPreparedRefs = getPreparedRefs();
            const nextSet = new Set(nextPreparedRefs);

            if (checkbox.checked) {
                nextSet.add(spellRef);
            } else {
                nextSet.delete(spellRef);
            }

            syncPreparedState(Array.from(nextSet));
        });
    }

    slotGroups.forEach((group) => {
        group.addEventListener("change", saveState);
    });

    snapshotPreparedTemplates();

    const savedState = readState();
    const initialPreparedRefs = getPreparedRefs();
    const preparedRefs = savedState && Array.isArray(savedState.preparedRefs)
        ? savedState.preparedRefs
        : initialPreparedRefs;

    renderPreparedList(preparedRefs);
    syncClassCheckboxes(preparedRefs);
    applySlotState(savedState ? savedState.slotState : null);
    updatePreparedCounter();
    applyFilters();

    if (!savedState) {
        saveState();
    }
});
