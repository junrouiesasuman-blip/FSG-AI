const form = document.querySelector('#analysisForm');
const predictionText = document.querySelector('#predictionText');
const confidenceText = document.querySelector('#confidenceText');
const probabilities = document.querySelector('#probabilities');
function pct(value){ return `${Math.round((value || 0) * 100)}%`; }
form?.addEventListener('submit', async (event) => {
  event.preventDefault();
  predictionText.textContent = 'Analyzing...';
  confidenceText.textContent = 'The trained model is processing your inputs.';
  probabilities.innerHTML = '';
  try {
    const payload = Object.fromEntries([...new FormData(form).entries()].map(([k,v]) => [k, Number(v)]));
    const data = await api('/api/analyze', { method: 'POST', body: JSON.stringify(payload) });
    predictionText.textContent = data.prediction;
    confidenceText.textContent = data.confidence == null ? 'Prediction complete.' : `Confidence: ${pct(data.confidence)}`;
    if (data.probabilities) {
      probabilities.innerHTML = Object.entries(data.probabilities).map(([label, score]) => `
        <div class="prob-row"><div class="prob-top"><b>${label}</b><span>${pct(score)}</span></div><div class="bar"><i style="width:${pct(score)}"></i></div></div>
      `).join('');
    }
    showSnack('Analysis saved to history.');
  } catch (error) {
    predictionText.textContent = 'Error';
    confidenceText.textContent = error.message;
    showSnack(error.message, 'error');
  }
});
