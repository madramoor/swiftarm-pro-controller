(() => {
  "use strict";

  // ===== Config =====
  const API_BASE = "http://localhost:5000/api";
  const POLL_MS = 500;

  // Expected API (typical shape; adjust endpoints if your backend differs):
  // GET  /status  -> { connected: bool, position:{x,y,z}, gripper:{open:bool}|string, pump:{on:bool}|string, estop:{active:bool} }
  // POST /move    -> { ok:true } body: { x, y, z, speed }
  // POST /gripper -> { ok:true } body: { action:"open"|"close"|"toggle" }
  // POST /pump    -> { ok:true } body: { action:"on"|"off"|"toggle" }
  // POST /estop   -> { ok:true } body: { action:"engage"|"reset" }

  // ===== DOM =====
  const el = {
    connDot: document.getElementById("connDot"),
    connText: document.getElementById("connText"),
    apiBaseText: document.getElementById("apiBaseText"),

    posX: document.getElementById("posX"),
    posY: document.getElementById("posY"),
    posZ: document.getElementById("posZ"),
    lastUpdate: document.getElementById("lastUpdate"),
    robotName: document.getElementById("robotName"),
    gripperState: document.getElementById("gripperState"),
    pumpState: document.getElementById("pumpState"),

    xInput: document.getElementById("xInput"),
    yInput: document.getElementById("yInput"),
    zInput: document.getElementById("zInput"),
    xErr: document.getElementById("xErr"),
    yErr: document.getElementById("yErr"),
    zErr: document.getElementById("zErr"),

    speedSlider: document.getElementById("speedSlider"),
    speedOut: document.getElementById("speedOut"),

    moveForm: document.getElementById("moveForm"),
    moveBtn: document.getElementById("moveBtn"),
    fillFromCurrentBtn: document.getElementById("fillFromCurrentBtn"),

    gripperToggleBtn: document.getElementById("gripperToggleBtn"),
    pumpToggleBtn: document.getElementById("pumpToggleBtn"),

    eStopBtn: document.getElementById("eStopBtn"),
    resetEStopBtn: document.getElementById("resetEStopBtn"),
    estopState: document.getElementById("estopState"),

    msgRegion: document.getElementById("msgRegion"),
    lastError: document.getElementById("lastError"),

    themeToggle: document.getElementById("themeToggle"),
  };

  el.apiBaseText.textContent = API_BASE;

  // ===== State =====
  const state = {
    connected: false,
    lastStatus: null,
    lastError: null,
    polling: false,
    currentPos: { x: null, y: null, z: null },
    gripperPressed: false,
    pumpPressed: false,
    theme: null,
  };

  // ===== Utilities =====
  const clamp = (n, min, max) => Math.min(max, Math.max(min, n));
  const nowTime = () => new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });

  function setMessage(text, kind = "info") {
    // Keep it simple + accessible via aria-live region
    el.msgRegion.textContent = text;

    // Subtle semantic styling via border glow (no color requirement, but helpful)
    el.msgRegion.dataset.kind = kind;
  }

  function setLastError(text) {
    state.lastError = text || null;
    el.lastError.textContent = text || "—";
  }

  function setConnected(isConnected) {
    state.connected = !!isConnected;

    el.connDot.classList.toggle("dot--connected", state.connected);
    el.connDot.classList.toggle("dot--disconnected", !state.connected);

    el.connText.textContent = state.connected ? "Connected" : "Disconnected";
    el.connText.style.color = state.connected ? "var(--text)" : "var(--muted)";

    // Disable controls when disconnected (except theme + e-stop which may still be attempted)
    el.moveBtn.disabled = !state.connected || !isFormValid(false);
    el.gripperToggleBtn.disabled = !state.connected;
    el.pumpToggleBtn.disabled = !state.connected;
    el.fillFromCurrentBtn.disabled = !state.connected;

    // Reset pressed states when disconnected (avoid misleading toggles)
    if (!state.connected) {
      el.gripperToggleBtn.setAttribute("aria-pressed", "false");
      el.pumpToggleBtn.setAttribute("aria-pressed", "false");
    }
  }

  function fmtNum(v) {
    if (v === null || v === undefined || Number.isNaN(v)) return "—";
    // tabular-ish presentation without forcing decimals
    const n = Number(v);
    return Number.isFinite(n) ? (Math.round(n * 10) / 10).toString() : "—";
  }

  // ===== Validation =====
  const ranges = {
    x: { min: 50, max: 320 },
    y: { min: -200, max: 200 },
    z: { min: 0, max: 150 },
    speed: { min: 1, max: 2000 }
  };

  function validateField(inputEl, errEl, min, max, name) {
    const raw = inputEl.value.trim();
    if (raw.length === 0) {
      errEl.textContent = `${name} is required.`;
      inputEl.setAttribute("aria-invalid", "true");
      return { ok: false, value: null };
    }
    const val = Number(raw);
    if (!Number.isFinite(val)) {
      errEl.textContent = `${name} must be a number.`;
      inputEl.setAttribute("aria-invalid", "true");
      return { ok: false, value: null };
    }
    if (val < min || val > max) {
      errEl.textContent = `${name} must be between ${min} and ${max}.`;
      inputEl.setAttribute("aria-invalid", "true");
      return { ok: false, value: null };
    }
    errEl.textContent = "";
    inputEl.removeAttribute("aria-invalid");
    return { ok: true, value: val };
  }

  function isFormValid(updateUI = true) {
    const vx = validateField(el.xInput, el.xErr, ranges.x.min, ranges.x.max, "X");
    const vy = validateField(el.yInput, el.yErr, ranges.y.min, ranges.y.max, "Y");
    const vz = validateField(el.zInput, el.zErr, ranges.z.min, ranges.z.max, "Z");

    const ok = vx.ok && vy.ok && vz.ok;
    if (!updateUI) return ok;
    return ok;
  }

  function refreshMoveButtonState() {
    el.moveBtn.disabled = !state.connected || !isFormValid(true);
  }

  // ===== Fetch wrapper (timeout + errors) =====
  async function apiFetch(path, options = {}) {
    const url = `${API_BASE}${path}`;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 2000); // keep snappy; polling is frequent

    try {
      const res = await fetch(url, {
        ...options,
        headers: {
          "Content-Type": "application/json",
          ...(options.headers || {})
        },
        signal: controller.signal
      });

      const contentType = res.headers.get("content-type") || "";
      let body = null;

      if (contentType.includes("application/json")) {
        body = await res.json().catch(() => null);
      } else {
        body = await res.text().catch(() => null);
      }

      if (!res.ok) {
        const msg = (body && body.error) ? body.error : `HTTP ${res.status} ${res.statusText}`;
        throw new Error(msg);
      }

      return body;
    } catch (err) {
      throw err;
    } finally {
      clearTimeout(timeout);
    }
  }

  // ===== Polling =====
  async function pollStatusOnce() {
    const data = await apiFetch("/status", { method: "GET" });
    return data;
  }

  function applyStatus(status) {
    state.lastStatus = status;

    // Connection inference:
    // - prefer explicit boolean if provided; otherwise treat successful fetch as connected.
    const isConnected = typeof status?.connected === "boolean" ? status.connected : true;
    setConnected(isConnected);

    // Position
    const px = status?.position?.x ?? status?.x ?? null;
    const py = status?.position?.y ?? status?.y ?? null;
    const pz = status?.position?.z ?? status?.z ?? null;

    state.currentPos = { x: px, y: py, z: pz };

    el.posX.textContent = fmtNum(px);
    el.posY.textContent = fmtNum(py);
    el.posZ.textContent = fmtNum(pz);

    // Tool states (accept boolean objects or strings)
    const gr = status?.gripper;
    const pu = status?.pump;

    const grText =
      typeof gr === "string" ? gr :
      typeof gr?.open === "boolean" ? (gr.open ? "Open" : "Closed") :
      typeof gr?.state === "string" ? gr.state :
      "—";

    const puText =
      typeof pu === "string" ? pu :
      typeof pu?.on === "boolean" ? (pu.on ? "On" : "Off") :
      typeof pu?.state === "string" ? pu.state :
      "—";

    el.gripperState.textContent = grText;
    el.pumpState.textContent = puText;

    // E-stop state
    const es = status?.estop;
    const active =
      typeof es === "boolean" ? es :
      typeof es?.active === "boolean" ? es.active :
      typeof status?.estop_active === "boolean" ? status.estop_active :
      null;

    if (active === true) {
      el.estopState.textContent = "E-Stop: ACTIVE";
      el.estopState.classList.remove("pill--neutral", "pill--ok");
      el.estopState.classList.add("pill--bad");
    } else if (active === false) {
      el.estopState.textContent = "E-Stop: Ready";
      el.estopState.classList.remove("pill--neutral", "pill--bad");
      el.estopState.classList.add("pill--ok");
    } else {
      el.estopState.textContent = "E-Stop: Unknown";
      el.estopState.classList.remove("pill--ok", "pill--bad");
      el.estopState.classList.add("pill--neutral");
    }

    el.lastUpdate.textContent = nowTime();
    setLastError(null);
    refreshMoveButtonState();
  }

  async function startPolling() {
    if (state.polling) return;
    state.polling = true;

    while (state.polling) {
      try {
        const status = await pollStatusOnce();
        applyStatus(status);
      } catch (err) {
        // Poll failures => disconnected, but keep trying
        setConnected(false);
        const msg = err?.name === "AbortError" ? "Polling timed out." : (err?.message || "Polling error.");
        setLastError(msg);
        setMessage(`Disconnected: ${msg}`, "error");
        refreshMoveButtonState();
      }

      await new Promise(r => setTimeout(r, POLL_MS));
    }
  }

  function stopPolling() {
    state.polling = false;
  }

  // ===== Actions =====
  async function sendMove(x, y, z, speed) {
    // Clamp speed defensively
    const s = clamp(Number(speed), ranges.speed.min, ranges.speed.max);

    setMessage("Sending move command…");
    const body = { x, y, z, speed: s };

    const res = await apiFetch("/move", { method: "POST", body: JSON.stringify(body) });
    setMessage("Move command accepted.");
    return res;
  }

  async function toggleTool(path, label) {
    setMessage(`${label}: sending…`);
    const res = await apiFetch(path, { method: "POST", body: JSON.stringify({ action: "toggle" }) });
    setMessage(`${label}: command accepted.`);
    return res;
  }

  async function engageEStop() {
    // Keep deliberate: no confirmation modal (can block keyboard/screen reader users),
    // but require a long-press on pointer devices? We’ll keep it immediate per requirement.
    setMessage("Emergency stop: engaging…", "warn");
    const res = await apiFetch("/estop", { method: "POST", body: JSON.stringify({ action: "engage" }) });
    setMessage("Emergency stop engaged.", "warn");
    return res;
  }

  async function resetEStop() {
    setMessage("Resetting emergency stop…");
    const res = await apiFetch("/estop", { method: "POST", body: JSON.stringify({ action: "reset" }) });
    setMessage("Emergency stop reset.");
    return res;
  }

  // ===== Theme =====
  function getPreferredTheme() {
    const saved = localStorage.getItem("swiftarm_theme");
    if (saved === "dark" || saved === "light") return saved;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  }

  function applyTheme(theme) {
    state.theme = theme;
    document.documentElement.setAttribute("data-theme", theme);
    const pressed = theme === "light";
    el.themeToggle.setAttribute("aria-pressed", pressed ? "true" : "false");
    localStorage.setItem("swiftarm_theme", theme);
  }

  // ===== Wire up events =====
  function onInputChanged() {
    isFormValid(true);
    refreshMoveButtonState();
  }

  el.xInput.addEventListener("input", onInputChanged);
  el.yInput.addEventListener("input", onInputChanged);
  el.zInput.addEventListener("input", onInputChanged);

  el.speedOut.textContent = `${el.speedSlider.value} mm/min`;
  el.speedSlider.addEventListener("input", () => {
    el.speedOut.textContent = `${el.speedSlider.value} mm/min`;
  });

  el.moveForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!state.connected) {
      setMessage("Cannot move: not connected.", "error");
      return;
    }

    const vx = validateField(el.xInput, el.xErr, ranges.x.min, ranges.x.max, "X");
    const vy = validateField(el.yInput, el.yErr, ranges.y.min, ranges.y.max, "Y");
    const vz = validateField(el.zInput, el.zErr, ranges.z.min, ranges.z.max, "Z");

    if (!(vx.ok && vy.ok && vz.ok)) {
      setMessage("Fix validation errors before moving.", "error");
      refreshMoveButtonState();
      return;
    }

    try {
      el.moveBtn.disabled = true;
      await sendMove(vx.value, vy.value, vz.value, el.speedSlider.value);
    } catch (err) {
      const msg = err?.message || "Move failed.";
      setLastError(msg);
      setMessage(`Move failed: ${msg}`, "error");
      setConnected(false); // conservative: if commands fail, treat as disconnected until poll recovers
    } finally {
      refreshMoveButtonState();
    }
  });

  el.fillFromCurrentBtn.addEventListener("click", () => {
    if (!state.connected) return;
    const { x, y, z } = state.currentPos;
    if (x === null || y === null || z === null) {
      setMessage("Current position not available yet.", "error");
      return;
    }
    el.xInput.value = fmtNum(x);
    el.yInput.value = fmtNum(y);
    el.zInput.value = fmtNum(z);
    setMessage("Filled inputs with current position.");
    refreshMoveButtonState();
  });

  el.gripperToggleBtn.addEventListener("click", async () => {
    if (!state.connected) {
      setMessage("Cannot toggle gripper: not connected.", "error");
      return;
    }
    try {
      await toggleTool("/gripper", "Gripper");
    } catch (err) {
      const msg = err?.message || "Gripper command failed.";
      setLastError(msg);
      setMessage(`Gripper failed: ${msg}`, "error");
      setConnected(false);
    }
  });

  el.pumpToggleBtn.addEventListener("click", async () => {
    if (!state.connected) {
      setMessage("Cannot toggle pump: not connected.", "error");
      return;
    }
    try {
      await toggleTool("/pump", "Pump");
    } catch (err) {
      const msg = err?.message || "Pump command failed.";
      setLastError(msg);
      setMessage(`Pump failed: ${msg}`, "error");
      setConnected(false);
    }
  });

  el.eStopBtn.addEventListener("click", async () => {
    // Even if disconnected, attempt (could be local safety controller responding)
    try {
      await engageEStop();
    } catch (err) {
      const msg = err?.message || "E-Stop failed.";
      setLastError(msg);
      setMessage(`E-Stop failed: ${msg}`, "error");
      setConnected(false);
    }
  });

  el.resetEStopBtn.addEventListener("click", async () => {
    try {
      await resetEStop();
    } catch (err) {
      const msg = err?.message || "E-Stop reset failed.";
      setLastError(msg);
      setMessage(`Reset failed: ${msg}`, "error");
      setConnected(false);
    }
  });

  el.themeToggle.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme") || "dark";
    applyTheme(current === "dark" ? "light" : "dark");
  });

  // ===== Init =====
  applyTheme(getPreferredTheme());
  refreshMoveButtonState();
  setMessage("Starting status polling…");
  startPolling();

  // Stop polling when tab is hidden to reduce load, resume when visible
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      stopPolling();
    } else {
      setMessage("Resuming status polling…");
      startPolling();
    }
  });

  // Helpful: prevent accidental scroll on spacebar when focused on buttons
  window.addEventListener("keydown", (e) => {
    if (e.code === "Space" && document.activeElement && document.activeElement.tagName === "BUTTON") {
      // Let button activate, but avoid page scroll in some browsers
      e.preventDefault();
      document.activeElement.click();
    }
  }, { passive: false });
})();
