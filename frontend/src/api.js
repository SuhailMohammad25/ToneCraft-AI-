const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  (typeof window !== 'undefined' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1'
    ? '/backend'
    : 'http://localhost:8000');

const CASES_STORAGE_KEY = 'tonecraft-ai-cases';

function readLocalCases() {
  if (typeof window === 'undefined') {
    return [];
  }

  try {
    const raw = window.localStorage.getItem(CASES_STORAGE_KEY);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function writeLocalCases(cases) {
  if (typeof window === 'undefined') {
    return;
  }
  window.localStorage.setItem(CASES_STORAGE_KEY, JSON.stringify(cases));
}

function createLocalCase(payload) {
  return {
    ...payload,
    id: Date.now(),
    created_at: new Date().toISOString(),
  };
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let message = 'Request failed';
    try {
      const payload = await response.json();
      message = payload.detail || message;
    } catch {
      message = response.statusText || message;
    }
    throw new Error(Array.isArray(message) ? message.map((item) => item.msg).join(', ') : message);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export function analyzeMessage(payload) {
  return request('/api/analyze', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function saveCase(payload) {
  const localCase = createLocalCase(payload);
  const current = readLocalCases();
  writeLocalCases([localCase, ...current]);

  request('/api/cases', {
    method: 'POST',
    body: JSON.stringify(payload),
  }).catch(() => null);

  return Promise.resolve(localCase);
}

export function getCases() {
  return Promise.resolve(readLocalCases());
}

export function deleteCase(caseId) {
  const nextCases = readLocalCases().filter((item) => item.id !== caseId);
  writeLocalCases(nextCases);

  request(`/api/cases/${caseId}`, {
    method: 'DELETE',
  }).catch(() => null);

  return Promise.resolve(null);
}
