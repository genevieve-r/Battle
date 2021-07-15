from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Create Black Magic
fire = Spell("Fire", 25, 80, "Black Magic")
thunder = Spell("Thunder", 25, 140, "Black Magic")
blizzard = Spell("Blizzard", 25, 100, "Black Magic")
meteor = Spell("Meteor", 40, 200, "Black Magic")
quake = Spell("Quake", 15, 140, "Black Magic")


# Create White Magic
cure = Spell("Cure", 25, 120, "White Magic")
cura = Spell("Cura", 32, 200, "White Magic")

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, cure]


# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50, 15)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100, 5)
superpotion = Item("Super-Potion", "potion", "Heals 500 HP", 500, 2)

elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999, 4)
megaelixir = Item("Mega-Elixir", "elixir", "Fully restores HP/MP of all party member", 9999, 1)

grenade = Item("Grenade", "attack", "Deals 500 damage points", 500, 1)

player_items = [potion, hipotion, superpotion, elixir, megaelixir, grenade]

#Instantiated the Person class
player1 = Person(bcolors.OKBLUE + "Elliot" + bcolors.ENDC, 4800, 132, 311, 34, player_spells, player_items)
player2 = Person(bcolors.OKBLUE + "Théodore" + bcolors.ENDC, 4160, 188, 300, 34, player_spells, player_items)
player3 = Person(bcolors.OKBLUE + "Léopold" + bcolors.ENDC, 3089, 174, 288, 34, player_spells, player_items)

