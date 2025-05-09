from Character import Character, Knight, Barbarian, Cleric, Druid
from battlemanagement import CombatManager
import time

def main():
    print("=== Fantasy Tournament ===")
    print("Welcome to the arena!\n")

    combat_manager = CombatManager()

    barbarian = Barbarian("Conan")
    knight = Knight("Sir Loyns")
    cleric = Cleric("Dustin")
    druid = Druid("Karmine")

    barbarian.team = "Team A"
    knight.team = "Team B"
    cleric.team = "Team B"
    druid.team = "Team A"

    combat_manager.add_participants(barbarian)
    combat_manager.add_participants(knight)
    combat_manager.add_participants(cleric)
    combat_manager.add_participants(druid)

    print("\nToday's Match:")
    print("Team A:")
    print(f"   {barbarian.name} the Barbarian!")
    print(f"   {druid.name} the Druid!")

    print("\nTeam B:")
    print(f"   {knight.name} the Knight!")
    print(f"   {cleric.name} the Cleric!")

    input("\nPress Enter to begin the battle...")

    round_number = 1
    max_rounds = 20

    while combat_manager.is_combat_active and round_number <= max_rounds:
        print(f"\n=== Round {round_number} ===")

        result = combat_manager.run_simulation()

        for msg in result:
            print(msg)
            time.sleep(0.5)

        print("\nStatus after round:")
        for character in combat_manager.participants:
            status = "Alive" if character.is_alive() else "Defeated"
            print(f"{character.name}: HP {character.health}/{character.max_health} - {status}")

        if not combat_manager.is_combat_active:
            print("\nThe battle has ended!")

            teams_alive = {}
            for character in combat_manager.participants:
                if character.is_alive():
                    teams_alive[character.team] = teams_alive.get(character.team, 0) + 1

            if len(teams_alive) == 0:
                print("It's a draw! all combatants have fallen!")
            else:
                winner = max(teams_alive, key=teams_alive.get)
                print(f"{winner} is victorious!")

        round_number += 1

        if combat_manager.is_combat_active:
            input("\nPress Enter for the next round...")

    if round_number > max_rounds and combat_manager.is_combat_active:
        print(f"\nMaximum rounds ({max_rounds}) reached!")
        print("The battle ends in a stalemate!")

    print("\nBattle Ended!")
    print("Final Status:")
    for character in combat_manager.participants:
        status = "Alive" if character.is_alive() else "Defeated"
        print(f"{character.name} ({character.type_name}) - {status}")
        print(f" HP: {character.health}/{character.max_health}")
        print(f" Mana: {character.mana}/{character.max_mana}")
        
    team_survivors = {}
    for character in combat_manager.participants:
        if character.is_alive():
            team_survivors[character.team] = team_survivors.get(character.team, 0) + 1
        
    if len(team_survivors) == 0:
        print("\nThe battle ends in a draw! All combatants have fallen!")

    elif len(team_survivors) == 1:
        winning_team = list(team_survivors.keys())[0]
        print(f"\n{winning_team} emerges victorious!")
    else:
        team_with_most = max(team_survivors, key=team_survivors.get)
        print(f"\n{team_with_most} claims a narrow victory with {team_survivors[team_with_most]} survivors!")

    print("\nThank you for attending Fantasy Tournament!")

if __name__ == "__main__":
    main()