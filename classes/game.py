import random
from classes.magic import Spell



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m' #This is red
    ENDC = '\033[0m' #This ends the colors
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items", "Quit"]
        self.name = name

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    # def generate_spell_damage(self, i):
    #     mgl = self.magic[i]["dmg"] - 5
    #     mgh = self.magic[i]["dmg"] + 5
    #     return random.randrange(mgl, mgh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "ACTIONS:" +bcolors.ENDC)
        for item in self.actions:
            print("    " + str(i) + ".", item)
            i += 1

    def get_action_name(self, i):
        return self.actions[i]

    def choose_magic(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "MAGIC:" + bcolors.ENDC)
        for spell in self.magic:
            # print(str(i) +":", spell["name"], "(cost:", str(spell["cost"]) +")", "(dmg:", str(spell["dmg"]) +")")
            print("    " + str(i) +".", spell.name, "(cost:", str(spell.cost) +")", "(dmg:", str(spell.dmg) +")", "(type:", str(spell.type) +")")
            i += 1

    def choose_items(self):
        i = 1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "ITEMS:" + bcolors.ENDC)
        for item in self.items:
            print("    " + str(i) + ".", item.name, ":", item.description + ". x" + str(item.amount))
            i += 1

    def choose_target(self, enemies):
        i = 1

        print("\n" + bcolors.FAIL + bcolors.BOLD + "    TARGET:" + bcolors.ENDC)

        for enemy in enemies:
            print ("        " + str(i) + ".", enemy.name)
            i +=1

        choice = int(input("    Choose target:")) - 1
        return choice


    def get_enemy_stats(self):
        hp_bar = ""
        bar_ticks = (self.hp / self.maxhp) * 100 / 2

        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 11:
            decreased_hp = 11 - len(hp_string)

            while decreased_hp > 0:
                current_hp += " "
                decreased_hp -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        print(self.name)
        print(current_hp + "   |" + bcolors.FAIL +
              hp_bar + bcolors.ENDC +
              "|    ")

    def get_stats(self):

        hp_bar = ""
        hp_ticks = (self.hp / self.maxhp) * 100 / 4
        mp_bar = ""
        mp_ticks = (self.mp / self.maxmp) * 100 / 10

        while hp_ticks > 0:
            hp_bar += "█"
            hp_ticks -= 1
        while len(hp_bar) < 25:
            hp_bar += " "

        while mp_ticks > 0:
            mp_bar += "█"
            mp_ticks -= 1
        while len(mp_bar) < 10:
            mp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 11:
            decreased_hp = 11 - len(hp_string)

            while decreased_hp > 0:
                current_hp += " "
                decreased_hp -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        mp_string = str(self.mp) + "/" + str(self.maxmp)
        current_mp = ""

        if len(mp_string) < 7:
            decreased_mp = 7 - len(mp_string)

            while decreased_mp > 0:
                current_mp += " "
                decreased_mp -= 1

            current_mp += mp_string
        else:
            current_mp = mp_string

        print(self.name)
        print(current_hp +"   |" + bcolors.OKGREEN +
              hp_bar + bcolors.ENDC +
              "|   " + current_mp + "   |" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + "|")


    def choose_enemy_spell(self):

        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_spell_damage()
        print("The chosen spell type is", spell.type, ". The chosen spell name is", spell.name, ". The spell cost for it is", spell.cost)

        if self.mp > spell.cost:
            print("we have enough MPs")
            if spell.type == "White Magic" and self.hp < (self.maxhp * 0.5):
                print("the magic picked satisfied all conditions")
                return spell, magic_dmg
            elif spell.type == "Black Magic" and self.hp >= (self.maxhp * 0.5):
                print("this also satisfies the conditions")
                return spell, magic_dmg
            else:
                print("we have to try again")
                return self.choose_enemy_spell()
        else:
            print("we have to try again")
            return self.choose_enemy_spell()

