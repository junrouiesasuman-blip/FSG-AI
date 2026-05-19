const signupForm = document.querySelector('#signupForm');
const loginForm = document.querySelector('#loginForm');
function formPayload(form){ return Object.fromEntries(new FormData(form).entries()); }
signupForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  try {
    const data = await api('/api/auth/signup', { method: 'POST', body: JSON.stringify(formPayload(signupForm)) });
    showSnack(data.message || 'Account successfully created.');
    setTimeout(() => location.href = '/login', 1400);
  } catch (error) { showSnack(error.message, 'error'); }
});
loginForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  try {
    await api('/api/auth/login', { method: 'POST', body: JSON.stringify(formPayload(loginForm)) });
    showSnack('Login successful.');
    setTimeout(() => location.href = '/dashboard', 700);
  } catch (error) { showSnack(error.message, 'error'); }
});
