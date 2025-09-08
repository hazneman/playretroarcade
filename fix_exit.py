#!/usr/bin/env python3
import re

# Read the game file
with open('/Users/hasannumanoglu/Documents/SoftDev/playretroarcade/playretroarcade/NeonMazeRunner/index.html', 'r') as f:
    content = f.read()

# Define the new isReachable function
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

# Define the new spawnExitPortal function
new_spawn_exit_portal = '''    function spawnExitPortal() {
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

# Insert the isReachable function before spawnExitPortal
insert_position = content.find('    function spawnExitPortal()')
if insert_position != -1:
    content = content[:insert_position] + is_reachable_function + '\n' + content[insert_position:]

# Replace the old spawnExitPortal function
old_pattern = r'    function spawnExitPortal\(\) \{[^}]*\{[^}]*\}[^}]*\}'
content = re.sub(old_pattern, new_spawn_exit_portal, content, flags=re.DOTALL)

# Write the updated content back
with open('/Users/hasannumanoglu/Documents/SoftDev/playretroarcade/playretroarcade/NeonMazeRunner/index.html', 'w') as f:
    f.write(content)

print("Exit placement fix applied successfully!")
