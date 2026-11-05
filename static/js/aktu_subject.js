/* AKTU subject page: units as accordions with syllabus, notes, questions (with hints) and progress tracking. */
const root = $("#subject-root"),
  body = $("#subject-body"),
  subjectCode = root.dataset.code;
const DONE_KEY = "edudesk_aktu_done";
let subject = null;
const KIND_LABEL = { short: "Short", long: "Long", numerical: "Numerical" };

/* ---------- progress saved in this browser only ---------- */
function readDone() {
  try {
    return JSON.parse(localStorage.getItem(DONE_KEY) || "{}");
  } catch (error) {
    return {};
  }
}
function isDone(number) {
  return (readDone()[subject.code] || []).includes(number);
}
function setDone(number, done) {
  const all = readDone(),
    list = new Set(all[subject.code] || []);
  done ? list.add(number) : list.delete(number);
  all[subject.code] = [...list];
  try {
    localStorage.setItem(DONE_KEY, JSON.stringify(all));
  } catch (error) {
    toast("Could not save progress in this browser.", "error");
  }
}
function updateProgress() {
  const done = (readDone()[subject.code] || []).length,
    total = subject.units.length;
  $("#progress-fill").style.width = `${Math.round((done / total) * 100)}%`;
  $("#progress-text").textContent = `${done} of ${total} units marked done`;
  $$(".unit").forEach((el) =>
    el.classList.toggle("done", isDone(Number(el.dataset.number))),
  );
}

/* ---------- rendering ---------- */
function renderNotes(notes) {
  return notes
    .map((block) => {
      const lines = block.points.map((point) =>
        point.startsWith("CODE:")
          ? `<pre class="code-line">${esc(point.slice(5).trim())}</pre>`
          : `<li>${esc(point)}</li>`,
      );
      const code = lines.filter((l) => l.startsWith("<pre")).join(""),
        items = lines.filter((l) => l.startsWith("<li")).join("");
      return `<div class="note-block"><h4>${esc(block.heading)}</h4>${items ? `<ul>${items}</ul>` : ""}${code}</div>`;
    })
    .join("");
}

function renderQuestions(questions) {
  const groups = ["short", "long", "numerical"]
    .map((kind) => [kind, questions.filter((q) => q.kind === kind)])
    .filter(([, list]) => list.length);
  return groups
    .map(
      ([
        kind,
        list,
      ]) => `<div class="q-group"><h4>${esc(KIND_LABEL[kind])} questions (${list.length})</h4><ul class="q-list">
    ${list
      .map(
        (
          q,
        ) => `<li class="q-item"><span class="q-kind ${esc(kind)}">${esc(KIND_LABEL[kind])}</span>${esc(q.text)}
      ${q.hint ? `<button class="hint-btn" type="button">Show hint</button><div class="hint" hidden>${esc(q.hint)}</div>` : ""}</li>`,
      )
      .join("")}
  </ul></div>`,
    )
    .join("");
}

function renderUnit(unit) {
  const hours = unit.hours ? ` · ${esc(unit.hours)} hrs` : "";
  return `<details class="unit" data-number="${unit.number}">
    <summary><span class="unit-number">${unit.number}</span><span><div class="unit-title">${esc(unit.title)}</div><div class="unit-sub">${unit.questions.length} questions${hours}</div></span></summary>
    <div class="unit-body">
      <h4>Syllabus topics</h4><div class="syllabus-box">${esc(unit.syllabus)}</div>
      ${renderNotes(unit.notes)}
      ${renderQuestions(unit.questions)}
      <label class="unit-done"><input type="checkbox" data-done ${isDone(unit.number) ? "checked" : ""}> Mark this unit as done</label>
    </div></details>`;
}

function renderPapers(papers) {
  if (!papers || !papers.length) return "";
  return `<h3 style="margin-top:28px">Previous year papers</h3><ul class="ref-list">${papers
    .map(
      (p) =>
        `<li><a href="${esc(safeUrl(p.official_url))}" target="_blank" rel="noopener noreferrer">${esc(p.title)}</a>
      <span class="muted small">${[p.exam_session, p.paper_type].filter(Boolean).map(esc).join(" · ")}</span></li>`,
    )
    .join("")}</ul>
    <p class="muted small">Links open the original source. Always verify on the official AKTU website.</p>`;
}

function renderLabs(labs) {
  if (!labs || !labs.length) return "";
  return `<h3 style="margin-top:28px">Lab syllabus</h3>${labs
    .map(
      (
        lab,
      ) => `<div class="lab-card"><b>${esc(lab.code)}</b> — ${esc(lab.title)}
    ${lab.items && lab.items.length ? `<ul class="ref-list">${lab.items.map((item) => `<li>${esc(item)}</li>`).join("")}</ul>` : ""}</div>`,
    )
    .join("")}`;
}

