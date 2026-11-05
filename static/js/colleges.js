/* College & Course Finder: search + filters from /api/meta, cards, details modal. */
const form = $("#college-filters"),
  grid = $("#college-grid"),
  countLabel = $("#college-count"),
  searchInput = $("#college-search");
const collegeCache = new Map();

function collegeCard(college) {
  return `<article class="card item-card">
    <div class="card-top"><span class="badge ${college.type === "Government" ? "badge-gov" : "badge-private"}">${esc(college.type)}</span>${demoBadge(college.is_demo)}</div>
    <h3 class="card-title">${esc(college.name)}</h3>
    <p class="card-desc">📍 ${esc(college.city)}, ${esc(college.state)}</p>
    <div class="tags">${(college.courses || []).map((c) => `<span class="tag">${esc(c)}</span>`).join("")}</div>
    <div class="card-meta">
      <span><b>Eligibility:</b> ${esc(college.eligibility)}</span>
      <span><b>Admission:</b> ${esc(college.admission_process)}</span>
    </div>
    <div class="card-actions">
      <button class="btn btn-primary btn-sm" data-view="${college.id}">View Details</button>
      ${officialLink(college.official_url, "Website")}
    </div></article>`;
}

async function loadColleges() {
  showSkeletons(grid);
  const params = new URLSearchParams(
    Object.fromEntries(
      [...new FormData(form).entries()].filter(([, value]) => value !== ""),
    ),
  );
  if (searchInput.value.trim()) params.set("q", searchInput.value.trim());
  try {
    const data = await api(`/api/colleges?${params}`);
    data.items.forEach((college) => collegeCache.set(college.id, college));
    countLabel.textContent = data.count
      ? `${data.count} college${data.count === 1 ? "" : "s"} found (demo data)`
      : "";
    grid.innerHTML = data.count
      ? data.items.map(collegeCard).join("")
      : emptyState(
          "No colleges found",
          "Try changing or removing a filter.",
          '<button class="btn btn-primary btn-sm" id="empty-reset">Reset filters</button>',
        );
    $("#empty-reset")?.addEventListener("click", resetAll);
  } catch (error) {
    grid.innerHTML = errorState(error.message);
    countLabel.textContent = "";
  }
}

function resetAll() {
  form.reset();
  searchInput.value = "";
  loadColleges();
}

async function showCollege(id) {
  let college = collegeCache.get(id);
  if (!college) {
    try {
      college = await api(`/api/colleges/${id}`);
    } catch (error) {
      return toast(error.message, "error");
    }
  }
  openModal(
    college.name,
    `
    <div class="tags"><span class="badge ${college.type === "Government" ? "badge-gov" : "badge-private"}">${esc(college.type)}</span>${demoBadge(college.is_demo)}</div>
    <p style="margin-top:12px">📍 ${esc(college.city)}, ${esc(college.state)}</p>
    ${listBlock("Courses (sample list)", college.courses)}
    ${listBlock("Entrance exams accepted", college.entrance_exams)}
    ${textBlock("Eligibility", college.eligibility)}
    ${textBlock("Admission process", college.admission_process)}
    ${textBlock("Fee band", `${college.fee_band} (indicative only — check the official fee structure)`)}
    <p class="muted small" style="margin-top:14px">${esc(DEMO_NOTE)}</p>
    <div class="modal-actions">${officialLink(college.official_url)}${helpButton(`admission at ${college.name}`)}</div>`,
  );
}

grid.addEventListener("click", (event) => {
  const view = event.target.closest("[data-view]");
  if (view) showCollege(Number(view.dataset.view));
});
form.addEventListener("change", loadColleges);
form.addEventListener("submit", (event) => event.preventDefault());
$("#college-reset").addEventListener("click", () => setTimeout(resetAll, 0));
searchInput.addEventListener("input", debounce(loadColleges, 250));

(async function init() {
  try {
    const meta = await api("/api/meta");
    fillSelect(form.elements.course, meta.college_courses);
    fillSelect(form.elements.state, meta.college_states);
    fillSelect(form.elements.city, meta.college_cities);
    fillSelect(form.elements.exam, meta.college_exams);
  } catch (error) {
    toast(error.message, "error");
  }
  await loadColleges();
  openFromUrl(showCollege);
})();
