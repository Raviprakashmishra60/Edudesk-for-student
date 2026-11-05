/* AKTU Study Hub - subject list: search, category chips, progress from this browser. */
const aktuGrid = $("#aktu-grid"),
  aktuCount = $("#aktu-count"),
  aktuSearch = $("#aktu-search"),
  aktuChips = $("#aktu-chips");
const DONE_KEY = "edudesk_aktu_done"; // {"BAS101": [1, 2], ...} saved only in this browser
let aktuCategory = "";
let categoriesBuilt = false;

function doneUnits(code) {
  try {
    return (JSON.parse(localStorage.getItem(DONE_KEY) || "{}")[code] || [])
      .length;
  } catch (error) {
    return 0;
  }
}

function matchingTitles(subject, query) {
  const words = query
    .toLowerCase()
    .split(/\s+/)
    .filter((w) => w.length > 2);
  if (!words.length) return [];
  return subject.unit_titles.filter((title) =>
    words.some((w) => title.toLowerCase().includes(w)),
  );
}

function subjectCard(subject, query) {
  const done = doneUnits(subject.code),
    percent = subject.unit_count
      ? Math.round((done / subject.unit_count) * 100)
      : 0;
  const codes = subject.alt_code
    ? `${subject.code} / ${subject.alt_code}`
    : subject.code;
  const matches = matchingTitles(subject, query);
  return `<article class="card item-card subject-card">
    <div class="card-top"><span class="code">${esc(codes)}</span><span class="tag">${esc(subject.category)}</span></div>
    <h3 class="card-title">${esc(subject.name)}</h3>
    <div class="stats"><span>${esc(subject.credits)} credits</span><span>L-T-P ${esc(subject.ltp)}</span><span>${esc(subject.unit_count)} units</span><span>${esc(subject.question_count)} questions</span></div>
    ${matches.length ? `<div class="match-titles">Matches: ${matches.map(esc).join(" · ")}</div>` : ""}
    <div><div class="mini-progress"><i style="width:${percent}%"></i></div><span class="progress-label">${done} of ${esc(subject.unit_count)} units marked done</span></div>
    <div class="card-actions"><a class="btn btn-primary btn-sm" href="/aktu/${encodeURIComponent(subject.code)}">Open notes</a>${helpButton(subject.name + " (AKTU)")}</div>
  </article>`;
}

function buildChips(items) {
  [...new Set(items.map((s) => s.category))].forEach((category) =>
    aktuChips.insertAdjacentHTML(
      "beforeend",
      `<button class="chip" data-category="${esc(category)}">${esc(category)}</button>`,
    ),
  );
  categoriesBuilt = true;
}

async function loadSubjects() {
  showSkeletons(aktuGrid, 6);
  const params = new URLSearchParams();
  const query = aktuSearch.value.trim();
  if (query) params.set("q", query);
  try {
    if (!categoriesBuilt) buildChips((await api("/api/aktu/subjects")).items);
    if (aktuCategory) params.set("category", aktuCategory);
    const data = await api(`/api/aktu/subjects?${params}`);
    aktuCount.textContent = data.count
      ? `${data.count} subject${data.count === 1 ? "" : "s"}`
      : "";
    aktuGrid.innerHTML = data.count
      ? data.items.map((s) => subjectCard(s, query)).join("")
      : emptyState(
          "No subject found",
          "Try a subject name (Physics, Maths, C programming) or a topic such as “Laplace”.",
          '<button class="btn btn-primary btn-sm" id="aktu-reset">Show all subjects</button>',
        );
    $("#aktu-reset")?.addEventListener("click", () => {
      aktuSearch.value = "";
      aktuCategory = "";
      syncChips();
      loadSubjects();
    });
  } catch (error) {
    aktuGrid.innerHTML = errorState(error.message);
    aktuCount.textContent = "";
  }
}
function syncChips() {
  $$("#aktu-chips .chip").forEach((chip) =>
    chip.classList.toggle("active", chip.dataset.category === aktuCategory),
  );
}

aktuChips.addEventListener("click", (event) => {
  const chip = event.target.closest(".chip");
  if (!chip) return;
  aktuCategory = chip.dataset.category;
  syncChips();
  loadSubjects();
});
aktuSearch.addEventListener("input", debounce(loadSubjects, 250));
$("#aktu-search-clear").addEventListener("click", () => {
  aktuSearch.value = "";
  loadSubjects();
  aktuSearch.focus();
});
loadSubjects();
