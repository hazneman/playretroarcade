/* Bug-report button for PlayRetroArcade.
   Include this script on any page: it injects a small fixed 🐞 button
   (bottom-right) that opens a tiny report form. Reports POST to
   /api/feedback (page + message only — no personal data). */
(function () {
  if (document.getElementById('arcFbBtn')) return;

  const btn = document.createElement('button');
  btn.id = 'arcFbBtn';
  btn.className = 'arc-fb-btn';
  btn.title = 'Report a bug';
  btn.textContent = '🐞';
  document.body.appendChild(btn);

  const wrap = document.createElement('div');
  wrap.className = 'arc-fb-overlay';
  wrap.style.display = 'none';
  wrap.innerHTML =
    '<div class="arc-fb-card">' +
    '  <div class="arc-fb-title">🐞 Report a bug</div>' +
    '  <div class="arc-fb-sub">What went wrong on this page? (no personal data is sent)</div>' +
    '  <textarea class="arc-fb-text" maxlength="300" rows="4" placeholder="e.g. the ball got stuck after level 2..."></textarea>' +
    '  <div class="arc-fb-row">' +
    '    <button class="arc-fb-send">Send</button>' +
    '    <button class="arc-fb-cancel">Cancel</button>' +
    '  </div>' +
    '  <div class="arc-fb-msg"></div>' +
    '</div>';
  document.body.appendChild(wrap);

  const text = wrap.querySelector('.arc-fb-text');
  const msg = wrap.querySelector('.arc-fb-msg');

  // typing must never reach game key handlers
  ['keydown', 'keyup', 'keypress'].forEach(ev =>
    text.addEventListener(ev, e => e.stopPropagation()));

  function open() { wrap.style.display = 'flex'; msg.textContent = ''; text.focus(); }
  function close() { wrap.style.display = 'none'; text.value = ''; }

  btn.addEventListener('click', open);
  wrap.querySelector('.arc-fb-cancel').addEventListener('click', close);
  wrap.addEventListener('click', e => { if (e.target === wrap) close(); });

  wrap.querySelector('.arc-fb-send').addEventListener('click', async () => {
    const message = text.value.trim();
    if (message.length < 5) { msg.textContent = 'Please describe the problem (at least 5 characters).'; return; }
    msg.textContent = 'Sending…';
    try {
      const r = await fetch('/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ page: location.pathname, message })
      });
      if (!r.ok) throw new Error('http ' + r.status);
      msg.textContent = '✅ Thank you! Your report is in.';
      text.value = '';
      setTimeout(close, 1400);
    } catch (e) {
      msg.textContent = 'Could not send right now — please try again later.';
    }
  });
})();
