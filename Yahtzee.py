from random import choice, randint
from collections import Counter

DICE = [i for i in range(1, 7)]
RESET = "\033[0m"
HIGHLIGHT = "\033[7m"


def switch_player():
    global player
    player = player % 2 + 1

class Player():

    def __init__(self):
        self.section = [0 for i in range(11)]
        self.section_locked = [False for i in range(11)]
        self.dices = [1 for i in range(5)] # Valeurs par défaut
        self.locked_dices = [False for i in range(5)]
        self.remaining_roll = 3


    def new_roll(self):
        for i in range(len(self.dices)):
            if not self.locked_dices[i]:
                self.dices[i] = choice(DICE)


    def points_calculation(self):
        for i in range(6):
            if self.dices.count(i+1) > 0 and not self.section_locked[i]:
                self.section[i] = self.dices.count(i+1) * (i+1)
        
        if figure_detection(self.dices) == "brelan" and\
not self.section_locked[6]: self.section[6] = sum(self.dices)
        if figure_detection(self.dices) == "carre" :
            if not self.section_locked[7] : self.section[7] = sum(self.dices)
            if not self.section_locked[6] : self.section[6] = sum(self.dices)
        if figure_detection(self.dices) == "full" : 
            if not self.section_locked[8] : self.section[8] = 25
            if not self.section_locked[6] : self.section[6] = sum(self.dices)
        if figure_detection(self.dices) == "suite" and not self.section_locked[9] : self.section[9] = 40
        if figure_detection(self.dices) == "yazi" and not self.section_locked[10] : self.section[10] = 50 

    def reset_points(self):
        """réinitialise l'aperçut des points de la section (donc pas les points bloqués)"""
        for i in range(len(self.section)):
            if not self.section_locked[i]:
                self.section[i] = 0
    
    def reset_dice(self):
        self.locked_dices = [False for i in range(5)]
        self.remaining_roll = 3


player1 = Player()
player2 = Player()

points_p1 = 0
points_p2 = 0

player = randint(1, 2)
players = [None, player1, player2]

def finished():
    """Renvoie True si la partie est finie, False si la partie continue"""
    return all(player1.section_locked) and all(player2.section_locked)

def show_sections(section_p1, section_p2, section_locked_p1, section_locked_p2):
    
    section_list = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅",\
                    "■ ■ ■", "◉ ◉ ◉ ◉", "◆ ◆ ◆ ◉ ◉", "■ ◆ ◉ ▲ ★", "★ ★ ★ ★ ★"]
    
    print('\033c') # Clear la console
    
    points_addition()
    print(f"Joueur 1 : {points_p1} pts | Joueur 2 : {points_p2} pts")

    for i in range(len(section_list)):
        if section_locked_p1[i] and section_locked_p2[i]:
            print(f"{i+1:<2}) {section_list[i]:<12} : {HIGHLIGHT}{section_p1[i]:>2}{RESET} | \
{HIGHLIGHT}{section_p2[i]:>2}{RESET}")
        elif section_locked_p1[i] and not section_locked_p2[i]:
            print(f"{i+1:<2}) {section_list[i]:<12} : {HIGHLIGHT}{section_p1[i]:>2}{RESET} | {section_p2[i]:>2}")
        elif not section_locked_p1[i] and section_locked_p2[i]:
            print(f"{i+1:<2}) {section_list[i]:<12} : {section_p1[i]:>2} | {HIGHLIGHT}{section_p2[i]:>2}{RESET}")
        else:
            print(f"{i+1:<2}) {section_list[i]:<12} : {section_p1[i]:>2} | {section_p2[i]:>2}")

def show_dices(dices, locked_dices):
    
    dices_list = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    dices_str = ""
    for i in range(len(dices)):
        if locked_dices[i]:
            dices_str += f"{HIGHLIGHT}{str(dices_list[dices[i]-1])} {RESET}"
        else:
            dices_str += f"{str(dices_list[dices[i]-1])} "
    print(dices_str)

def points_addition():

    global points_p1
    global points_p2

    sum_indice_p1 = []
    sum_indice_p2 = []
    
    for i in range(len(player1.section_locked)):
        if player1.section_locked[i]:
            sum_indice_p1.append(i)
    
    for i in range(len(player2.section_locked)):
        if player2.section_locked[i]:
            sum_indice_p2.append(i)

    points_p1 = sum(player1.section[i] for i in sum_indice_p1)
    points_p2 = sum(player2.section[i] for i in sum_indice_p2)

    return points_p1, points_p2

def figure_detection(dices):
    """Détecte les différentes figures à partir d'une liste de dés"""
    counts = Counter(dices).values()
    if 5 in counts:
        return "yazi"  # Yahtzee
    if 4 in counts:
        return "carre"  # Carré
    if 3 in counts and 2 in counts:
        return "full"  # Full
    if 3 in counts:
        return "brelan"  # Brelan 
    if sorted(set(dices)) in ([1, 2, 3, 4, 5], [2, 3, 4, 5, 6]):
        return "suite"  # Suite
    return None

def section_locking(player):
    section = input("Choix de la figure (enter to skip) :")
    if not section or len(section) > 2 or int(section) > 11 or int(section)<1:
        return
    elif player.section_locked[int(section)-1] :
        input("figure déjà bloquée !")
        return
    else:
        player.section_locked[int(section)-1] = True
        switch_player()
        player.reset_points()
        player.reset_dice()

def dice_locking(player):
    if player.remaining_roll > 0:
        dice = input("Choix du blocage des dés ex: 1 2 3.. :")
        try:
            if not dice.strip():
                print("Aucun dé sélectionné.")
                return
            
            dice_list = [int(x) for x in dice.split()]

            if len(dice_list) > 5:
                print("Erreur : 5 dés maxium")
                return
            
            for lock in dice_list:
                if 1 <= lock <= 5:
                    player.locked_dices[lock-1] = not player.locked_dices[lock-1]
                else:
                    print(f"Dé numéro {lock} non valide. Les dés vont de 1 à 5")
        except ValueError:
            print("Erreur: les chiffres doivent être séparés par des espaces")


def dice_rolling(player, force=False):
    if player.remaining_roll > 0:
        if force:
            request = input("Lancement des dés...")
        else:
            request = input(f"Lancer les dés ? (y/m or None) ({player.remaining_roll} restants) :")


        if force or request == "y" or request == "m":
            player.remaining_roll -= 1
            player.new_roll()
            player.reset_points()
            player.points_calculation()
        else:
            print("dés non lancés")
    else:
        print("Pas de relance possible...")


def game_loop():
    show_sections(player1.section, player2.section, player1.section_locked, player2.section_locked)
    print(f"Au tour du joueur {player} !")
    while not finished():
        current_player = players[player]
        current_nbplayer = player
        dice_rolling(current_player, True)
        while current_nbplayer == player:
            show_sections(player1.section, player2.section, player1.section_locked, player2.section_locked)
            print(f"Au tour du joueur {player} !")
            print("\n--------------------\n")
            show_dices(current_player.dices, current_player.locked_dices)
            dice_locking(current_player)
            dice_rolling(current_player)
            section_locking(current_player)

        
        show_sections(player1.section, player2.section, player1.section_locked, player2.section_locked)
        print(f"Au tour du joueur {player} !")

    print(f"Le joueur 1 a {points_p1} points et le joueur 2 a {points_p2} points")
    if points_p1 > points_p2 : print("Le joueur 1 a gagné !")
    if points_p1 < points_p2 : print("Le joueur 2 a gagné !")
    if points_p1 == points_p2 : print("égalité !")

game_loop()
