const historyList = document.querySelector('#historyList');
function fmt(date){ return new Date(date).toLocaleString(); }
async function loadHistory(){
  try {
    const data = await api('/api/history');
    if (!data.history.length) { historyList.innerHTML = '<p class="muted">No analysis history yet.</p>'; return; }
    historyList.innerHTML = data.history.map(item => `
      <article class="history-card glass">
        <header><div><h3>Prediction: ${item.prediction}</h3><p>${fmt(item.created_at)} ${item.confidence == null ? '' : `• Confidence ${Math.round(item.confidence*100)}%`}</p></div><button class="btn btn-small ghost" data-delete="${item.id}">Delete</button></header>
        <details><summary>View input data</summary><pre>${JSON.stringify(item.input_data, null, 2)}</pre></details>
      </article>`).join('');
  } catch (error) { historyList.innerHTML = `<p class="muted">${error.message}</p>`; }
}
historyList?.addEventListener('click', async (event) => {
  const id = event.target.dataset.delete;
  if (!id) return;
  await api(`/api/history/${id}`, {method:'DELETE'});
  showSnack('History item deleted.');
  loadHistory();
});
loadHistory();
