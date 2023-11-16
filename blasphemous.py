import random

class Player:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def attack_enemy(self, enemy):
        damage = random.randint(1, self.attack)
        enemy.take_damage(damage)
        return damage

class Enemy:
    def __init__(self, name, hp, attack, speed):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.speed = speed

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def attack_player(self, player):
        damage = random.randint(1, self.attack)
        player.take_damage(damage)
        return damage
    
    # Create def for speed.

# Create class and function declaration for map/maze.

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
3 - QUIT
"""

border = "====================================================================================="

print(border)
print(welcome)
print(border)
print(story)
print(border)
navchoice = input(menu)
print(border)

if navchoice == '1':
    print("You are now playing Blasphemous.")
elif navchoice == '2':
    print("These are your stats.")
else:
    quit()

