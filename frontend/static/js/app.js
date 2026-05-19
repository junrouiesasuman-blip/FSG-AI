const $ = (selector) => document.querySelector(selector);
const snackbar = $('#snackbar');
function showSnack(message, type = 'success') {
  if (!snackbar) return;
  snackbar.textContent = message;
  snackbar.classList.add('show');
  setTimeout(() => snackbar.classList.remove('show'), 2800);
}
async function api(path, options = {}) {
  const response = await fetch(path, { headers: { 'Content-Type': 'application/json', ...(options.headers || {}) }, ...options });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.message || 'Request failed');
  return data;
}
$('.nav-toggle')?.addEventListener('click', () => $('.nav-links')?.classList.toggle('open'));
(async function hydrateNav(){
  try {
    const me = await api('/api/me');
    document.querySelectorAll('[data-auth]').forEach(el => el.classList.toggle('hidden', !me.authenticated));
    document.querySelectorAll('[data-guest]').forEach(el => el.classList.toggle('hidden', me.authenticated));
  } catch {}
})();
$('#logoutBtn')?.addEventListener('click', async () => { await api('/api/auth/logout', {method:'POST'}); location.href = '/login'; });
