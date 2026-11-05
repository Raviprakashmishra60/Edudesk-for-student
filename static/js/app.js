/* EDUDESK - shared helpers used on every page.
   Pages load this file first, then their own file (services.js, dashboard.js ...). */

const STATES = [
  "Andhra Pradesh",
  "Arunachal Pradesh",
  "Assam",
  "Bihar",
  "Chhattisgarh",
  "Goa",
  "Gujarat",
  "Haryana",
  "Himachal Pradesh",
  "Jharkhand",
  "Karnataka",
  "Kerala",
  "Madhya Pradesh",
  "Maharashtra",
  "Manipur",
  "Meghalaya",
  "Mizoram",
  "Nagaland",
  "Odisha",
  "Punjab",
  "Rajasthan",
  "Sikkim",
  "Tamil Nadu",
  "Telangana",
  "Tripura",
  "Uttar Pradesh",
  "Uttarakhand",
  "West Bengal",
  "Andaman and Nicobar Islands",
  "Chandigarh",
  "Dadra and Nagar Haveli and Daman and Diu",
  "Delhi",
  "Jammu and Kashmir",
  "Ladakh",
  "Lakshadweep",
  "Puducherry",
];

const DEMO_NOTE = "Demo data — verify on the official website.";
const WHATSAPP = document.body.dataset.whatsapp || "918604551960";

/* ---------- tiny DOM helpers ---------- */
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

/* Escape text before putting it into HTML. ALWAYS use esc() for data that came from the server or the user. */
function esc(value) {
  return String(value ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
}

function debounce(fn, wait = 250) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), wait);
  };
}

/* Only allow http(s) or site-relative links (protects against javascript: URLs). */
function safeUrl(url) {
  return /^(https?:\/\/|\/)/i.test(url || "") ? url : "#";
}

/* ---------- API helper: always returns JSON or throws an Error with a readable message ---------- */
async function api(path, options = {}) {
  const init = {
    method: options.method || "GET",
    credentials: "same-origin",
    headers: { "X-Requested-With": "EDUDESK" },
  };
  if (options.body !== undefined) {
    init.headers["Content-Type"] = "application/json";
    init.body = JSON.stringify(options.body);
  }
  let response;
  try {
    response = await fetch(path, init);
  } catch (networkError) {
    throw new Error(
      "Cannot reach the server. Please check that EDUDESK is running and try again.",
    );
  }
  let data = null;
  try {
    data = await response.json();
  } catch (parseError) {
    /* empty body */
  }
  if (!response.ok) {
    const error = new Error(
      (data && data.error) || `Request failed (${response.status}).`,
    );
    error.status = response.status;
    throw error;
  }
  return data;
}

/* ---------- toast messages ---------- */
function toast(message, type = "") {
  const root = $("#toast-root");
  if (!root) return;
  const item = document.createElement("div");
  item.className = `toast ${type}`;
  item.setAttribute("role", type === "error" ? "alert" : "status");
  item.textContent = message;
  root.appendChild(item);
  setTimeout(() => item.remove(), 4200);
}

/* ---------- modal windows ---------- */
let activeModal = null;
function closeModal() {
  if (!activeModal) return;
  activeModal.overlay.remove();
  document.body.style.overflow = "";
  activeModal.previousFocus?.focus?.();
  activeModal = null;
}
function openModal(title, bodyHtml) {
  closeModal();
  const overlay = document.createElement("div");
  overlay.className = "modal-overlay";
  overlay.innerHTML = `<div class="modal" role="dialog" aria-modal="true" aria-label="${esc(title)}">
      <div class="modal-head"><h3>${esc(title)}</h3><button class="icon-btn" data-close aria-label="Close">✕</button></div>
      <div class="modal-body">${bodyHtml}</div></div>`;
  overlay.addEventListener("click", (event) => {
    if (event.target === overlay || event.target.closest("[data-close]"))
      closeModal();
  });
  document.body.appendChild(overlay);
  document.body.style.overflow = "hidden";
  activeModal = { overlay, previousFocus: document.activeElement };
  $("[data-close]", overlay).focus();
  return $(".modal-body", overlay);
}
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeModal();
});
/* "Try again" buttons (inline onclick is blocked by our Content-Security-Policy, so we listen here) */
document.addEventListener("click", (event) => {
  if (event.target.closest("[data-reload]")) location.reload();
});

/* ---------- WhatsApp help (pre-filled message) ---------- */
function whatsappUrl(topic) {
  const text = `Hello EDUDESK, I need help with ${topic}.`;
  return `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(text)}`;
}
function helpButton(topic, extraClass = "") {
  return `<a class="btn btn-wa btn-sm ${extraClass}" href="${esc(whatsappUrl(topic))}" target="_blank" rel="noopener">Need Help?</a>`;
}

