import random

class Cell:
    def __init__(self, symbol, passable=True):
        self.symbol = symbol
        self.passable = passable

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[Cell('.') for _ in range(width)] for _ in range(height)]

    def spawn_entity(self, entity_symbol):
        x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        while self.cells[y][x].symbol != '.':
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        self.cells[y][x] = Cell(entity_symbol)
        return x, y

    def remove_entity(self, x, y):
        self.cells[y][x] = Cell('.')

    def print_grid(self, player_x, player_y):
        for y in range(self.height):
            for x in range(self.width):
                if x == player_x and y == player_y:
                    print('P', end=' ')
                else:
                    print(self.cells[y][x].symbol, end=' ')
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
    print(welcome)
    print(border)
    print(story)
    print(border)
    
    width = 20
    height = 10
    num_enemies = 3

    grid = Grid(width, height)
    player_x, player_y = grid.spawn_entity('P')

    player = Entity("Hero", 100, 10, 20)
    enemies = [Entity(f"Enemy{i}", random.randint(20, 50), random.randint(5, 10), random.randint(5, 15)) for i in range(num_enemies)]
    enemy_positions = [grid.spawn_entity('E') for _ in range(num_enemies)]
    
    while True:
        navchoice = input(menu)
        print(border)
        if navchoice == '1':
            print("You are now playing Blasphemous. You are in an empty temple, watch out for the enemies.")

            print("Welcome to the RPG Game!")

            while player.is_alive():
                grid.print_grid(player_x, player_y)
                print("\nPlayer Stats:")
                print(f"Name: {player.name}")
                print(f"HP: {player.health}")
                print(f"Speed: {player.speed}")
                print(f"Attack: {player.attack}")

                action = input("\nEnter 'w', 'a', 's', 'd' to move or 'q' to quit: ")

                if action == 'q':
                    print("You quit the game.")
                    break

                # Move player based on input
                new_player_x, new_player_y = player_x, player_y
                if action == 'w' and player_y > 0 and grid.cells[player_y - 1][player_x].passable:
                    new_player_y -= 1
                elif action == 'a' and player_x > 0 and grid.cells[player_y][player_x - 1].passable:
                    new_player_x -= 1
                elif action == 's' and player_y < height - 1 and grid.cells[player_y + 1][player_x].passable:
                    new_player_y += 1
                elif action == 'd' and player_x < width - 1 and grid.cells[player_y][player_x + 1].passable:
                    new_player_x += 1

                # Check for enemy encounters and attacks
                for enemy, (enemy_x, enemy_y) in zip(enemies, enemy_positions):
                    if (abs(new_player_x - enemy_x) == 1 and new_player_y == enemy_y) or \
                    (new_player_x == enemy_x and abs(new_player_y - enemy_y) == 1):
                        print(f"Encountered {enemy.name}!")
                        while player.is_alive() and enemy.is_alive():
                            grid.print_grid(new_player_x, new_player_y)
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
                                    break

                            elif action == 'q':
                                print("You ran away from the battle.")
                                break

                if player.is_alive():
                    player_x, player_y = new_player_x, new_player_y
        elif navchoice == '2':
            print("These are your stats.")
            print("\nPlayer Stats:")
            print(f"Name: {player.name}")
            print(f"HP: {player.health}")
            print(f"Speed: {player.speed}")
            print(f"Attack: {player.attack}")
        else:
            print(credits)
            quit()
            break


if __name__ == "__main__":
    main()
