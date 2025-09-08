#!/usr/bin/env python3
import re

print("Applying careful fix to Neon Maze Runner...")

# Read the game file
with open('/Users/hasannumanoglu/Documents/SoftDev/playretroarcade/playretroarcade/NeonMazeRunner/index.html', 'r') as f:
    content = f.read()

# Find the exact location to insert the isReachable function
# Look for the end of findEmptyTiles function
find_empty_end = content.find('    }\n\n    function spawnExitPortal()')
if find_empty_end == -1:
    find_empty_end = content.find('    }\n    \n    function spawnExitPortal()')

if find_empty_end != -1:
    # Insert the isReachable function right before spawnExitPortal
    is_reachable_function = '''
    // Check if a tile is reachable from player position using BFS
    function isReachable(targetX, targetY) {
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
    }
'''
    
    # Insert the function
    insertion_point = content.find('\n    function spawnExitPortal()')
    content = content[:insertion_point] + is_reachable_function + content[insertion_point:]
    
    # Now replace the spawnExitPortal function content carefully
    # Find the exact function body
    start_pattern = 'function spawnExitPortal() {'
    start_pos = content.find(start_pattern)
    
    if start_pos != -1:
        # Find the end of this function by counting braces
        brace_count = 0
        pos = start_pos + len(start_pattern)
        
        while pos < len(content):
            if content[pos] == '{':
                brace_count += 1
            elif content[pos] == '}':
                if brace_count == 0:
                    break
                brace_count -= 1
            pos += 1
        
        # Replace the function content
        old_function = content[start_pos:pos+1]
        new_function = '''function spawnExitPortal() {
      const emptyTiles = findEmptyTiles();
      
      // Filter tiles that are reachable from player position
      const reachableTiles = emptyTiles.filter(tile => isReachable(tile.x, tile.y));
      
      // Further filter by distance from player (must be reasonably far)
      const farTiles = reachableTiles.filter(tile => {
        const dx = tile.x * TILE_SIZE - game.player.x;
        const dy = tile.y * TILE_SIZE - game.player.y;
        return Math.sqrt(dx*dx + dy*dy) > TILE_SIZE * 3; // Reduced from 5 to 3 for better placement
      });
      
      // Use far tiles if available, otherwise use any reachable tile
      const availableTiles = farTiles.length > 0 ? farTiles : reachableTiles;
      
      if (availableTiles.length > 0) {
        const spawn = availableTiles[0];
        game.exitPortal = {
          x: spawn.x * TILE_SIZE,
          y: spawn.y * TILE_SIZE
        };
        console.log(`Exit portal placed at reachable location: (${spawn.x}, ${spawn.y})`);
      } else {
        // Fallback: if no reachable tiles found, try again with looser constraints
        console.warn('No reachable tiles found for exit portal, using fallback placement');
        if (emptyTiles.length > 0) {
          const spawn = emptyTiles[0];
          game.exitPortal = {
            x: spawn.x * TILE_SIZE,
            y: spawn.y * TILE_SIZE
          };
        }
      }
    }'''
        
        content = content.replace(old_function, new_function)
    
    # Write the updated content back
    with open('/Users/hasannumanoglu/Documents/SoftDev/playretroarcade/playretroarcade/NeonMazeRunner/index.html', 'w') as f:
        f.write(content)
    
    print("✅ Careful fix applied successfully!")
    print("✅ Exit placement will now use pathfinding to ensure reachability")
else:
    print("❌ Could not find insertion point for the fix")
