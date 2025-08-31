#!/bin/bash

# Fix NeonMazeRunner drone boundary issues

cd "$(dirname "$0")"

# Backup original
cp NeonMazeRunner/index.html NeonMazeRunner/index.html.bak

# Apply patches to fix drone boundary issues
python3 << 'EOF'
import re

# Read the file
with open('NeonMazeRunner/index.html', 'r') as f:
    content = f.read()

# Fix 1: Add boundary constraint function
constraint_function = '''
    // Safety function to keep drones within bounds
    function constrainToBounds(drone) {
      drone.x = Math.max(TILE_SIZE, Math.min(drone.x, CANVAS_WIDTH - drone.size - TILE_SIZE));
      drone.y = Math.max(TILE_SIZE, Math.min(drone.y, CANVAS_HEIGHT - drone.size - TILE_SIZE));
    }
'''

# Insert constraint function before the game loop
content = re.sub(r'(\s+// Game loop\s+function gameLoop\(\))', constraint_function + r'\1', content)

# Fix 2: Update patrol movement to include boundary check
old_patrol = r'''        } else {
          this\.x \+= \(dx / distance\) \* this\.speed;
          this\.y \+= \(dy / distance\) \* this\.speed;
        }'''

new_patrol = '''        } else {
          const newX = this.x + (dx / distance) * this.speed;
          const newY = this.y + (dy / distance) * this.speed;
          
          // Check boundaries before moving
          if (newX >= TILE_SIZE && newX + this.size <= CANVAS_WIDTH - TILE_SIZE && 
              newY >= TILE_SIZE && newY + this.size <= CANVAS_HEIGHT - TILE_SIZE) {
            this.x = newX;
            this.y = newY;
          } else {
            // If can't move to target, skip to next patrol point
            this.pathIndex = (this.pathIndex + 1) % this.patrolPath.length;
          }
        }'''

content = re.sub(old_patrol, new_patrol, content)

# Fix 3: Update hunter movement
old_hunter = r'''            if \(!this\.checkWallCollision\(this\.x \+ moveX, this\.y\)\) {
              this\.x \+= moveX;
            }
            if \(!this\.checkWallCollision\(this\.x, this\.y \+ moveY\)\) {
              this\.y \+= moveY;
            }'''

new_hunter = '''            const newX = this.x + moveX;
            const newY = this.y + moveY;
            
            if (!this.checkWallCollision(newX, this.y) && 
                newX >= TILE_SIZE && newX + this.size <= CANVAS_WIDTH - TILE_SIZE) {
              this.x = newX;
            }
            if (!this.checkWallCollision(this.x, newY) && 
                newY >= TILE_SIZE && newY + this.size <= CANVAS_HEIGHT - TILE_SIZE) {
              this.y = newY;
            }'''

content = re.sub(old_hunter, new_hunter, content)

# Fix 4: Update guard movement
old_guard = r'''            if \(!this\.checkWallCollision\(this\.x \+ moveX, this\.y\)\) {
              this\.x \+= moveX;
            }
            if \(!this\.checkWallCollision\(this\.x, this\.y \+ moveY\)\) {
              this\.y \+= moveY;
            }'''

new_guard = '''            const newX = this.x + moveX;
            const newY = this.y + moveY;
            
            if (!this.checkWallCollision(newX, this.y) && 
                newX >= TILE_SIZE && newX + this.size <= CANVAS_WIDTH - TILE_SIZE) {
              this.x = newX;
            }
            if (!this.checkWallCollision(this.x, newY) && 
                newY >= TILE_SIZE && newY + this.size <= CANVAS_HEIGHT - TILE_SIZE) {
              this.y = newY;
            }'''

content = re.sub(old_guard, new_guard, content, count=1)

# Fix 5: Update moveInDirection
old_move_direction = r'''        if \(!this\.checkWallCollision\(newX, newY\)\) {
          this\.x = newX;
          this\.y = newY;
        } else {
          this\.direction = Math\.floor\(Math\.random\(\) \* 4\);
        }'''

new_move_direction = '''        if (!this.checkWallCollision(newX, newY) && 
            newX >= TILE_SIZE && newX + this.size <= CANVAS_WIDTH - TILE_SIZE &&
            newY >= TILE_SIZE && newY + this.size <= CANVAS_HEIGHT - TILE_SIZE) {
          this.x = newX;
          this.y = newY;
        } else {
          this.direction = Math.floor(Math.random() * 4);
        }'''

content = re.sub(old_move_direction, new_move_direction, content)

# Fix 6: Add constraint calls in game loop
old_game_loop = r'''      // Update
      game\.player\.update\(\);
      game\.drones\.forEach\(drone => drone\.update\(\)\);'''

new_game_loop = '''      // Update
      game.player.update();
      game.drones.forEach(drone => {
        drone.update();
        constrainToBounds(drone); // Safety constraint
      });'''

content = re.sub(old_game_loop, new_game_loop, content)

# Write the fixed content
with open('NeonMazeRunner/index.html', 'w') as f:
    f.write(content)

print("Applied drone boundary fixes!")
EOF
