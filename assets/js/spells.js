document.addEventListener("DOMContentLoaded", () => {
    const spellManager = document.querySelector(".spell-manager");
    if (!spellManager) {
        return;
    }

    const searchInput = document.getElementById("spell-search");
    const preparedSpellsList = document.getElementById("prepared-spells-list");
    const classSpellsList = document.getElementById("class-spells-list");
    const levelButtons = Array.from(spellManager.querySelectorAll(".spell-level-filter"));

    let activeLevel = "all";
    let searchQuery = "";

    function getSpellCards() {
        return Array.from(spellManager.querySelectorAll(".spell-card"));
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
            const spellCard = checkbox.closest(".class-spell-item");
            if (!spellCard || !spellRef) {
                return;
            }

            if (checkbox.checked) {
                const existing = preparedSpellsList.querySelector(`[data-spell-ref="${spellRef}"]`);
                if (!existing) {
                    const msg = preparedSpellsList.querySelector(".no-prepared-msg");
                    if (msg) {
                        msg.remove();
                    }

                    const preparedCard = spellCard.cloneNode(true);
                    preparedCard.classList.remove("class-spell-item");
                    preparedCard.classList.add("prepared-spell-item");
                    preparedCard.style.borderLeftColor = "var(--accent-color)";
                    preparedCard.setAttribute("data-spell-ref", spellRef);

                    const checkboxContainer = preparedCard.querySelector(".prepare-spell-label");
                    if (checkboxContainer) {
                        checkboxContainer.outerHTML = `<span class="prepared-spell-badge"><i class="ra ra-health"></i> Preparada</span>`;
                    }

                    const details = preparedCard.querySelector(".spell-details-accordion");
                    if (details) {
                        details.removeAttribute("open");
                    }

                    preparedSpellsList.appendChild(preparedCard);
                }
            } else {
                const preparedCard = preparedSpellsList.querySelector(`[data-spell-ref="${spellRef}"]`);
                if (preparedCard) {
                    preparedCard.remove();
                }

                if (preparedSpellsList.querySelectorAll(".prepared-spell-item").length === 0) {
                    preparedSpellsList.innerHTML = `<p class="no-prepared-msg" style="color:var(--text-muted); font-style:italic;">Nenhuma magia preparada no momento.</p>`;
                }
            }

            applyFilters();
        });
    }

    applyFilters();
});
