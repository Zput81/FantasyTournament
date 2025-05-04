import random

class Character:
    def __init__(self, name):
        self.name = name
        
        self.strength = 10
        self.vitality = 10
        self.dexterity = 10
        self.intelligence = 10
        self.luck = 10

        self.armor = 10
        self.armor_threshold = self.calculate_armor_threshold()
        
        self.max_health = self.calculate_max_health()
        self.health = self.max_health
        
        self.max_mana = self.calculate_max_mana()
        self.mana = self.max_mana
        
        self.dodge_chance = self.calculate_dodge()
        self.critical_chance = self.calculate_critical()

        self.abilities = {}
        self.statuses = {}

        self.team = "neutral"

    def calculate_max_health(self):
        base_health = 15
        health_bonus = (self.vitality * 0.5)
        return int(base_health + health_bonus)
    
    def calculate_max_mana(self):
        base_mana = 15
        mana_bonus = (self.intelligence * 0.5)
        return int(base_mana + mana_bonus)
    
    def calculate_dodge(self):
        base_dodge = 5 + (self.dexterity * 0.8)
        luck_bonus = self.luck * 0.5
        return round(base_dodge + luck_bonus, 1)
    
    def calculate_critical(self):
        base_critical = 5 + (self.strength * 0.5)
        luck_bonus = self.luck * 0.5
        return round(base_critical + luck_bonus, 1)
    
    def calculate_armor_threshold(self):
        return int(5 + self.armor // 4)
    
    def take_damage(self, attack_damage, effective_threshold):
        print(f"debug: {self.name} has {self.armor} with a threshold of {effective_threshold}")
        print(f"debug: incoming damage is {attack_damage}")
        if attack_damage <= effective_threshold:
            print(f"{self.name}'s armor absorbed the blow!")
            return 0
        
        damage_reduction = self.armor * 0.1
        print(f"debug: reducing damage by {damage_reduction}")
        actual_damage = max(1, round(attack_damage - damage_reduction, 1))
        self.health = round(self.health - actual_damage, 1)
        print(f"{self.name} takes {actual_damage:.1f} of damage!")

        if self.health <= 0:
            self.health = 0
            print(f"{self.name} has been defeated!")
        
        return actual_damage
    
    def calculate_base_damage(self):
        base_damage = (self.strength * 0.5)
        variance = random.uniform(0.75, 1.25)
        return round(base_damage * variance, 1)
    
    def attack(self, target):
        is_critical = self.roll_for_critical()
        is_dodge = self.roll_for_dodge()
        damage = self.calculate_base_damage()
        if is_critical:
            damage = round(damage * 1.75, 1)
            armor_penetration = target.armor_threshold * 0.5
            print(f"{self.name} lands a CRITICAL HIT!")
        else:
            armor_penetration = 0

        effective_threshold = max(0, target.armor_threshold - armor_penetration)

        if is_critical and is_dodge:
            partial_damage = round(damage * random.uniform(0.25, 0.5), 1)
            target.health -= partial_damage
            print(f"{target.name} partially dodged {self.name}'s critial hit and takes {partial_damage} damage!")
            return partial_damage

        if target.roll_for_dodge():
            print(f"{target.name} dodges {self.name}'s attack!")
            return 0
        
        final_damage = target.take_damage(damage, effective_threshold)
        return final_damage
    
    def roll_for_critical(self):
        crit_roll = random.randint(1, 100)
        return crit_roll <= self.critical_chance
    
    def roll_for_dodge(self):
        dodge_roll = random.randint(1, 100)
        return dodge_roll <= self.dodge_chance
    
    def apply_status(self, status_name, duration, **effect_params):
        self.statuses[status_name] = {
            "duration": duration,
            "params": effect_params
        }

        message = None

        if status_name == "armor_up":
            self.armor += effect_params.get("armor_bonus", 15)
            message = f"{self.name} gains armor up (+{effect_params.get('armor_bonus', 15)} armor"
        elif status_name == "rage":
            self.strength += effect_params.get("bonus_strength", 10)
            self.armor -= effect_params.get("armor_loss", 5)
            message = f"{self.name} enters a rage (+{effect_params.get('bonus_strength', 10)} strength (- {effect_params.get('armor_loss', 5)}) armor)"
        elif status_name == "stun":
            message = f"{self.name} is stunned and cannot act"

    def can_act(self):
        if "stun" in self.statuses:
            return False
        return self.is_alive()

    def process_status_effect_at_turn_start(self):
        results = []

        return results
    
    def process_status_effects_at_turn_end(self):
        results = []

        for status_name in list(self.statuses.keys()):
            self.statuses[status_name]["duration"] -= 1

            if self.statuses[status_name]["duration"] <= 0:
                message = f"{status_name} has worn of from {self.name}"
                results.append(message)
                self.remove_status_effect(status_name)
        
        return results

    def remove_status_effect(self, status_name):
        if status_name not in self.statuses:
            return
        
        params = self.statuses[status_name]["params"]

        if status_name == "armor_up":
            self.armor -= params.get("armor_bonus")
            print(f"{self.name}'s armor up fades.")
        elif status_name == "rage":
            self.strength -= params.get("bonus_strength", 10)
            self.armor -= params.get("armor_loss", 5)
            print(f"{self.name} calms down")
        elif status_name == "stun":
            print(f"{self.name} is no longer stunned.")

        del self.statuses[status_name]

    def add_abilities(self):
        self.abilities = {}

    def add_ability(self, name, cost, description, effect_function):
        self.abilities[name] = {
            "cost": cost,
            "description": description,
            "effect": effect_function
        }

    def use_ability(self, ability_name, target=None):
        if ability_name not in self.abilities:
            print(f"{self.name} doesn't know {ability_name}.")
            return False

        if self.mana < self.abilities[ability_name]["cost"]:
            print(f"{self.name} doesn't have enough mana to use {ability_name}.")
            return False
        
        self.mana -= self.abilities[ability_name]["cost"]
        print(f"{self.name} uses {ability_name}!")

        return self.abilities[ability_name]["effect"](self, target)
    
    def is_alive(self):
        return self.health > 0
    
    def set_team(self, team_name):
        self.team = team_name
        return f"{self.name} is now aligned with team {team_name}"
    
    def choose_action(self, targets):
        valid_targets = [target for target in targets
                         if target.team != self.team and target.is_alive()]
        
        if not valid_targets:
            return {"type": "pass"}
        
        chosen_target = random.choice(valid_targets)

        return {
            "type": "attack",
            "target": chosen_target
        }
    
class Barbarian(Character):
    def __init__(self, name):
        super().__init__(name)
        self.strength += 5
        self.vitality += 3
        self.intelligence -= 3
        self.luck += 1

        self.max_health = self.calculate_max_health()
        self.max_mana = self.calculate_max_mana()

        self.armor -= 4
        self.armor_threshold = self.calculate_armor_threshold()

        self.health = self.max_health
        self.mana = self.max_mana

        self.initialize_abilities()

    def calculate_base_damage(self):
        base = self.strength * 0.6
        return round(base * random.uniform(0.9, 1.1), 1)
    
    def initialize_abilities(self):

        def rage_effect(self, target=None):
            bonus_strength = 10
            armor_loss = 5
            self.strength += bonus_strength
            self.armor -= armor_loss
            self.apply_status("rage", 3, bonus_strength=bonus_strength, armor_loss=armor_loss)
            print(f"{self.name} begins to rage.")
            return True
        
        self.add_ability("Rage", 5, "Increases strength and health at the loss of armor for 3 turns", rage_effect)

        def ground_stomp_effect(self, target):
            damage = self.strength * 0.5
            print(f"{self.name} slams the ground causing {damage} damage.")
            effective_threshold = 5
            target.take_damage(damage, effective_threshold)
            target.apply_status("stun", 1)
            print("All enemies are stunned for 1 turn")
            return True
        
        self.add_ability("Ground Stomp", 10, "Damages and stuns all enemies for 1 turn", ground_stomp_effect)

class Knight(Character):
    def __init__(self, name):
        super().__init__(name)
        self.strength += 3
        self.vitality += 4
        self.dexterity -= 2
        self.luck -= 1

        self.max_health = self.calculate_max_health()
        self.max_mana = self.calculate_max_mana()

        self.armor += 8
        self.armor_threshold = self.calculate_armor_threshold()

        self.health = self.max_health
        self.mana = self.max_mana

        self.initialize_abilities()

    def calculate_base_damage(self):
        base = self.strength * 0.5
        return round(base * random.uniform(0.9, 1.1), 1)
        
    def initialize_abilities(self):

        def armor_up_effect(user, target=None):
            bonus_armor = 15
            user.armor += bonus_armor
            user.apply_status("armor_up", 3, armor_bonus=bonus_armor)
            print(f"{user.name}'s armor increased by {bonus_armor}.")
            return True
        
        self.add_ability("Armor Up", 5, "Increases armor for 3 turns", armor_up_effect)

        def veteran_strike_effect(self, target):
            if not target:
                print("This ability needs a target.")
                return False
            
            damage = self.strength * 1.5
            effective_threshold = 8
            target.take_damage(damage, effective_threshold)
            heal_amount = round(damage * 0.3,1)
            heal_amount = round(heal_amount, 1)
            self.health = round(min(self.max_health, self.health + heal_amount), 1)
            print(f"{self.name} regained {heal_amount} health.")
            return True
        
        self.add_ability("Veteran Strike", 10, "Strikes target and regains a portion of damage as health", veteran_strike_effect)