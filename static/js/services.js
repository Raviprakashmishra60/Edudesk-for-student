/* Services page: search, category filter, details modal, save, track, WhatsApp help. */
const grid = $("#service-grid"),
  countLabel = $("#service-count"),
  searchInput = $("#service-search");
let currentCategory =
  new URLSearchParams(location.search).get("category") || "";
let servicesCache = new Map();

function serviceCard(service) {
  const saved = savedServices.has(service.id);
  return `<article class="card item-card">
    <div class="card-top"><span class="tag">${esc(service.category)}</span>${demoBadge(service.is_demo)}</div>
    <h3 class="card-title">${esc(service.title)}</h3>
    <p class="card-desc">${esc(service.description)}</p>
    <div class="card-actions">
      <button class="btn btn-primary btn-sm" data-view="${service.id}">View Details</button>
      <button class="save-btn ${saved ? "saved" : ""}" data-save="${service.id}" aria-label="Save service" aria-pressed="${saved}">${saved ? "♥" : "♡"}</button>
      ${helpButton(service.title)}
    </div></article>`;
}

async function loadServices() {
  showSkeletons(grid);
  const params = new URLSearchParams();
  if (currentCategory) params.set("category", currentCategory);
  if (searchInput.value.trim()) params.set("q", searchInput.value.trim());
  try {
    const data = await api(`/api/services?${params}`);
    data.items.forEach((service) => servicesCache.set(service.id, service));
    if (!data.items.length) {
      grid.innerHTML = emptyState(
        "No services found",
        "Try different words (for example “scholarship” or “admission”) or clear the category.",
        '<button class="btn btn-primary btn-sm" id="clear-filters">Clear filters</button>',
      );
      countLabel.textContent = "";
      $("#clear-filters").addEventListener("click", resetFilters);
      return;
    }
    countLabel.textContent =
      data.exact || !searchInput.value.trim()
        ? `${data.count} service${data.count === 1 ? "" : "s"} found`
        : `No exact match — showing ${data.count} related service${data.count === 1 ? "" : "s"}`;
    grid.innerHTML = data.items.map(serviceCard).join("");
  } catch (error) {
    grid.innerHTML = errorState(error.message);
  }
}

function resetFilters() {
  currentCategory = "";
  searchInput.value = "";
  updateChips();
  loadServices();
}
function updateChips() {
  $$("#category-chips .chip").forEach((chip) =>
    chip.classList.toggle("active", chip.dataset.category === currentCategory),
  );
}

async function showService(id) {
  let service = servicesCache.get(id);
  if (!service) {
    try {
      service = await api(`/api/services/${id}`);
    } catch (error) {
      return toast(error.message, "error");
    }
  }
  const body = openModal(
    service.title,
    `
    <div class="tags"><span class="tag">${esc(service.category)}</span>${demoBadge(service.is_demo)}</div>
    <p style="margin-top:12px">${esc(service.description)}</p>
    ${textBlock("Eligibility", service.eligibility)}
    ${listBlock("Required documents", service.documents)}
    ${stepsBlock("Application steps", service.steps)}
    ${textBlock("Important dates", service.important_dates)}
    <p class="muted small" style="margin-top:14px">${esc(DEMO_NOTE)}</p>
    <div class="modal-actions">
      ${officialLink(service.official_url)}
      <button class="btn btn-soft btn-sm" id="m-track">+ Track this</button>
      <button class="btn btn-soft btn-sm" id="m-save">${savedServices.has(service.id) ? "Remove from saved" : "♡ Save"}</button>
      ${helpButton(service.title)}
    </div>`,
  );
  $("#m-track", body).addEventListener("click", () =>
    addToTracker(service.title, service.category),
  );
  $("#m-save", body).addEventListener("click", async (event) => {
    await toggleSaved(service.id, null);
    event.target.textContent = savedServices.has(service.id)
      ? "Remove from saved"
      : "♡ Save";
    loadServices();
  });
}

grid.addEventListener("click", (event) => {
  const view = event.target.closest("[data-view]"),
    save = event.target.closest("[data-save]");
  if (view) showService(Number(view.dataset.view));
  if (save) toggleSaved(Number(save.dataset.save), save);
});
$("#category-chips").addEventListener("click", (event) => {
  const chip = event.target.closest(".chip");
  if (!chip) return;
  currentCategory = chip.dataset.category;
  updateChips();
  loadServices();
});
searchInput.addEventListener("input", debounce(loadServices, 250));
$("#service-search-clear").addEventListener("click", () => {
  searchInput.value = "";
  loadServices();
  searchInput.focus();
});

(async function init() {
  searchInput.value = new URLSearchParams(location.search).get("q") || "";
  updateChips();
  await loadSavedServices();
  await loadServices();
  openFromUrl(showService);
})();
