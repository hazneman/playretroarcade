# PlayRetroArcade 🎮

Quick, clean, and kid-friendly retro games. Pick a classic and play instantly — no installs, no sign-ups, no downloads.

## Games

| Game | Description |
|------|-------------|
| 🐍 **Snake Classic** | Eat food, grow longer, don't hit the walls or yourself |
| 🟦 **Tetris** | Stack falling blocks to clear lines |
| 👾 **Space Invaders** | Defend Earth from waves of descending aliens |
| 🏀 **Basketball Shootout** | Physics-based shooting with realistic ball physics |
| 🏎️ **Race Car Championship** | High-speed racing with AI opponents and time trials |
| 🌐 **Neon Maze Runner** | Navigate neon mazes, dodge drones, find the exit portal |
| ⚓ **Sky & Sea Defense** | Defend your fleet from air and sea attacks |
| 🚢 **Battleship (Amiral Battı)** | The classic hidden-fleet guessing game vs an AI admiral |
| 🔢 **2048** | The beloved sliding-tile puzzle ([open source, MIT](https://github.com/gabrielecirulli/2048) by Gabriele Cirulli) |

## Project Structure

```
/
├── index.html          # Home page with game catalog (search, filter, sort)
├── Snake/              # Each game is a self-contained index.html
├── Tetris/
├── SpaceInvaders/
├── Basketball/
├── RaceCar/
├── NeonMazeRunner/
├── SkySeaDefense/
├── Battleship/         # + pixel art ship assets
├── Public/             # Logo
└── Sound/              # Shared music loops
```

## Getting Started

1. Open `index.html` in your browser for the game catalog
2. Click any game to play
3. Keyboard controls on desktop, on-screen controls on mobile

## Technical Details

- Pure HTML5, CSS3, and JavaScript — no frameworks, no build step
- Each game is a single self-contained HTML file with canvas rendering
- High scores and preferences persist via localStorage (per browser)
- Deployed on Cloudflare Pages (auto-deploys from `main`): https://playretroarcade.pages.dev

Enjoy the retro gaming experience! 🕹️
