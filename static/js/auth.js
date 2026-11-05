/* Login / Register page. Validates in the browser first, then calls the API. */
const root = $("#auth-root"),
  loginForm = $("#login-form"),
  registerForm = $("#register-form");
const nextUrl = root.dataset.next || "/dashboard";
const EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

function showTab(tab) {
  $$(".auth-tab").forEach((button) =>
    button.classList.toggle("active", button.dataset.tab === tab),
  );
  loginForm.hidden = tab !== "login";
  registerForm.hidden = tab !== "register";
}
$$(".auth-tab").forEach((button) =>
  button.addEventListener("click", () => showTab(button.dataset.tab)),
);
showTab(root.dataset.start || "login");

function showError(id, message) {
  const box = $(id);
  box.textContent = message;
  box.hidden = !message;
}

async function submitAuth(form, endpoint, errorId, payload) {
  const button = $("button[type=submit]", form);
  showError(errorId, "");
  setBusy(button, true);
  try {
    await api(endpoint, { method: "POST", body: payload });
    location.href =
      nextUrl.startsWith("/") && !nextUrl.startsWith("//")
        ? nextUrl
        : "/dashboard";
  } catch (error) {
    showError(errorId, error.message);
    setBusy(button, false);
  }
}

loginForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(loginForm).entries());
  if (!EMAIL.test(data.email.trim()))
    return showError("#login-error", "Enter a valid email address.");
  if (!data.password) return showError("#login-error", "Enter your password.");
  submitAuth(loginForm, "/api/login", "#login-error", {
    email: data.email.trim(),
    password: data.password,
  });
});

registerForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(registerForm).entries());
  if (data.name.trim().length < 2)
    return showError("#register-error", "Please enter your full name.");
  if (!EMAIL.test(data.email.trim()))
    return showError("#register-error", "Enter a valid email address.");
  if (data.password.length < 8)
    return showError(
      "#register-error",
      "Password must be at least 8 characters.",
    );
  if (!/[A-Za-z]/.test(data.password) || !/\d/.test(data.password))
    return showError(
      "#register-error",
      "Password needs at least one letter and one number.",
    );
  if (data.password !== data.confirm)
    return showError("#register-error", "Passwords do not match.");
  submitAuth(registerForm, "/api/register", "#register-error", {
    name: data.name.trim(),
    email: data.email.trim(),
    password: data.password,
  });
});
