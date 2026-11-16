/* Shared learner state and renewable browser authentication. */
const STORAGE_KEY = "athena_v1_state";
const ACCESS_KEY = "athena_access_token";
let memoryAccessToken = null;
let renewal = null;
// Entitlement overrides are enforced by the backend. Never make the browser
// an independent source of truth for a development or production paywall.
const ATHENA_UNLOCK_ALL_LESSONS = false;

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const stored = JSON.parse(raw);
      return {
        user: stored.user?.email ? stored.user : null,
        accessToken: stored.accessToken || null,
        isPremium: Boolean(stored.isPremium),
        completedLessons: Array.isArray(stored.completedLessons) ? stored.completedLessons : [],
        quizAttempts: stored.quizAttempts || {}
      };
    }
  } catch (e) { /* corrupt or blocked storage — fall back to defaults */ }
  return {
    user: null,
    accessToken: null,
    isPremium: false,
    completedLessons: [],
    quizAttempts: {}
  };
}
function saveState(state) {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
  catch (e) { console.warn("Athena: could not persist state", e); }
}

const AthenaState = {
  get() { return loadState(); },
  isLessonComplete(lessonId) { return this.get().completedLessons.includes(lessonId); },

  /* Gating rule required by the product brief: a learner must pass a
     lesson's quiz before the NEXT lesson in that topic unlocks. The
     first lesson in a topic is always unlocked. */
  isLessonUnlocked(topic, lessonId) {
    if (ATHENA_UNLOCK_ALL_LESSONS) return true;
    const idx = topic.lessons.findIndex(l => l.id === lessonId);
    if (idx <= 0) return true;
    return this.isLessonComplete(topic.lessons[idx - 1].id);
  },

  hasLessonAccess(lesson) {
    return ATHENA_UNLOCK_ALL_LESSONS || lesson.free || this.get().isPremium;
  },

  recordQuizAttempt(lessonId, score, passed) {
    const state = this.get();
    if (!state.quizAttempts[lessonId]) state.quizAttempts[lessonId] = [];
    state.quizAttempts[lessonId].push({ score, passed, date: new Date().toISOString() });
    if (passed && !state.completedLessons.includes(lessonId)) state.completedLessons.push(lessonId);
    saveState(state);
    return state;
  },

  topicProgress(topic) {
    const total = topic.lessons.length;
    const done = topic.lessons.filter(l => this.isLessonComplete(l.id)).length;
    return total === 0 ? 0 : done / total;
  },

  setUser(partial) {
    const state = this.get();
    state.user = { ...(state.user || {}), ...partial };
    saveState(state);
    return state;
  },

  setSession(session) {
    const state = this.get();
    const user = session.user;
    if (state.user?.email && state.user.email !== user.email) {
      state.completedLessons = [];
      state.quizAttempts = {};
    }
    state.user = {
      firstName: user.first_name,
      email: user.email,
      grade: user.grade,
      mode: user.curriculum_mode,
      role: user.role,
      isPremium: user.is_premium
    };
    memoryAccessToken = session.access_token;
    try { sessionStorage.setItem(ACCESS_KEY, session.access_token); } catch (_) {}
    state.accessToken = null; // Long-lived browser credentials remain HttpOnly.
    state.isPremium = user.is_premium;
    saveState(state);
    return state;
  },

  accessToken() {
    if (memoryAccessToken) return memoryAccessToken;
    try { if (sessionStorage.getItem(ACCESS_KEY)) return sessionStorage.getItem(ACCESS_KEY); } catch (_) {}
    return this.get().accessToken || null; // One-time compatibility with existing sessions.
  },

  clearSession() {
    memoryAccessToken = null;
    try { sessionStorage.removeItem(ACCESS_KEY); } catch (_) {}
    saveState({ user: null, accessToken: null, isPremium: false,
      completedLessons: [], quizAttempts: {} });
  },

  reset() { localStorage.removeItem(STORAGE_KEY); }
};

