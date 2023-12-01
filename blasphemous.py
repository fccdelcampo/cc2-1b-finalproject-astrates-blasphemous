import random
import time
from collections import deque

class Cell:
    def __init__(self, symbol, passable=True):
        self.symbol = symbol
        self.passable = passable

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[Cell('#') for _ in range(width)] for _ in range(height)]

    def generate_maze(self):
        # Initialize the maze with solid borders
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    self.cells[y][x] = Cell('#')
                else:
                    self.cells[y][x] = Cell(' ')

        # Create a stack for backtracking
        stack = [(2, 2)]

        while stack:
            current_x, current_y = stack[-1]

            # Get neighbors
            neighbors = [(current_x + 2, current_y), (current_x - 2, current_y),
                         (current_x, current_y + 2), (current_x, current_y - 2)]
            neighbors = [(x, y) for x, y in neighbors if 0 < x < self.width - 1 and 0 < y < self.height - 1]

            unvisited_neighbors = [(x, y) for x, y in neighbors if self.cells[y][x].symbol == ' ']

            if unvisited_neighbors:
                next_x, next_y = random.choice(unvisited_neighbors)
                wall_x, wall_y = (current_x + next_x) // 2, (current_y + next_y) // 2

                self.cells[wall_y][wall_x] = Cell('#')
                self.cells[next_y][next_x] = Cell('#')
                stack.append((next_x, next_y))
            else:
                stack.pop()

    def spawn_entity(self, entity_symbol, x, y):
        self.cells[y][x] = Cell(entity_symbol)
        return x, y

    def remove_entity(self, x, y):
        self.cells[y][x] = Cell(' ')

    def move_entity(self, old_x, old_y, new_x, new_y):
        if self.cells[new_y][new_x].passable:
            self.cells[new_y][new_x], self.cells[old_y][old_x] = self.cells[old_y][old_x], Cell(' ')

    def print_grid(self, player_x, player_y):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[y][x]
                if x == player_x and y == player_y:
                    print('P', end=' ')
                else:
                    print(cell.symbol, end=' ')
            print()

class Entity:
    def __init__(self, name, health, speed, attack):
        self.name = name
        self.health = health
        self.speed = speed
        self.attack = attack

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

def fade_in_text(text, delay=0.001):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def is_path_exists(grid, start, end):
    visited = set()
    queue = deque([start])

    while queue:
        current_x, current_y = queue.popleft()
        if (current_x, current_y) == end:
            return True

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_x, next_y = current_x + dx, current_y + dy
            if 0 < next_x < len(grid[0]) - 1 and 0 < next_y < len(grid) - 1 and grid[next_y][next_x].symbol == ' ' and (next_x, next_y) not in visited:
                visited.add((next_x, next_y))
                queue.append((next_x, next_y))

    return False

def play_game():
    width = 20
    height = 10
    num_enemies = 5

    enemies_defeated = 0
    
    grid = Grid(width, height)
    grid.generate_maze()  # Start generating maze from (1, 1) to ensure an open space
    player_x, player_y = (1, 1)

    player = Entity("Hero", 100, 10, 20)

    # Initialize enemies and their positions
    enemies = []
    enemy_positions = []

    for i in range(num_enemies):
        # Try to find a valid position for the enemy
        while True:
            enemy_x = random.randint(1, width - 2)
            enemy_y = random.randint(1, height - 2)

            # Check if there is a path from player to the enemy
            if is_path_exists(grid.cells, (player_x, player_y), (enemy_x, enemy_y)):
                break

        enemies.append(Entity(f"Enemy{i}", random.randint(20, 50), random.randint(5, 10), random.randint(5, 15)))
        enemy_positions.append(grid.spawn_entity('E', enemy_x, enemy_y))

    while enemies_defeated != 5:
        grid.print_grid(player_x, player_y)
        print("\nPlayer Stats:")
        print(f"Name: {player.name}")
        print(f"HP: {player.health}")
        print(f"Speed: {player.speed}")
        print(f"Attack: {player.attack}")
        
        # Check if there are no more enemies


        for enemy, (enemy_x, enemy_y) in zip(enemies, enemy_positions):
            if (abs(player_x - enemy_x) == 1 and player_y == enemy_y) or \
                    (player_x == enemy_x and abs(player_y - enemy_y) == 1):
                print(f"Encountered {enemy.name} or {enemy.name}'s previous position!")
                while player.is_alive() and enemy.is_alive():
                    grid.print_grid(player_x, player_y)
                    print("\nPlayer Stats:")
                    print(f"Name: {player.name}")
                    print(f"HP: {player.health}")
                    print(f"Speed: {player.speed}")
                    print(f"Attack: {player.attack}")

                    print("\nEnemy Stats:")
                    print(f"Name: {enemy.name}")
                    print(f"HP: {enemy.health}")
                    print(f"Speed: {enemy.speed}")
                    print(f"Attack: {enemy.attack}")

                    action = input("\nEnter 'a' to attack, 'q' to run: ")

                    if action == 'a':
                        player_damage = player.attack
                        enemy.take_damage(player_damage)
                        print(f"\nYou dealt {player_damage} damage to {enemy.name}.")

                        if enemy.is_alive():
                            enemy_damage = enemy.attack
                            player.take_damage(enemy_damage)
                            print(f"{enemy.name} dealt {enemy_damage} damage to you.")
                        else:
                            print(f"\nYou defeated {enemy.name}!")
                            grid.remove_entity(enemy_x, enemy_y)
                            del(enemy)
                            enemies_defeated += 1
                            break

                    elif action == 'q':
                        print("You ran away from the battle.")
                        break

        if player.is_alive():
            # Get user input for movement or quitting
            action = input("\nEnter 'w' to move up, 'a' to move left, 's' to move down, 'd' to move right, or 'q' to quit: ")

            if action == 'q':
                print("You quit the game.")
                break

            # Move player based on input
            new_player_x, new_player_y = player_x, player_y

            if action == 'w' and player_y > 1 and grid.cells[player_y - 1][player_x].symbol == ' ':
                new_player_y -= 1
            elif action == 'a' and player_x > 1 and grid.cells[player_y][player_x - 1].symbol == ' ':
                new_player_x -= 1
            elif action == 's' and player_y < height - 2 and grid.cells[player_y + 1][player_x].symbol == ' ':
                new_player_y += 1
            elif action == 'd' and player_x < width - 2 and grid.cells[player_y][player_x + 1].symbol == ' ':
                new_player_x += 1

            # Check if the new position is within the maze
            if 0 < new_player_x < width - 1 and 0 < new_player_y < height - 1:
                player_x, player_y = new_player_x, new_player_y
                
    # Print credits after the game is over
    print("Congratulations, you defeated all enemies, you won!")
    print(credits)

