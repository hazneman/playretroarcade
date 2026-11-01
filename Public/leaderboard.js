/* Shared leaderboard client for PlayRetroArcade.
   Server: functions/api/scores.js (stores nickname + score only).

   Usage at game over:
     ArcadeLB.offerSubmit('snake', score, overlayElement);

   Renders a top-5 list plus (when score >= 1) a nickname save row
   inside the host element. Replaces any previous box on re-call.
   Stays completely silent when the API is offline, so games keep
   working from file:// or before the KV binding exists. */
window.ArcadeLB = (function () {
  const esc = s => String(s).replace(/[&<>"']/g, c =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  async function getRows(game) {
    const r = await fetch('/api/scores?game=' + encodeURIComponent(game), { cache: 'no-store' });
    if (!r.ok) throw new Error('http ' + r.status);
    return r.json();
  }

  function fmtTime(ms) {
    const m = Math.floor(ms / 60000);
    const s = Math.floor((ms % 60000) / 1000);
    const cs = Math.floor((ms % 1000) / 10);
    return m + ':' + String(s).padStart(2, '0') + '.' + String(cs).padStart(2, '0');
  }

  function listHtml(rows, opts) {
    if (!rows.length) return '<div class="arc-lb-empty">no scores yet — be first!</div>';
    const show = v => (opts && opts.time) ? fmtTime(v) : v;
    return '<ol class="arc-lb-list">' + rows.slice(0, 5).map(r =>
      '<li><span>' + esc(r.name) + '</span><span>' + show(r.score) + '</span></li>').join('') + '</ol>';
  }

  async function offerSubmit(game, score, host, opts) {
    if (!host) return;
    const old = host.querySelector('.arc-lb-box');
    if (old) old.remove();

    let rows;
    try { rows = await getRows(game); } catch (e) { return; } // offline: say nothing

    const box = document.createElement('div');
    box.className = 'arc-lb-box';
    const canSubmit = Number.isInteger(score) && score >= 1;
    const title = (opts && opts.title) || '🏆 Top Scores';
    const saveLabel = (opts && opts.time) ? 'Save time' : 'Save score';
    box.innerHTML =
      '<div class="arc-lb-title">' + title + '</div>' + listHtml(rows, opts) +
      (canSubmit
        ? '<div class="arc-lb-row"><input class="arc-lb-name" maxlength="16" placeholder="nickname">' +
          '<button class="arc-lb-save">' + saveLabel + '</button></div><div class="arc-lb-msg"></div>'
        : '');
    host.appendChild(box);
    if (!canSubmit) return;

    const input = box.querySelector('.arc-lb-name');
    const msg = box.querySelector('.arc-lb-msg');
    input.value = localStorage.getItem('arcadeNickname') || '';
    // typing a nickname must never reach the game's key handlers
    // (e.g. R restarts Snake/Tetris)
    ['keydown', 'keyup', 'keypress'].forEach(ev =>
      input.addEventListener(ev, e => e.stopPropagation()));

    box.querySelector('.arc-lb-save').addEventListener('click', async () => {
      const name = input.value.trim();
      if (name.length < 2) { msg.textContent = 'Nickname needs at least 2 characters.'; return; }
      localStorage.setItem('arcadeNickname', name);
      msg.textContent = 'Saving…';
      try {
        const r = await fetch('/api/scores', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ game, name, score })
        });
        if (!r.ok) throw new Error('http ' + r.status);
        msg.textContent = '✅ Saved!';
        box.querySelector('.arc-lb-row').style.display = 'none';
        try {
          box.querySelector('.arc-lb-list, .arc-lb-empty').outerHTML = listHtml(await getRows(game), opts);
        } catch (e) { /* list refresh is best-effort */ }
      } catch (e) {
        msg.textContent = 'Could not reach the leaderboard.';
      }
    });
  }

  return { offerSubmit };
})();
