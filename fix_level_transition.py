#!/usr/bin/env python3
"""
Fix level transition crash by adding safety checks to isReachable function.
"""

import re

def fix_level_transition():
    """Add safety checks to prevent crashes during level transitions."""
    
    # Read the current file
    with open('NeonMazeRunner/index.html', 'r') as f:
        content = f.read()
    
    # Find and replace the isReachable function with safety checks
    old_function = '''    function isReachable(targetX, targetY) {
      const playerTileX = Math.floor(game.player.x / TILE_SIZE);
      const playerTileY = Math.floor(game.player.y / TILE_SIZE);
      
      if (playerTileX === targetX && playerTileY === targetY) {
        return true;
      }
      
      const visited = new Set();
      const queue = [{x: playerTileX, y: playerTileY}];
      visited.add(`${playerTileX},${playerTileY}`);
      
      const directions = [{x: 0, y: 1}, {x: 1, y: 0}, {x: 0, y: -1}, {x: -1, y: 0}];
      
      while (queue.length > 0) {
        const current = queue.shift();
        
        if (current.x === targetX && current.y === targetY) {
          return true;
        }
        
        for (const dir of directions) {
          const newX = current.x + dir.x;
          const newY = current.y + dir.y;
          const key = `${newX},${newY}`;
          
          if (newX >= 0 && newX < MAZE_WIDTH && 
              newY >= 0 && newY < MAZE_HEIGHT && 
              !visited.has(key) && 
              game.maze[newY][newX] === 0) {
            visited.add(key);
            queue.push({x: newX, y: newY});
          }
        }
      }
      
      return false;
    }'''
    
    new_function = '''    function isReachable(targetX, targetY) {
      // Safety checks to prevent crashes during level transitions
      if (!game || !game.player || !game.maze) {
        console.log('Game not fully initialized, assuming reachable');
        return true;
      }
      
      // Check if player coordinates are valid
      if (typeof game.player.x !== 'number' || typeof game.player.y !== 'number') {
        console.log('Player coordinates not valid, assuming reachable');
        return true;
      }
      
      const playerTileX = Math.floor(game.player.x / TILE_SIZE);
      const playerTileY = Math.floor(game.player.y / TILE_SIZE);
      
      // Check if player position is within maze bounds
      if (playerTileX < 0 || playerTileX >= MAZE_WIDTH || 
          playerTileY < 0 || playerTileY >= MAZE_HEIGHT) {
        console.log('Player position out of bounds, assuming reachable');
        return true;
      }
      
      if (playerTileX === targetX && playerTileY === targetY) {
        return true;
      }
      
      const visited = new Set();
      const queue = [{x: playerTileX, y: playerTileY}];
      visited.add(`${playerTileX},${playerTileY}`);
      
      const directions = [{x: 0, y: 1}, {x: 1, y: 0}, {x: 0, y: -1}, {x: -1, y: 0}];
      
      while (queue.length > 0) {
        const current = queue.shift();
        
        if (current.x === targetX && current.y === targetY) {
          return true;
        }
        
        for (const dir of directions) {
          const newX = current.x + dir.x;
          const newY = current.y + dir.y;
          const key = `${newX},${newY}`;
          
          if (newX >= 0 && newX < MAZE_WIDTH && 
              newY >= 0 && newY < MAZE_HEIGHT && 
              !visited.has(key) && 
              game.maze[newY] && game.maze[newY][newX] === 0) {
            visited.add(key);
            queue.push({x: newX, y: newY});
          }
        }
      }
      
      return false;
    }'''
    
    # Replace the function
    if old_function in content:
        content = content.replace(old_function, new_function)
        print("✅ Updated isReachable function with safety checks")
    else:
        print("❌ Could not find the exact isReachable function to replace")
        return False
    
    # Write the updated content back to the file
    with open('NeonMazeRunner/index.html', 'w') as f:
        f.write(content)
    
    print("🎮 Level transition fix applied successfully!")
    return True

if __name__ == "__main__":
    fix_level_transition()
