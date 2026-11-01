// Shared arcade leaderboard — Cloudflare Pages Function backed by Workers KV.
//
// Privacy: stores ONLY a self-chosen nickname and a score. No accounts,
// no emails, no IPs, no tracking.
//
// Setup (one time, Cloudflare dashboard):
//   Workers & Pages -> playretroarcade -> Settings -> Bindings ->
//   Add binding -> KV namespace -> Variable name: SCORES -> create/pick a
//   namespace. Until then every request returns 503 and the games fall
//   back to device-local best scores.

const GAMES = new Set([
  'brickbreaker', 'snake', 'tetris', 'spaceinvaders',
  'basketball', 'neonmaze', 'skysea', 'battleship',
  'racecar', // value = best lap in milliseconds
  '2048', 'darkroom',
]);
// games where the stored value is a time: lower is better
const LOWER_IS_BETTER = new Set(['racecar']);
const MAX_ROWS = 50;

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
  });
}

function cleanName(raw) {
  const name = String(raw || '').trim().replace(/\s+/g, ' ').slice(0, 16);
  // letters (incl. Turkish), digits, space and a few safe symbols
  if (!/^[\p{L}\p{N} _.\-]{2,16}$/u.test(name)) return null;
  return name;
}

export async function onRequestGet({ request, env }) {
  if (!env.SCORES) return json({ error: 'leaderboard not configured' }, 503);
  const game = new URL(request.url).searchParams.get('game');
  if (!GAMES.has(game)) return json({ error: 'unknown game' }, 400);
  const rows = JSON.parse((await env.SCORES.get('scores:' + game)) || '[]');
  return json(rows);
}

export async function onRequestPost({ request, env }) {
  if (!env.SCORES) return json({ error: 'leaderboard not configured' }, 503);

  let body;
  try { body = await request.json(); } catch { return json({ error: 'bad json' }, 400); }

  const game = body.game;
  if (!GAMES.has(game)) return json({ error: 'unknown game' }, 400);

  const name = cleanName(body.name);
  if (!name) return json({ error: 'bad name' }, 400);

  const score = Number(body.score);
  if (!Number.isInteger(score) || score < 1 || score > 1000000) {
    return json({ error: 'bad score' }, 400);
  }

  const key = 'scores:' + game;
  const rows = JSON.parse((await env.SCORES.get(key)) || '[]');

  // keep each nickname's best entry only (lowest for times, highest for scores)
  const timeBased = LOWER_IS_BETTER.has(game);
  const existing = rows.find(r => r.name.toLowerCase() === name.toLowerCase());
  if (existing) {
    const worseOrEqual = timeBased ? score >= existing.score : score <= existing.score;
    if (worseOrEqual) return json({ ok: true, kept: existing.score });
    existing.score = score;
    existing.at = Date.now();
  } else {
    rows.push({ name, score, at: Date.now() });
  }

  rows.sort(timeBased ? (a, b) => a.score - b.score : (a, b) => b.score - a.score);
  rows.length = Math.min(rows.length, MAX_ROWS);
  await env.SCORES.put(key, JSON.stringify(rows));
  return json({ ok: true });
}
