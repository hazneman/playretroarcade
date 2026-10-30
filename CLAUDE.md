# PlayRetroArcade

Static retro-games site: a catalog home page plus 8 self-contained HTML5 canvas games. No frameworks, no build step, no package manager — every page is a single standalone HTML file with inline CSS and JS.

## Architecture

- `index.html` — home page. The game catalog is the `GAMES` array in its inline script; search/filter/sort and the header game counter all derive from it.
- `<GameName>/index.html` — each game is one self-contained file (canvas rendering, inline styles/scripts). Games do not share code.
- `Public/logo.svg` — site logo, used as favicon and header image on all pages. There is deliberately no `logo.png` (a mislabeled SVG-as-PNG once lived there and broke rendering — don't recreate it).
- `Sound/` — shared `.ogg` music loops referenced by some games.
- `Battleship/` — classic Amiral Battı vs an AI (DOM grid, not canvas); ship sprites live in `Battleship/Assets/`.
- High scores and preferences use per-game localStorage keys (`snake_best`, `tetrisBest`, `spaceInvadersHighScore`, …). There is no backend, no accounts, and no data collection — keep it that way; this is a kid-friendly site.

## Adding a game

1. Create `<GameName>/index.html` (self-contained, favicon + logo via `../Public/logo.svg`).
2. Add an entry to the `GAMES` array in `index.html` (id, title, description, genres, players, updatedAt, route, emoji, featured, tags). Do not add fake ratings or play counts.

## Deployment

Cloudflare Pages, auto-deploys from `main` (no build command, output = repo root): https://playretroarcade.pages.dev

## Design system

`Public/arcade.css` is the single source of design truth: palette, the one brand cyan (#00f5ff — never introduce a second cyan), the three-step radius scale (8/12/20), font stacks (system UI for body, 'Courier New' only for big titles and HUD chips), shadows, and shared `arc-*` components (topbar, pill, btn, panel, chip, overlay). Every first-party page links it before its own `<style>` and differs only by `--game-accent` (e.g. Basketball orange, RaceCar red) plus its own game art. Don't redefine shell values locally — alias the arcade tokens. Third-party games (2048, ADarkRoom) keep their upstream look and do NOT link it.

## Third-party games

Open-source games may be added for future ad monetization, but only under licenses that allow commercial use (MIT, BSD, Apache, Unlicense, MPL; never any "NC" license). Each one keeps its upstream LICENSE file and in-game credits in its own folder (`2048/` and `ADarkRoom/` are the pattern), and gets a small "Back to PlayRetroArcade" link. Strip any analytics tags and CDN script loads when vendoring. Never add emulated ROMs or games whose *names* are live trademarks — and vet the ASSETS separately from the code license: jakesgordon/javascript-racer was rejected because its code is MIT but its sprites are ripped from Sega's OutRun and its music is licensed to that project only.

## Conventions

- Never commit editor/OS files, backups (`*.bak`, `*.tmp`, `index_old.html`-style copies), or one-off fix scripts — see `.gitignore`.
- Verify changes by opening the page in a browser; there are no tests.