def main():
    name = input("What's your name?\n")
    welcome = f"""BACKGROUND: Welcome to Blasphemous, {name}. Play as the Penitent One - a sole survivor 
     of the massacre of the ‘Silent Sorrow’. Trapped in an endless cycle of death and 
     rebirth, it’s down to him to free the world from this terrible fate and reach the 
     origin of his anguish."""

    story = """STORY: The story of Blasphemous is set in the deeply religious realm of Cvstodia, where the 
     Sorrowful Miracle manifests itself to both the pious and sinful in cruel and unusual 
     ways. Every pain of the soul is tangible within everyone and everywhere, whether in 
     the form of a blessing or a punishment. With such a divine and unfathomable will at 
     large, all one can do is make penance.

     A warrior forever vowed to silence, The Penitent One, awakens in a sanctuary 
     surrounded by his slain comrades. Under the guidance of Deogracias and with the 
     strength of the sword of guilt, he fights his way to the Cradle of Affliction to 
     fulfill this ultimate penance. Throughout his journey, he traverses a land ravaged 
     by the Grievous Miracle, battling beasts consumed by faith and rage, communing with 
     holy figures, assisting others at the mercy of The Miracle, and freeing tormented 
     souls from eternal punishment.

     The Penitent One's guilt is his strength; his pilgrimage is his penance. But 
     in the end, it is the will of The Miracle to decide if his guilt is enough to 
     earn him salvation.

     Blasphemous begins in the Brotherhood of the Silent Sorrow, a religious order opposed to
     His Holiness Escribar's authority, after all its members have been massacred. The last 
     of their kind, the Penitent One, is resurrected by the Miracle and departs on a pilgrimage."""

    menu = """
     To play, enter the number of your choosing below.
     1 - START GAME
     2 - SEE INITIAL STATS
     3 - QUIT (Are you sure that you want to quit?)
     """

    border = "=========================================================================================="

    credits = """
     Thank you for playing our game. Whether you won or lost doesn't matter, as long as you enjoyed.
     Hope you play our game again.

     BLASPHEMOUS CREATED BY:
         Francis Carlo Del Campo
         Miguel Liceralde III
         Mark Dunstan Gabor
         Daniel Javillonar
     """

    print(border)
    fade_in_text(welcome)
    print(border)
    fade_in_text(story)
    print(border)

    while True:
        print(menu)
        navchoice = input("Enter your choice: ")

        if navchoice == '1':
            print("You are now playing Blasphemous. You are in an empty temple, watch out for the enemies. The extra P marks your initial position.")
            play_game()
        elif navchoice == '2':
            print("These are your stats.")
            print("\nPlayer Stats:")
            print(f"Name: {player.name}")
            print(f"HP: {player.health}")
            print(f"Speed: {player.speed}")
            print(f"Attack: {player.attack}")
        elif navchoice == '3':
            print(credits)
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    # Move these lines to the global scope
    player = Entity("Hero", 100, 10, 20)
    width = 20
    height = 10
    num_enemies = 5

    grid = Grid(width, height)
    grid.generate_maze()  # Start generating maze from (1, 1) to ensure an open space
    player_x, player_y = (1, 1)

    enemies = [Entity(f"Enemy{i}", random.randint(20, 50), random.randint(5, 10), random.randint(5, 15)) for i in
               range(num_enemies)]
    enemy_positions = [grid.spawn_entity('E', random.randint(0, width - 1), random.randint(0, height - 1)) for _ in
                       range(num_enemies)]

    main()