#enemy1 = Person(bcolors.FAIL + "Le Gros Méchant" + bcolors.ENDC, 18200, 701, 1525, 25, [], [])
enemy1 = Person(bcolors.FAIL + "Un Petit Méchant" + bcolors.ENDC, 1250, 130, 560, 325, enemy_spells, [])
enemy2 = Person(bcolors.FAIL + "Le Gros Méchant" + bcolors.ENDC, 4200, 701, 1525, 25, enemy_spells, []) #18200
enemy3 = Person(bcolors.FAIL + "Un Autre Petit Méchant" + bcolors.ENDC, 1250, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

# print(player1.get_hp())
# print(player1.hp)

running = True
i = 0
print("=====================================================================")

while running:
    # print("I'm a little teapot")
    # print(players)

    for player in players:
        print("=====================================================================")
        player.get_stats()

    print("=====================================================================")
    for enemy in enemies:
        print("=====================================================================")
        enemy.get_enemy_stats()

    print("=====================================================================")

    for player in players:
        print("=====================================================================")
        # print("\n")
        # print(bcolors.FAIL + bcolors.BOLD + enemy.name, "attacks!" + bcolors.ENDC)
        # print("*****")
        #print("Enemy HP:", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC + "\n")
        # enemy.get_enemy_stats()
        print("\n")
        print(bcolors.OKBLUE + "It is", player.name + "'s turn:" + bcolors.ENDC)
        print("*****")
        player.get_stats()

        player.choose_action()
        choice = input("Choose action: ")
        index = int(choice) - 1

        print("\n" + player.name, "chose", player.get_action_name(int(index)))
        #enemy = player.choose_target(enemies)

        #ATTACK
        if index == 0: #Attack
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print(bcolors.OKBLUE + player.name, "attacked", enemies[enemy].name, "for", dmg, "points." + bcolors.ENDC)

            if enemies[enemy].get_hp() == 0:
                print(bcolors.FAIL + enemies[enemy].name, "lost!" + bcolors.ENDC)
                enemies.remove(enemies[enemy])

        #MAGIC SPELLS
        elif index == 1: #Magic
            player.choose_magic()
            magic_choice = int(input("Choose spell: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_spell_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP, choose again\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "Black Magic":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(dmg)
                #enemy.take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name, "deals", str(magic_dmg), "points of damage to", enemies[enemy].name, "." + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(bcolors.FAIL + enemies[enemy].name, "lost!" + bcolors.ENDC)
                    enemies.remove(enemies[enemy])

            elif spell.type == "White Magic":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name, "gives you", str(magic_dmg), "hit points back." + bcolors.ENDC)

        #ITEMS
        elif index == 2: #items
            while True:
                player.choose_items()
                item_choice = int(input("Choose item: ")) - 1

                if item_choice == -1:
                    continue

                item = player.items[item_choice]
                item_quantity = item.get_item_amount()

                if item_quantity == 0:
                    print(bcolors.FAIL + "\n Item exhausted. Choose a different item. \n" + bcolors.ENDC)
                    continue


                if item.type == "potion":
                    player.heal(item.prop)
                    print(bcolors.OKGREEN + "\n" + item.name, "heals for", item.prop, "HP" + bcolors.ENDC)
                elif item.type == "elixir":
                    if item.name == "Mega-Elixir":
                        for player in players:
                            player.hp = player.maxhp
                            player.mp = player.maxmp
                    else:
                        player.hp = player.maxhp
                        player.mp = player.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name, "fully restores HP/MP" + bcolors.ENDC)
                elif item.type == "attack":
                    enemy = player.choose_target(enemies)
                    enemies[enemy].take_damage(item.prop)
                    print(bcolors.FAIL + "\n" + item.name, "deals", item.prop, "points of damage to", enemies[enemy].name, "." + bcolors.ENDC)

                    if enemies[enemy].get_hp() == 0:
                        print(bcolors.FAIL + enemies[enemy].name, "lost!" + bcolors.ENDC)
                        enemies.remove(enemies[enemy])

                item.reduce_item_amount()
                break

        # QUIT
        elif index == 3:  # Quit
            print("\n" + "Au revoir")
            running = False
            break

        # if enemies[enemy].get_hp() == 0:
        #     print(bcolors.FAIL + enemies[enemy].name, "lost!" + bcolors.ENDC)
        #     enemies.remove(enemies[enemy])

        if len(enemies) == 0:
            print("\n\n")
            print("All enemies are dead")
            running = False


        attacker = random.randrange(0, len(enemies))
        attacker_choice = random.randrange(0, 3)
        target = random.randrange(0, len(players))
        # print("\n" + enemies[attacker].name, "chose", enemies[attacker].get_action_name(int(enemy_choice)))
        #
        # enemy_dmg = enemies[attacker].generate_damage()
        # enemy_choice = 1 #Enemy attacks
        # enemy_dmg = enemies[0].generate_damage()

        if attacker_choice == 0: #ATTACK
            print("\n" + enemies[attacker].name, "chose", enemies[attacker].get_action_name(int(attacker_choice)))
            enemy_dmg = enemies[attacker].generate_damage()
            #target = random.randrange(0, len(players))  # why did using len(players) -1 not work here? because randrange goes up to but does not include
            players[target].take_damage(enemy_dmg)
            print(bcolors.FAIL + enemies[attacker].name + bcolors.ENDC, "attacked", players[target].name, "for", enemy_dmg,
                  "points.")
        elif attacker_choice == 1: #SPELL
            spell, magic_dmg = enemies[attacker].choose_enemy_spell()
            enemies[attacker].reduce_mp(spell.cost)
            # print("The spell type is", spell.type)
            # print("\n" + enemies[enemy].name, "chose", enemies[enemy].get_action_name(int(enemy_choice)))
            print("\n" + enemies[attacker].name, "chose", spell.type)

            if spell.type == "White Magic":
                enemies[attacker].heal(magic_dmg)
                print(bcolors.FAIL + enemies[attacker].name + bcolors.ENDC, "used", spell.name, "to heal for", magic_dmg,
                      "points.")
            elif spell.type == "Black Magic":
                players[target].take_damage(magic_dmg)
                print(bcolors.FAIL + enemies[attacker].name + bcolors.ENDC, "used", spell.name, "on", players[target].name, "for", magic_dmg,
                      "points.")

            # if enemies[enemy].get_hp() < enemies[enemy].get_max_hp(): #use cure item
            #     spell.type == "white"
            #     enemies[enemy].heal(magic_dmg)
            #     print(bcolors.FAIL + enemies[enemy].name + bcolors.ENDC, "used", spell.name, "to heal for", magic_dmg,
            #           "points.")
            # else:
            #     spell.type = "black"
            #     players[target].take_damage(magic_dmg)
            #     print(bcolors.FAIL + enemies[enemy].name + bcolors.ENDC, "used", spell.name, "on", players[target].name, "for", magic_dmg,
            #       "points.")



        elif attacker_choice == 2: #ITEMS
            print("\n" + enemies[attacker].name, "chose", enemies[attacker].get_action_name(int(attacker_choice)))
            # if enemies[enemy].get_hp() < enemies[enemy].get_max_hp(): #use cure item
            #
            # else: #use attack item

        # print("There are", len(players), "players remaining")

        # target = random.randrange(0, len(players)) #why did using len(players) -1 not work here? because randrange goes up to but does not include
        # players[target].take_damage(enemy_dmg)
        # print(bcolors.FAIL + enemies[enemy].name + bcolors.ENDC,  "attacked", players[target].name, "for", enemy_dmg, "points.")
        # print("this is the current target:", players[target].name)
        # print("target hp:", players[target].get_hp())

        if players[target].get_hp() == 0:
            print(bcolors.FAIL + players[target].name, "lost..." + bcolors.ENDC)
            players.remove(players[target])

        if len(players) == 0:
            print("\n\n")
            print("All of the players are dead")
            running = False









