/* Ask EDUDESK: chat UI that calls POST /api/ask and shows labelled answer sections. */
const log = $("#chat-log"),
  askForm = $("#ask-form"),
  input = $("#ask-input"),
  sendButton = $("#ask-send");

function addMessage(role, html) {
  const row = document.createElement("div");
  row.className = `msg ${role}`;
  row.innerHTML = `<div class="bubble">${html}</div>`;
  log.appendChild(row);
  log.scrollTop = log.scrollHeight;
  return row;
}

const BADGE_CLASS = {
  general: "badge-general",
  database: "badge-db",
  official: "badge-official",
};

function renderLink(link) {
  const external = /^https?:\/\//i.test(link.url);
  return `<a class="btn btn-soft btn-sm" href="${esc(safeUrl(link.url))}" ${external ? 'target="_blank" rel="noopener noreferrer"' : ""}>${esc(link.label)}${external ? " ↗" : ""}</a>`;
}

function renderAnswer(data) {
  const sections = data.sections
    .map(
      (section) => `
    <div class="answer-section">
      <span class="badge ${BADGE_CLASS[section.kind] || "badge-general"}">${esc(section.label)}</span>
      <p>${esc(section.text)}</p>
      ${section.points && section.points.length ? `<ul>${section.points.map((p) => `<li>${esc(p)}</li>`).join("")}</ul>` : ""}
      ${
        section.items && section.items.length
          ? `<ul>${section.items
              .map(
                (item) =>
                  `<li><a href="${esc(safeUrl(item.url))}"><b>${esc(item.title)}</b></a> <span class="muted small">(${esc(item.type)} · ${esc(item.summary)})</span></li>`,
              )
              .join("")}</ul>`
          : ""
      }
      ${section.links && section.links.length ? `<div class="answer-links">${section.links.map(renderLink).join("")}</div>` : ""}
    </div>`,
    )
    .join("");
  return `${sections}<p class="disclaimer">${esc(data.disclaimer)}</p>`;
}

async function ask(question) {
  addMessage("user", esc(question));
  const thinking = addMessage("bot", '<span class="spinner"></span> Thinking…');
  sendButton.disabled = true;
  try {
    const data = await api("/api/ask", { method: "POST", body: { question } });
    thinking.querySelector(".bubble").innerHTML = renderAnswer(data);
    loadRecent();
  } catch (error) {
    thinking.querySelector(".bubble").innerHTML = `⚠️ ${esc(error.message)}`;
  } finally {
    sendButton.disabled = false;
    log.scrollTop = log.scrollHeight;
  }
}

async function loadRecent() {
  const list = $("#recent-questions");
  try {
    const data = await api("/api/questions/recent");
    list.innerHTML = data.items.length
      ? data.items
          .map(
            (q) =>
              `<li><button class="chip" data-q="${esc(q.text)}">${esc(q.text)}</button></li>`,
          )
          .join("")
      : '<li class="muted small">Your questions will appear here.</li>';
  } catch (error) {
    list.innerHTML = `<li class="muted small">${esc(error.message)}</li>`;
  }
}

askForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const question = input.value.trim();
  if (question.length < 3) {
    toast("Please type a longer question.", "error");
    return;
  }
  input.value = "";
  ask(question);
});
$("#ask-suggestions").addEventListener("click", (event) => {
  const chip = event.target.closest(".chip");
  if (chip) ask(chip.textContent.trim());
});
$("#recent-questions").addEventListener("click", (event) => {
  const chip = event.target.closest("[data-q]");
  if (chip) ask(chip.dataset.q);
});

loadRecent();
const preset = new URLSearchParams(location.search).get("q");
if (preset) ask(preset.slice(0, 500));
