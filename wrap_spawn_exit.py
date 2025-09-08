#!/usr/bin/env python3
"""
Wrap the spawnExitPortal function with try-catch to prevent crashes.
"""

import re

def wrap_spawn_exit_with_try_catch():
    """Wrap the spawnExitPortal function with comprehensive error handling."""
    
    # Read the current file
    with open('NeonMazeRunner/index.html', 'r') as f:
        content = f.read()
    
    # Find the spawnExitPortal function and wrap it with try-catch
    pattern = r'(    function spawnExitPortal\(\) \{)(.*?)(\n    \})'
    
    def replacement(match):
        indent = "    "
        function_header = match.group(1)
        function_body = match.group(2)
        function_end = match.group(3)
        
        # Indent the original function body by 2 more spaces for the try block
        indented_body = re.sub(r'\n      ', '\n        ', function_body)
        indented_body = re.sub(r'\n    ', '\n      ', indented_body)
        
        new_function = f"""{function_header}
      try {{
        {indented_body.strip()}
      }} catch (error) {{
        console.error('Critical error in spawnExitPortal:', error);
        console.log('Game state:', game ? 'exists' : 'null');
        console.log('Player state:', game && game.player ? 'exists' : 'null');
        console.log('Maze state:', game && game.maze ? 'exists' : 'null');
        
        // Emergency fallback - place exit at a safe location
        try {{
          const fallbackTiles = findEmptyTiles();
          if (fallbackTiles && fallbackTiles.length > 0) {{
            const spawn = fallbackTiles[0];
            game.exitPortal = {{
              x: spawn.x * TILE_SIZE,
              y: spawn.y * TILE_SIZE
            }};
            console.log('Exit portal placed at emergency fallback location');
          }} else {{
            // Absolute emergency - place it at a fixed location
            game.exitPortal = {{
              x: TILE_SIZE * 2,
              y: TILE_SIZE * 2
            }};
            console.log('Exit portal placed at absolute emergency location');
          }}
        }} catch (emergencyError) {{
          console.error('Even emergency fallback failed:', emergencyError);
          // Don't crash the game - just log and continue
        }}
      }}
{function_end}"""
        return new_function
    
    # Apply the replacement
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        # Write the updated content back to the file
        with open('NeonMazeRunner/index.html', 'w') as f:
            f.write(new_content)
        print("✅ Wrapped spawnExitPortal with comprehensive error handling")
        return True
    else:
        print("❌ Could not find spawnExitPortal function to wrap")
        return False

if __name__ == "__main__":
    wrap_spawn_exit_with_try_catch()
