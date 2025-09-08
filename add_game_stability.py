#!/usr/bin/env python3
"""
Add error handling to game loop and level transitions.
"""

def add_game_loop_error_handling():
    """Add try-catch to critical game functions."""
    
    # Read the current file
    with open('NeonMazeRunner/index.html', 'r') as f:
        content = f.read()
    
    # Add error handling to gameLoop
    old_game_loop = '''    function gameLoop() {
      if (game.gameState !== 'playing') return;
      
      // Update
      game.player.update();
      game.drones.forEach(drone => drone.update());'''
    
    new_game_loop = '''    function gameLoop() {
      try {
        if (game.gameState !== 'playing') return;
        
        // Update
        if (game.player && typeof game.player.update === 'function') {
          game.player.update();
        }
        if (game.drones && Array.isArray(game.drones)) {
          game.drones.forEach(drone => {
            if (drone && typeof drone.update === 'function') {
              drone.update();
            }
          });
        }'''
    
    # Replace the game loop start
    if old_game_loop in content:
        content = content.replace(old_game_loop, new_game_loop)
        print("✅ Added error handling to gameLoop")
    else:
        print("⚠️ Could not find exact gameLoop pattern")
    
    # Add error handling to nextLevel function
    old_next_level = '''    function nextLevel() {
      game.level++;
      game.gameState = 'playing';
      game.startTime = Date.now();
      
      hideAllMenus();
      generateLevel();
    }'''
    
    new_next_level = '''    function nextLevel() {
      try {
        game.level++;
        game.gameState = 'transitioning';
        game.startTime = Date.now();
        
        hideAllMenus();
        
        // Add a small delay to ensure clean state transition
        setTimeout(() => {
          try {
            generateLevel();
            game.gameState = 'playing';
            console.log('Successfully transitioned to level', game.level);
          } catch (generateError) {
            console.error('Error during level generation:', generateError);
            // Fallback to previous level if generation fails
            game.level--;
            game.gameState = 'playing';
            alert('Error loading level ' + (game.level + 1) + '. Staying on level ' + game.level);
          }
        }, 100);
      } catch (error) {
        console.error('Error in nextLevel:', error);
        game.gameState = 'playing';
      }
    }'''
    
    if old_next_level in content:
        content = content.replace(old_next_level, new_next_level)
        print("✅ Added error handling to nextLevel with delayed transition")
    else:
        print("⚠️ Could not find exact nextLevel pattern")
    
    # Write the updated content back to the file
    with open('NeonMazeRunner/index.html', 'w') as f:
        f.write(content)
    
    print("🎮 Game stability improvements applied!")
    return True

if __name__ == "__main__":
    add_game_loop_error_handling()
