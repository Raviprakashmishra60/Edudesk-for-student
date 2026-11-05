/* Exam Center: category chips, search, details modal. */
const grid = $("#exam-grid"),
  countLabel = $("#exam-count"),
  searchInput = $("#exam-search");
let currentCategory = "";
const examCache = new Map();

function examCard(exam) {
  return `<article class="card item-card">
    <div class="card-top"><span class="tag">${esc(exam.category)}</span>${demoBadge(exam.is_demo)}</div>
    <h3 class="card-title">${esc(exam.name)}</h3>
    <p class="card-desc">${esc(exam.description)}</p>
    <div class="card-meta"><span><b>Eligibility:</b> ${esc(exam.eligibility)}</span><span><b>Dates:</b> ${esc(exam.important_dates)}</span></div>
    <div class="card-actions"><button class="btn btn-primary btn-sm" data-view="${exam.id}">View Details</button>${officialLink(exam.official_url, "Website")}</div>
  </article>`;
}

async function loadExams() {
  showSkeletons(grid);
  const params = new URLSearchParams();
  if (currentCategory) params.set("category", currentCategory);
  if (searchInput.value.trim()) params.set("q", searchInput.value.trim());
  try {
    const data = await api(`/api/exams?${params}`);
    data.items.forEach((exam) => examCache.set(exam.id, exam));
    countLabel.textContent = data.count
      ? `${data.count} exam${data.count === 1 ? "" : "s"} found (demo data)`
      : "";
    grid.innerHTML = data.count
      ? data.items.map(examCard).join("")
      : emptyState(
          "No exams found",
          "Try another name or choose All categories.",
          '<button class="btn btn-primary btn-sm" id="empty-reset">Show all exams</button>',
        );
    $("#empty-reset")?.addEventListener("click", () => {
      currentCategory = "";
      searchInput.value = "";
      updateChips();
      loadExams();
    });
  } catch (error) {
    grid.innerHTML = errorState(error.message);
    countLabel.textContent = "";
  }
}
function updateChips() {
  $$("#exam-chips .chip").forEach((chip) =>
    chip.classList.toggle("active", chip.dataset.category === currentCategory),
  );
}

async function showExam(id) {
  let exam = examCache.get(id);
  if (!exam) {
    try {
      exam = await api(`/api/exams/${id}`);
    } catch (error) {
      return toast(error.message, "error");
    }
  }
  const body = openModal(
    exam.name,
    `
    <div class="tags"><span class="tag">${esc(exam.category)}</span>${demoBadge(exam.is_demo)}</div>
    <p style="margin-top:12px">${esc(exam.description)}</p>
    ${textBlock("Eligibility", exam.eligibility)}
    ${textBlock("Registration process", exam.registration_process)}
    ${listBlock("Documents usually needed", exam.documents)}
    ${textBlock("Important dates", exam.important_dates)}
    <p class="muted small" style="margin-top:14px">${esc(DEMO_NOTE)} Exam dates are not listed on purpose — they change every year.</p>
    <div class="modal-actions">${officialLink(exam.official_url, "Official website")}
      <button class="btn btn-soft btn-sm" id="e-track">+ Track this</button>
      <a class="btn btn-soft btn-sm" href="/documents">Prepare photo &amp; signature</a>${helpButton(exam.name + " form")}</div>`,
  );
  $("#e-track", body).addEventListener("click", () =>
    addToTracker(`${exam.name} application`, "Entrance Exams"),
  );
}

grid.addEventListener("click", (event) => {
  const view = event.target.closest("[data-view]");
  if (view) showExam(Number(view.dataset.view));
});
$("#exam-chips").addEventListener("click", (event) => {
  const chip = event.target.closest(".chip");
  if (!chip) return;
  currentCategory = chip.dataset.category;
  updateChips();
  loadExams();
});
searchInput.addEventListener("input", debounce(loadExams, 250));
(async function init() {
  await loadExams();
  openFromUrl(showExam);
})();