/* ---------- reusable UI pieces ---------- */
function showSkeletons(container, count = 6) {
  container.innerHTML = Array.from(
    { length: count },
    () => '<div class="skeleton"></div>',
  ).join("");
}
function emptyState(title, message, actionHtml = "") {
  return `<div class="empty-state"><div class="empty-icon">🔍</div><h3>${esc(title)}</h3><p>${esc(message)}</p>${actionHtml}</div>`;
}
function errorState(message) {
  return `<div class="empty-state"><div class="empty-icon">⚠️</div><h3>Something went wrong</h3><p>${esc(message)}</p>
    <button class="btn btn-primary btn-sm" data-reload>Try again</button></div>`;
}
function listBlock(title, items) {
  if (!items || !items.length) return "";
  return `<h4>${esc(title)}</h4><ul>${items.map((item) => `<li>${esc(item)}</li>`).join("")}</ul>`;
}
function stepsBlock(title, items) {
  if (!items || !items.length) return "";
  return `<h4>${esc(title)}</h4><ol>${items.map((item) => `<li>${esc(item)}</li>`).join("")}</ol>`;
}
function textBlock(title, text) {
  return text ? `<h4>${esc(title)}</h4><p>${esc(text)}</p>` : "";
}
function officialLink(url, label = "Official website") {
  return url
    ? `<a class="btn btn-outline btn-sm" href="${esc(safeUrl(url))}" target="_blank" rel="noopener noreferrer">${esc(label)} ↗</a>`
    : "";
}
function demoBadge(isDemo) {
  return isDemo
    ? '<span class="badge badge-demo" title="Demo data — verify on the official website.">Demo data</span>'
    : "";
}
function formatDate(isoDate) {
  const date = new Date(`${isoDate}T00:00:00`);
  return isNaN(date)
    ? isoDate
    : date.toLocaleDateString("en-IN", {
        day: "numeric",
        month: "short",
        year: "numeric",
      });
}
function setBusy(button, busy, busyText = "Please wait…") {
  if (!button) return;
  if (busy) {
    button.dataset.label = button.innerHTML;
    button.innerHTML = `<span class="spinner"></span> ${busyText}`;
    button.disabled = true;
  } else {
    button.innerHTML = button.dataset.label || button.innerHTML;
    button.disabled = false;
  }
}
function fillSelect(select, values) {
  if (!select) return;
  values.forEach((value) =>
    select.insertAdjacentHTML(
      "beforeend",
      `<option value="${esc(value)}">${esc(value)}</option>`,
    ),
  );
}
/* Opens a card automatically when the URL has ?open=<id> (used by Ask EDUDESK links). */
function openFromUrl(openFn) {
  const id = new URLSearchParams(location.search).get("open");
  if (id && /^\d+$/.test(id)) openFn(Number(id));
}

/* ---------- saved services (works for guests and logged-in users) ---------- */
const savedServices = new Set();
async function loadSavedServices() {
  try {
    (await api("/api/saved")).service_ids.forEach((id) =>
      savedServices.add(id),
    );
  } catch (error) {
    /* not critical */
  }
}
async function toggleSaved(serviceId, button) {
  const wasSaved = savedServices.has(serviceId);
  try {
    if (wasSaved) {
      await api(`/api/saved/${serviceId}`, { method: "DELETE" });
      savedServices.delete(serviceId);
    } else {
      await api("/api/saved", {
        method: "POST",
        body: { service_id: serviceId },
      });
      savedServices.add(serviceId);
    }
    if (button) {
      button.classList.toggle("saved", !wasSaved);
      button.setAttribute("aria-pressed", String(!wasSaved));
      button.textContent = !wasSaved ? "♥" : "♡";
    }
    toast(
      wasSaved ? "Removed from saved services." : "Saved to your dashboard.",
      "success",
    );
  } catch (error) {
    toast(error.message, "error");
  }
}

/* ---------- "Add to tracker" from any page ---------- */
async function addToTracker(title, category) {
  try {
    const user = document.body.dataset.user;
    const body = {
      title,
      category,
      status: "Not Started",
      student_name: user || "Student",
    };
    await api("/api/applications", { method: "POST", body });
    toast("Added to your application tracker.", "success");
  } catch (error) {
    toast(error.message, "error");
  }
}

/* ---------- navigation + floating help button ---------- */
document.addEventListener("DOMContentLoaded", () => {
  const toggle = $("#nav-toggle"),
    nav = $("#main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
  }
  const floatHelp = $("#float-help");
  if (floatHelp) floatHelp.href = whatsappUrl("EDUDESK student services");
  $$("select[data-states]").forEach((select) => fillSelect(select, STATES));
});
