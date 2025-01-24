# Directions
[1, 0, 0, 0] # Straight 
[0, 1, 0, 0] # Right
[0, 0, 1, 0] # Left
[0, 0, 0, 1] # Back

# Rewards
# Food -> +10
# Obstacle -> -10

# States (with a vision of only 1 block, 0 and 1 values) 
# where 1 is the obtable or the food and 0 is the empty space
[1, 0, 0, 0, 0, 0, 0, 0, 0] # Obstacle straight
[0, 1, 0, 0, 0, 0, 0, 0, 0] # Obstacle right
[0, 0, 1, 0, 0, 0, 0, 0, 0] # Obstacle left
[0, 0, 0, 1, 0, 0, 0, 0, 0] # Obstacle back
[0, 0, 0, 0, 1, 0, 0, 0, 0] # Food straight
[0, 0, 0, 0, 0, 1, 0, 0, 0] # Food left
[0, 0, 0, 0, 0, 0, 1, 0, 0] # Food right
[0, 0, 0, 0, 0, 0, 0, 1, 0] # Food back
[0, 0, 0, 0, 0, 0, 0, 0, 1] # Empty space

# Just thinking that if I want to estend the vision to 2 blocks, I will have 2^6 = 64 states because every state 
# would be a vector of 2 elements (0 or 1) for each of the 6 blocks. 

# Using Bellman Equation to calculate the Q value

# Per verificare la collisione tra due sfere è necessario calcolare la distanza tra i due centri e controllare che questa
# sia inferiore alle somma dei raggi delle due sfere