function renderSubject(data) {
  subject = data;
  const codes = data.alt_code ? `${data.code} / ${data.alt_code}` : data.code;
  document.title = `${data.name} (${codes}) · EDUDESK`;
  $("#subject-title").textContent = data.name;
  $("#subject-meta").innerHTML =
    `<span class="tag">${esc(codes)}</span><span class="tag">${esc(data.category)}</span><span class="tag">${esc(data.credits)} credits</span><span class="tag">L-T-P ${esc(data.ltp)}</span>`;
  $("#subject-objective").textContent = data.objective || "";
  $("#subject-note").innerHTML = data.syllabus_note
    ? `<div class="notice warn"><b>About this unit list:</b> ${esc(data.syllabus_note)}</div>`
    : `<div class="notice">Unit titles, hours and topic lists follow the official AKTU first-year syllabus (session 2022-23). Check <a href="https://aktu.ac.in" target="_blank" rel="noopener noreferrer">aktu.ac.in</a> for any later change.</div>`;
  body.innerHTML = `
    <div class="card progress-card"><div class="mini-progress"><i id="progress-fill"></i></div><span id="progress-text" class="progress-label"></span></div>
    <div class="subject-toolbar">
      <div class="search-bar"><input id="unit-search" type="search" placeholder="Search inside this subject…" aria-label="Search inside this subject" autocomplete="off"></div>
      <button class="btn btn-ghost btn-sm" id="expand-all" type="button">Expand all</button>
      <button class="btn btn-ghost btn-sm" id="collapse-all" type="button">Collapse all</button>
      <button class="btn btn-ghost btn-sm" id="print-page" type="button">Print / Save PDF</button>
      <a class="btn btn-soft btn-sm" href="/ask?q=${encodeURIComponent("Explain " + data.name + " topics")}">Ask EDUDESK</a>
      ${helpButton(data.name + " (AKTU)")}
    </div>
    <p id="unit-empty" class="muted" hidden>No unit matches your search.</p>
    ${data.units.map(renderUnit).join("")}
    ${data.books && data.books.length ? `<h3 style="margin-top:28px">Suggested reference books</h3><ul class="ref-list">${data.books.map((b) => `<li>${esc(b)}</li>`).join("")}</ul>` : ""}
    ${renderPapers(data.papers)}
    ${renderLabs(data.labs)}
    <p class="muted small" style="margin-top:24px">Notes and questions are original EDUDESK revision material, not AKTU past papers. Verify the syllabus on the official AKTU website.</p>`;
  updateProgress();
  bindEvents();
  const unitParam = Number(new URLSearchParams(location.search).get("unit"));
  if (unitParam) {
    const el = $(`.unit[data-number="${unitParam}"]`);
    if (el) {
      el.open = true;
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }
}

/* ---------- search inside the subject ---------- */
function filterUnits(query) {
  const words = query.toLowerCase().split(/\s+/).filter(Boolean);
  let visible = 0;
  $$(".unit").forEach((el) => {
    const unit = subject.units.find(
      (u) => u.number === Number(el.dataset.number),
    );
    const text = [
      unit.title,
      unit.syllabus,
      ...unit.notes.flatMap((n) => [n.heading, ...n.points]),
      ...unit.questions.flatMap((q) => [q.text, q.hint]),
    ]
      .join(" ")
      .toLowerCase();
    const match = words.every((w) => text.includes(w));
    el.hidden = !match;
    if (match) {
      visible++;
      if (words.length) el.open = true;
    }
  });
  $("#unit-empty").hidden = visible > 0;
}

function bindEvents() {
  $("#unit-search").addEventListener(
    "input",
    debounce((event) => filterUnits(event.target.value.trim()), 200),
  );
  $("#expand-all").addEventListener("click", () =>
    $$(".unit").forEach((el) => {
      el.open = true;
    }),
  );
  $("#collapse-all").addEventListener("click", () =>
    $$(".unit").forEach((el) => {
      el.open = false;
    }),
  );
  $("#print-page").addEventListener("click", () => {
    $$(".unit").forEach((el) => {
      el.open = true;
    });
    $$(".hint").forEach((el) => {
      el.hidden = false;
    });
    window.print();
  });
  body.addEventListener("click", (event) => {
    const hintButton = event.target.closest(".hint-btn");
    if (!hintButton) return;
    const hint = hintButton.nextElementSibling;
    hint.hidden = !hint.hidden;
    hintButton.textContent = hint.hidden ? "Show hint" : "Hide hint";
  });
  body.addEventListener("change", (event) => {
    const box = event.target.closest("[data-done]");
    if (!box) return;
    setDone(Number(box.closest(".unit").dataset.number), box.checked);
    updateProgress();
    toast(
      box.checked ? "Unit marked as done." : "Unit marked as not done.",
      "success",
    );
  });
}

(async function init() {
  try {
    renderSubject(
      await api(`/api/aktu/subjects/${encodeURIComponent(subjectCode)}`),
    );
  } catch (error) {
    body.innerHTML = errorState(error.message);
  }
})();
