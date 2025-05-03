from Character import Character, Knight, Barbarian



def test_abilities_and_statuses():
    print("=== Testing Abilities and Status Effects ===\n")
        
    # Create characters
    knight = Knight("Sir Lancelot")
    barbarian = Barbarian("Conan")
        
    print(f"{knight.name}: HP={knight.health}, Strength={knight.strength}, Armor={knight.armor}")
    print(f"{barbarian.name}: HP={barbarian.health}, Strength={barbarian.strength}, Armor={barbarian.armor}\n")
        
    # Test knight's shield wall
    print("Knight uses Armor Up:")
    knight.use_ability("Armor Up", None)
    print(f"Knight's armor after Shield Wall: {knight.armor}")
    print(f"Knight's status effects: {knight.statuses}")
        
    # Test barbarian's berserker rage
    print("\nBarbarian uses Rage:")
    barbarian.use_ability("Rage", None)
    print(f"Barbarian's strength after rage: {barbarian.strength}")
    print(f"Barbarian's armor after rage: {barbarian.armor}")
    print(f"Barbarian's status effects: {barbarian.statuses}")
        
    # Test ground slam ability
    print("\nBarbarian uses Ground Stomp on Knight:")
    barbarian.use_ability("Ground Stomp", knight)
    print(f"Knight's status effects: {knight.statuses}")
        
    # In your test function after testing other abilities
    print("\nKnight uses Veteran Strike on Barbarian:")
    knight.use_ability("Veteran Strike", barbarian)
    print(f"Knight's health after healing: {knight.health}")
    
    # Test status update
    print("\nUpdating status effects (1 turn passes):")
    knight.update_statuses()
    barbarian.update_statuses()
    print(f"Knight's armor after update: {knight.armor}")
    print(f"Knight's status effects: {knight.statuses}")


def main():
    test_abilities_and_statuses()

if __name__ == "__main__":
    main()