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
curaga = Spell("Curaga", 50, 6000, "White Magic")

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, curaga]

# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50, 15)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100, 5)
superpotion = Item("Super-Potion", "potion", "Heals 500 HP", 500, 2)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999, 4)
megaelixir = Item("Mega-Elixir", "elixir", "Fully restores HP/MP of all party member", 9999, 1)
grenade = Item("Grenade", "attack", "Deals 500 damage points", 500, 1)

player_items = [potion, hipotion, superpotion, elixir, megaelixir, grenade]
enemy_items = [superpotion, grenade]

#Instantiated the Person class
player1 = Person(bcolors.OKBLUE + "Elliot" + bcolors.ENDC, 4800, 132, 311, 34, player_spells, player_items)
player2 = Person(bcolors.OKBLUE + "Théodore" + bcolors.ENDC, 4160, 188, 300, 34, player_spells, player_items)
player3 = Person(bcolors.OKBLUE + "Léopold" + bcolors.ENDC, 3089, 174, 288, 34, player_spells, player_items)

enemy1 = Person(bcolors.FAIL + "Un Petit Méchant" + bcolors.ENDC, 1250, 10, 560, 325, enemy_spells, []) #1250, 450
enemy2 = Person(bcolors.FAIL + "Le Gros Méchant" + bcolors.ENDC, 18200, 10, 1525, 25, enemy_spells, []) #18200 #650
enemy3 = Person(bcolors.FAIL + "Un Autre Petit Méchant" + bcolors.ENDC, 1250, 10, 560, 325, enemy_spells, []) #1250, 450

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0
print("=====================================================================")

while running:
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
        print("\n")
        print(bcolors.OKBLUE + "It is", player.name + "'s turn:" + bcolors.ENDC)
        print("*****")
        player.get_stats()
        player.choose_action()
        choice = input("Choose action: ")
        index = int(choice) - 1
        print("\n" + player.name, "chose", player.get_action_name(int(index)))

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

        # CHECK IF ALL ENEMIES ARE DEAD
        if len(enemies) == 0:
            print("\n\n")
            print("All enemies are dead")
            running = False
            break

        # ENEMY TURN
        attacker = random.randrange(0, len(enemies))
        target = random.randrange(0, len(players))
        print("The attacker will be", enemies[attacker].name, ", and their target will be", players[target].name)

        while True:
            attacker_choice = random.randrange(0, 3)

            if attacker_choice == 0: #ATTACK
                print("\n" + enemies[attacker].name, "chose", enemies[attacker].get_action_name(int(attacker_choice)))
                enemy_dmg = enemies[attacker].generate_damage()
                players[target].take_damage(enemy_dmg)
                print(bcolors.FAIL + enemies[attacker].name + bcolors.ENDC, "attacked", players[target].name, "for", enemy_dmg,
                      "points.")
                break

            elif attacker_choice == 1: #SPELL
                print("The attacker chose Magic")
                # if enemies[attacker].mp < min(spell.cost):
                #     print("We don't have enough MPs for any of the spells. Pick a different action.")
                #     continue
                if enemies[attacker].mp < 25:
                    print("We don't have enough MPs for any of the spells. Pick a different action.")
                    continue
                attacker_spell, attacker_magic_dmg = enemies[attacker].choose_enemy_spell()
                print("\n" + enemies[attacker].name, "chose", attacker_spell.type)
                if enemies[attacker].mp > attacker_spell.cost:
                    if attacker_spell.type == "White Magic":
                        enemies[attacker].heal(attacker_magic_dmg)
                        enemies[attacker].reduce_mp(attacker_spell.cost)
                        print(bcolors.FAIL + enemies[attacker].name + bcolors.ENDC, "used", attacker_spell.name, "to heal for", attacker_magic_dmg,
                              "points.")
                    elif attacker_spell.type == "Black Magic":
                        players[target].take_damage(attacker_magic_dmg)
                        enemies[attacker].reduce_mp(attacker_spell.cost)
                        print(bcolors.FAIL + enemies[attacker].name + bcolors.ENDC, "used", attacker_spell.name, "on", players[target].name, "for", attacker_magic_dmg,
                              "points.")
                else:
                    print("There are not enough MPs for this spell. Pick a different spell.")
                    continue
                break

            elif attacker_choice == 2: #ITEMS
                print("\n" + enemies[attacker].name, "chose", enemies[attacker].get_action_name(int(attacker_choice)))
                item_choice = random.randrange(0, len(enemy_items))
                item_dmg = enemy_items[item_choice].prop
                print("Attacker chose", enemy_items[item_choice].name)

                if enemy_items[item_choice].type == "potion" and enemies[attacker].hp <= (0.5 * enemies[attacker].maxhp):
                    print(enemies[attacker].name, "uses the", enemy_items[item_choice].name, "to heal for",
                          enemy_items[item_choice].prop, "points.")
                    enemies[attacker].heal(item_dmg)
                    enemy_items[item_choice].reduce_item_amount()
                    if enemy_items[item_choice].amount == 0:
                        enemy_items.remove(enemy_items[item_choice])
                    break
                elif enemy_items[item_choice].type == "attack" and enemies[attacker].hp > (0.5 * enemies[attacker].maxhp):
                    print(enemies[attacker].name, "attacked with the", enemy_items[item_choice].name, "to cause",
                          enemy_items[item_choice].prop, "points of damage.")
                    players[target].take_damage(item_dmg)
                    enemy_items[item_choice].reduce_item_amount()
                    if enemy_items[item_choice].amount == 0:
                        enemy_items.remove(enemy_items[item_choice])
                    break
                else:
                    print("No items are available at this time. Choose a different action.")
            continue

        # CHECK IF PLAYER IS DEAD
        if players[target].get_hp() == 0:
            print(bcolors.FAIL + players[target].name, "lost..." + bcolors.ENDC)
            players.remove(players[target])

        # CHECK IF ALL PLAYERS ARE DEAD
        if len(players) == 0:
            print("\n\n")
            print("All of the players are dead")
            running = False









