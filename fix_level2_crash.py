#!/usr/bin/env python3
"""
Fix level 2 crash by improving the exit portal spawning logic and level transition timing.
"""

import re

def fix_level2_crash():
    """Fix the level 2 crash by improving timing and error handling."""
    
    # Read the current file
    with open('NeonMazeRunner/index.html', 'r') as f:
        content = f.read()
    
    # Find and replace the spawnExitPortal function with improved error handling
    old_spawn_function = '''    function spawnExitPortal() {
      const emptyTiles = findEmptyTiles();
      
      // Filter tiles that are reachable from player position
      const reachableTiles = emptyTiles.filter(tile => isReachable(tile.x, tile.y));
      
      // Further filter by distance from player (must be reasonably far)
      const farTiles = reachableTiles.filter(tile => {
        const dx = tile.x * TILE_SIZE - game.player.x;
        const dy = tile.y * TILE_SIZE - game.player.y;
        return Math.sqrt(dx*dx + dy*dy) > TILE_SIZE * 3; // Reduced from 5 to 3 for better placement
      });
      
      if (farTiles.length > 0) {
        const randomTile = farTiles[Math.floor(Math.random() * farTiles.length)];
        game.exitPortal = {
          x: randomTile.x * TILE_SIZE,
          y: randomTile.y * TILE_SIZE,
          active: true
        };
        console.log('Exit portal spawned at reachable location:', randomTile);
      } else if (reachableTiles.length > 0) {
        // Fallback to any reachable tile if no far tiles available
        const randomTile = reachableTiles[Math.floor(Math.random() * reachableTiles.length)];
        game.exitPortal = {
          x: randomTile.x * TILE_SIZE,
          y: randomTile.y * TILE_SIZE,
          active: true
        };
        console.log('Exit portal spawned at close reachable location:', randomTile);
      } else {
        // Final fallback to any empty tile
        const randomTile = emptyTiles[Math.floor(Math.random() * emptyTiles.length)];
        game.exitPortal = {
          x: randomTile.x * TILE_SIZE,
          y: randomTile.y * TILE_SIZE,
          active: true
        };
        console.log('Exit portal spawned at fallback location:', randomTile);
      }
    }'''
    
    new_spawn_function = '''    function spawnExitPortal() {
      try {
        const emptyTiles = findEmptyTiles();
        
        if (!emptyTiles || emptyTiles.length === 0) {
          console.error('No empty tiles found for exit portal');
          return;
        }
        
        // Try to filter reachable tiles with error handling
        let reachableTiles = emptyTiles;
        try {
          if (game && game.player && game.maze) {
            reachableTiles = emptyTiles.filter(tile => isReachable(tile.x, tile.y));
          }
        } catch (error) {
          console.warn('Pathfinding failed, using all empty tiles:', error);
          reachableTiles = emptyTiles;
        }
        
        // Further filter by distance from player (must be reasonably far)
        let farTiles = [];
        try {
          if (game && game.player) {
            farTiles = reachableTiles.filter(tile => {
              const dx = tile.x * TILE_SIZE - game.player.x;
              const dy = tile.y * TILE_SIZE - game.player.y;
              return Math.sqrt(dx*dx + dy*dy) > TILE_SIZE * 3;
            });
          }
        } catch (error) {
          console.warn('Distance filtering failed:', error);
          farTiles = [];
        }
        
        // Choose the best available tile
        let selectedTile;
        if (farTiles.length > 0) {
          selectedTile = farTiles[Math.floor(Math.random() * farTiles.length)];
          console.log('Exit portal spawned at far reachable location:', selectedTile);
        } else if (reachableTiles.length > 0) {
          selectedTile = reachableTiles[Math.floor(Math.random() * reachableTiles.length)];
          console.log('Exit portal spawned at close reachable location:', selectedTile);
        } else {
          selectedTile = emptyTiles[Math.floor(Math.random() * emptyTiles.length)];
          console.log('Exit portal spawned at fallback location:', selectedTile);
        }
        
        if (selectedTile) {
          game.exitPortal = {
            x: selectedTile.x * TILE_SIZE,
            y: selectedTile.y * TILE_SIZE,
            active: true
          };
        }
      } catch (error) {
        console.error('Critical error in spawnExitPortal:', error);
        // Emergency fallback - just place it somewhere
        game.exitPortal = {
          x: TILE_SIZE * 2,
          y: TILE_SIZE * 2,
          active: true
        };
      }
    }'''
    
    # Replace the function
    if old_spawn_function in content:
        content = content.replace(old_spawn_function, new_spawn_function)
        print("✅ Updated spawnExitPortal function with comprehensive error handling")
    else:
        print("❌ Could not find the exact spawnExitPortal function to replace")
        return False
    
    # Also improve the nextLevel function with a small delay to ensure state is ready
    old_next_level = '''    function nextLevel() {
      game.level++;
      game.gameState = 'playing';
      game.startTime = Date.now();
      
      hideAllMenus();
      generateLevel();
    }'''
    
    new_next_level = '''    function nextLevel() {
      game.level++;
      game.gameState = 'transitioning';
      game.startTime = Date.now();
      
      hideAllMenus();
      
      // Add a small delay to ensure clean state transition
      setTimeout(() => {
        try {
          generateLevel();
          game.gameState = 'playing';
        } catch (error) {
          console.error('Error during level generation:', error);
          // Fallback to previous level if generation fails
          game.level--;
          game.gameState = 'playing';
        }
      }, 100);
    }'''
    
    if old_next_level in content:
        content = content.replace(old_next_level, new_next_level)
        print("✅ Updated nextLevel function with delayed state transition")
    else:
        print("⚠️ Could not find nextLevel function - continuing anyway")
    
    # Write the updated content back to the file
    with open('NeonMazeRunner/index.html', 'w') as f:
        f.write(content)
    
    print("🎮 Level 2 crash fix applied successfully!")
    return True

if __name__ == "__main__":
    fix_level2_crash()
