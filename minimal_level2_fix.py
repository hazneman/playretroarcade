#!/usr/bin/env python3
"""
Careful fix for level 2 crash - only modify the nextLevel function with minimal changes.
"""

def careful_level2_fix():
    """Apply minimal fix to prevent level 2 crash."""
    
    # Read the current file
    with open('NeonMazeRunner/index.html', 'r') as f:
        content = f.read()
    
    # Only modify the nextLevel function to add a small delay
    old_next_level = '''    function nextLevel() {
      game.level++;
      game.gameState = 'playing';
      game.startTime = Date.now();
      
      hideAllMenus();
      generateLevel();
    }'''
    
    new_next_level = '''    function nextLevel() {
      game.level++;
      game.gameState = 'playing';
      game.startTime = Date.now();
      
      hideAllMenus();
      
      // Small delay to ensure state is ready for level transition
      setTimeout(() => {
        generateLevel();
      }, 50);
    }'''
    
    if old_next_level in content:
        content = content.replace(old_next_level, new_next_level)
        print("✅ Applied minimal nextLevel fix")
    else:
        print("❌ Could not find nextLevel function")
        return False
    
    # Also add minimal error handling just to the isReachable function calls
    # Find spawnExitPortal and make it more defensive
    old_spawn = '''      // Filter tiles that are reachable from player position
      const reachableTiles = emptyTiles.filter(tile => isReachable(tile.x, tile.y));'''
    
    new_spawn = '''      // Filter tiles that are reachable from player position
      let reachableTiles = emptyTiles;
      try {
        if (game && game.player && game.maze) {
          reachableTiles = emptyTiles.filter(tile => isReachable(tile.x, tile.y));
        }
      } catch (e) {
        console.warn('Pathfinding check failed, using all empty tiles');
      }'''
    
    if old_spawn in content:
        content = content.replace(old_spawn, new_spawn)
        print("✅ Added minimal safety check to spawnExitPortal")
    
    # Write the updated content back to the file
    with open('NeonMazeRunner/index.html', 'w') as f:
        f.write(content)
    
    print("🎮 Minimal level 2 fix applied successfully!")
    return True

if __name__ == "__main__":
    careful_level2_fix()