const AthenaAuth = {
  async signup({ firstName, email, password, grade, mode }) {
    const session = await this.request("/api/v1/auth/signup", {
      method: "POST",
      body: JSON.stringify({
        first_name: firstName,
        email,
        password,
        grade,
        curriculum_mode: mode
      })
    });
    AthenaState.setSession(session);
    return session.user;
  },

  async login({ email, password, rememberMe = false }) {
    const session = await this.request("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password, remember_me: rememberMe })
    });
    AthenaState.setSession(session);
    return session.user;
  },

  async renewSession() {
    if (!renewal) renewal = (async () => {
      const response = await fetch("/api/v1/auth/refresh", { method: "POST", credentials: "same-origin" });
      if (response.status === 401) { AthenaState.clearSession(); return null; }
      if (!response.ok) { const error = new Error("We couldn't reconnect. Your sign-in has been kept. Please retry."); error.status = response.status; throw error; }
      const session = await response.json();
      AthenaState.setSession(session);
      return session.user;
    })().finally(() => { renewal = null; });
    return renewal;
  },

  async fetch(path, options = {}) {
    const local = new URL(path, location.href);
    if (local.origin !== location.origin) throw new Error("Account requests must stay on Athena.");
    if (!AthenaState.accessToken() && AthenaState.get().user) await this.renewSession();
    const send = () => fetch(path, { ...options, credentials: "same-origin", headers: {
      ...(AthenaState.accessToken() ? { Authorization: `Bearer ${AthenaState.accessToken()}` } : {}),
      ...(options.headers || {})
    }});
    let response = await send();
    if (response.status === 401 && !/\/(login|signup|refresh|logout|providers)$/.test(local.pathname)) {
      const user = await this.renewSession();
      if (user) {
        const headers = {...(options.headers || {}), Authorization: `Bearer ${AthenaState.accessToken()}`};
        response = await fetch(path, {...options, credentials:"same-origin", headers});
      }
    }
    return response;
  },

  async restoreSession() {
    if (!AthenaState.accessToken()) return this.renewSession();
    try {
      const user = await this.request("/api/v1/auth/me");
      AthenaState.setSession({ access_token: AthenaState.accessToken(), user });
      return user;
    } catch (error) {
      if (error.status === 401) { AthenaState.clearSession(); return null; }
      throw error; // A network/server failure is not a sign-out.
    }
  },

  safeNext(value) {
    if (!value || !value.startsWith("/") || value.startsWith("//") || value.includes("\\") || /[\u0000-\u001f]/.test(value)) return "/dashboard.html";
    const target = new URL(value, location.origin);
    return target.origin === location.origin ? target.pathname + target.search + target.hash : "/dashboard.html";
  },

  async requireSession() {
    try {
      const user = await this.restoreSession();
      if (!user) location.href = `login.html?next=${encodeURIComponent(location.pathname + location.search)}`;
      return user;
    } catch (error) {
      const main = document.querySelector("main");
      if (main) {
        const notice = document.createElement("p"); notice.className = "card"; notice.setAttribute("role", "alert");
        notice.textContent = "We couldn't reconnect. Your sign-in has been kept. Refresh this page to try again.";
        main.prepend(notice);
      }
      return null;
    }
  },

  async updateProfile(changes) {
    const token = AthenaState.accessToken();
    if (!token) throw new Error("Please sign in again.");
    const user = await this.request("/api/v1/auth/me", {
      method: "PATCH",
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify(changes)
    });
    AthenaState.setSession({ access_token: token, user });
    return user;
  },

  async logout() {
    await this.request("/api/v1/auth/logout", {method:"POST"});
    AthenaState.clearSession();
    location.href = "login.html";
  },

  async request(path, options = {}) {
    const response = await (/(login|signup|logout|providers)$/.test(path) ? fetch : this.fetch.bind(this))(path, {
      credentials: "same-origin",
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {})
      }
    });
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      const error = new Error(typeof payload.detail === "string" ? payload.detail : "Check your details and try again.");
      error.status = response.status;
      throw error;
    }
    return response.json();
  }
};


window.addEventListener("storage", event => {
  if (event.key !== STORAGE_KEY) return;
  let previous, current;
  try { previous=JSON.parse(event.oldValue || "null"); current=JSON.parse(event.newValue || "null"); } catch (_) {}
  if (!current?.user || previous?.user?.email !== current.user.email) {
    memoryAccessToken = null;
    try { sessionStorage.removeItem(ACCESS_KEY); } catch (_) {}
    // Another tab signed out or changed account; never send that tab's old bearer.
  }
});
