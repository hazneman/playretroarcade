// Bug reports — Cloudflare Pages Function backed by the same KV namespace
// as the leaderboard (binding SCORES).
//
// POST {page, message}: public. Stores page path, message and a timestamp.
// No names, no emails, no IPs. Newest 200 reports are kept.
//
// GET ?key=...: returns the reports, but ONLY when the key matches the
// FEEDBACK_KEY environment variable (Pages project -> Settings ->
// Variables and secrets). Without that variable, reading is disabled.

const KV_KEY = 'feedback';
const MAX_REPORTS = 200;

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
  });
}

export async function onRequestPost({ request, env }) {
  if (!env.SCORES) return json({ error: 'not configured' }, 503);

  let body;
  try { body = await request.json(); } catch { return json({ error: 'bad json' }, 400); }

  const page = String(body.page || '').slice(0, 64).replace(/[^\w\s/.\-]/g, '');
  const message = String(body.message || '').trim().slice(0, 300);
  if (message.length < 5) return json({ error: 'message too short' }, 400);

  const rows = JSON.parse((await env.SCORES.get(KV_KEY)) || '[]');
  rows.unshift({ page, message, at: Date.now() });
  rows.length = Math.min(rows.length, MAX_REPORTS);
  await env.SCORES.put(KV_KEY, JSON.stringify(rows));
  return json({ ok: true });
}

export async function onRequestGet({ request, env }) {
  if (!env.SCORES) return json({ error: 'not configured' }, 503);
  if (!env.FEEDBACK_KEY) return json({ error: 'reading disabled: set FEEDBACK_KEY' }, 403);
  const key = new URL(request.url).searchParams.get('key');
  if (key !== env.FEEDBACK_KEY) return json({ error: 'wrong key' }, 403);
  return json(JSON.parse((await env.SCORES.get(KV_KEY)) || '[]'));
}
