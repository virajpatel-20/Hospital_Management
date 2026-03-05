const API = "http://127.0.0.1:5000";

// ========== USER SESSION ==========
function getUser() {
  try { return JSON.parse(localStorage.getItem("hms_user") || "null"); }
  catch { return null; }
}

function setUser(user) {
  localStorage.setItem("hms_user", JSON.stringify(user));
}

function logout() {
  localStorage.removeItem("hms_user");
  window.location.href = "../login.html";
}

function requireAuth(role = null) {
  const user = getUser();
  if (!user) {
    window.location.href = "../login.html";
    return null;
  }
  if (role && user.role !== role) {
    alert("Access denied. You do not have permission to view this page.");
    window.location.href = "../login.html";
    return null;
  }
  return user;
}

function requireAuthRoot(role = null) {
  const user = getUser();
  if (!user) {
    window.location.href = "login.html";
    return null;
  }
  if (role && user.role !== role) {
    alert("Access denied.");
    window.location.href = "login.html";
    return null;
  }
  return user;
}

// ========== API HELPERS ==========
async function apiPost(endpoint, data) {
  const res = await fetch(`${API}${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  const json = await res.json();
  return { ok: res.ok, data: json, status: res.status };
}

async function apiGet(endpoint) {
  const res = await fetch(`${API}${endpoint}`);
  const json = await res.json();
  return { ok: res.ok, data: json, status: res.status };
}

async function apiPut(endpoint, data = {}) {
  const res = await fetch(`${API}${endpoint}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  const json = await res.json();
  return { ok: res.ok, data: json, status: res.status };
}

async function apiDelete(endpoint) {
  const res = await fetch(`${API}${endpoint}`, { method: "DELETE" });
  const json = await res.json();
  return { ok: res.ok, data: json, status: res.status };
}

// ========== TOAST NOTIFICATIONS ==========
function showToast(message, type = "info", title = null) {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  const icons = { success: "✅", error: "❌", info: "ℹ️", warning: "⚠️" };
  const titles = { success: "Success", error: "Error", info: "Info", warning: "Warning" };

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${icons[type] || icons.info}</span>
    <div class="toast-content">
      <div class="toast-title">${title || titles[type]}</div>
      <div class="toast-msg">${message}</div>
    </div>
    <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
  `;

  container.appendChild(toast);
  setTimeout(() => { if (toast.parentElement) toast.remove(); }, 4500);
}

// ========== ALERT HELPERS ==========
function showAlert(id, message, type = "error") {
  const el = document.getElementById(id);
  if (!el) return;
  el.className = `alert alert-${type}`;
  el.textContent = message;
  el.classList.remove("hidden");
  el.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function hideAlert(id) {
  const el = document.getElementById(id);
  if (el) el.classList.add("hidden");
}

// ========== STATUS BADGE ==========
function statusBadge(status) {
  const map = {
    "Pending": "badge-pending",
    "Approved": "badge-approved",
    "Completed": "badge-completed",
    "Cancelled": "badge-cancelled"
  };
  return `<span class="badge ${map[status] || 'badge-pending'}">${status}</span>`;
}

function roleBadge(role) {
  return `<span class="badge badge-${role}">${role}</span>`;
}

// ========== DATE/TIME HELPERS ==========
function formatDate(dateStr) {
  if (!dateStr) return "—";
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" });
}

function formatTime(timeStr) {
  if (!timeStr) return "—";
  const [h, m] = timeStr.split(":");
  const hour = parseInt(h);
  const ampm = hour >= 12 ? "PM" : "AM";
  const hour12 = hour % 12 || 12;
  return `${hour12}:${m} ${ampm}`;
}

function getInitials(name) {
  if (!name) return "?";
  return name.split(" ").map(n => n[0]).join("").toUpperCase().slice(0, 2);
}

// ========== MODAL HELPERS ==========
function openModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.add("open");
}

function closeModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.remove("open");
}

// Close modal on backdrop click
document.addEventListener("click", (e) => {
  if (e.target.classList.contains("modal-backdrop")) {
    e.target.classList.remove("open");
  }
});

// ========== SIDEBAR ACTIVE LINK ==========
function setActiveSidebarLink() {
  const current = window.location.pathname.split("/").pop();
  document.querySelectorAll(".sidebar-nav a").forEach(a => {
    const href = a.getAttribute("href");
    if (href && href.includes(current)) {
      a.classList.add("active");
    }
  });
}

// ========== RENDER SIDEBAR USER INFO ==========
function renderSidebarUser(user) {
  const nameEl = document.getElementById("sidebar-user-name");
  const roleEl = document.getElementById("sidebar-user-role");
  const avatarEl = document.getElementById("sidebar-user-avatar");
  if (nameEl) nameEl.textContent = user.name;
  if (roleEl) roleEl.textContent = user.role;
  if (avatarEl) avatarEl.textContent = getInitials(user.name);
}

document.addEventListener("DOMContentLoaded", () => {
  setActiveSidebarLink();
});
