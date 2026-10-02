/* Original finite models; native range inputs enforce the displayed domains. */
(() => {
  'use strict';
  const value = id => Number(document.getElementById(id).value);
  const percent = x => `${(100 * x).toFixed(2)}%`;
  function update() {
    for (const id of ['prevalence', 'sensitivity', 'false-positive',
      'success-probability', 'attempts', 'shared-fraction']) {
      document.getElementById(`${id}-value`).textContent = String(value(id));
    }
    const prevalence = value('prevalence') / 100;
    const truePositive = prevalence * value('sensitivity') / 100;
    const falsePositive = (1 - prevalence) * value('false-positive') / 100;
    const calls = truePositive + falsePositive;
    const precision = calls ? percent(truePositive / calls) : 'undefined (no positive calls)';
    document.getElementById('detector-result').textContent =
      `Precision: ${precision}. Expected counts per 10,000 windows: ${(10000 * truePositive).toFixed(1)} true positives, ${(10000 * falsePositive).toFixed(1)} false positives.`;
    const p = value('success-probability') / 100;
    const n = value('attempts');
    const q = value('shared-fraction') / 100;
    const independent = n === 0 || p === 0 ? 0 : p === 1 ? 1 : -Math.expm1(n * Math.log1p(-p));
    const mixed = n === 0 ? 0 : (1 - q) * independent + q * p;
    document.getElementById('portfolio-result').textContent =
      `At least one success: ${percent(mixed)} with the shared-outcome mixture; ${percent(independent)} with independence. These are stipulated-model probabilities.`;
  }
  document.querySelectorAll('#chapter-content input').forEach(input => input.addEventListener('input', update));
  update();
})();
