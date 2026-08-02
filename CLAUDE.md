# PlayRetroArcade

Static retro-games site: a catalog home page plus 8 self-contained HTML5 canvas games. No frameworks, no build step, no package manager — every page is a single standalone HTML file with inline CSS and JS.

## Architecture

- `index.html` — home page. The game catalog is the `GAMES` array in its inline script; search/filter/sort and the header game counter all derive from it.
- `<GameName>/index.html` — each game is one self-contained file (canvas rendering, inline styles/scripts). Games do not share code.
- `Public/logo.svg` — site logo, used as favicon and header image on all pages. There is deliberately no `logo.png` (a mislabeled SVG-as-PNG once lived there and broke rendering — don't recreate it).
- `Sound/` — shared `.ogg` music loops referenced by some games.
- High scores and preferences use per-game localStorage keys (`snake_best`, `tetrisBest`, `spaceInvadersHighScore`, …). There is no backend, no accounts, and no data collection — keep it that way; this is a kid-friendly site.

## Adding a game

1. Create `<GameName>/index.html` (self-contained, favicon + logo via `../Public/logo.svg`).
2. Add an entry to the `GAMES` array in `index.html` (id, title, description, genres, players, updatedAt, route, emoji, featured, tags). Do not add fake ratings or play counts.

## Deployment

Cloudflare Pages, auto-deploys from `main` (no build command, output = repo root): https://playretroarcade.pages.dev

## Conventions

- Never commit editor/OS files, backups (`*.bak`, `*.tmp`, `index_old.html`-style copies), or one-off fix scripts — see `.gitignore`.
- Verify changes by opening the page in a browser; there are no tests.
