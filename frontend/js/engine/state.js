/* ============================================================
   STATE — mock auth + progress store (Phase 1 only)
   ------------------------------------------------------------
   Stands in for the real backend session + progress API (see
   backend/app/api/v1/auth.py and backend/app/db/models/progress.py).
   Kept in localStorage under one namespaced key. When the
   backend exists, only this file's internals change — its
   public shape (AthenaState.*) should stay the same so pages
   don't need to be rewritten.
   ============================================================ */
const STORAGE_KEY = "athena_v1_state";
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
    state.accessToken = session.access_token;
    state.isPremium = user.is_premium;
    saveState(state);
    return state;
  },

  accessToken() { return this.get().accessToken || null; },

  clearSession() {
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

  async login({ email, password }) {
    const session = await this.request("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password })
    });
    AthenaState.setSession(session);
    return session.user;
  },

  async restoreSession() {
    const token = AthenaState.accessToken();
    if (!token) return null;
    try {
      const user = await this.request("/api/v1/auth/me", {
        headers: { Authorization: `Bearer ${token}` }
      });
      AthenaState.setSession({ access_token: token, user });
      return user;
    } catch (error) {
      AthenaState.clearSession();
      return null;
    }
  },

  async requireSession() {
    const user = await this.restoreSession();
    if (!user) {
      location.href = `login.html?next=${encodeURIComponent(location.pathname + location.search)}`;
      return null;
    }
    return user;
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

  logout() {
    AthenaState.clearSession();
    location.href = "login.html";
  },

  async request(path, options = {}) {
    const response = await fetch(path, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {})
      }
    });
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      throw new Error(payload.detail || "Something went wrong. Please try again.");
    }
    return response.json();
  }
};
