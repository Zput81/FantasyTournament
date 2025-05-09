import random

class Character:
    def __init__(self, name):
        self.name = name
        
        self.strength = 10
        self.vitality = 10
        self.dexterity = 10
        self.intelligence = 10
        self.luck = 10
        self.speed = 10

        self.armor = 8
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
    
    def calculate_mana_regen(self):
        return 3 + (self.intelligence * 0.2)
    
    def regenerate_mana(self):
        regen_amount = self.calculate_mana_regen()
        self.mana = min(self.mana + regen_amount, self.max_mana)
        return regen_amount
    
    def take_damage(self, attack_damage, effective_threshold):
        
        if attack_damage <= effective_threshold:
            return {"damage": 0, "absorbed": True}
        
        damage_reduction = self.armor * 0.1
       
        actual_damage = max(1, round(attack_damage - damage_reduction, 1))
        self.health = round(self.health - actual_damage, 1)

        if self.health <= 0:
            self.health = 0

        
        return {"damage": actual_damage, "absorbed": False}
    
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
        else:
            armor_penetration = 0

        effective_threshold = max(0, target.armor_threshold - armor_penetration)

        result = {"is_critical": is_critical, "is_dodge": is_dodge}

        if is_dodge and not is_critical:
            result["damage"] = 0
            result["effect_description"] = f"{target.name} dodges {self.name}'s attack."
            return result
        
        elif is_critical and is_dodge:
            partial_damage = round(damage * random.uniform(0.25, 0.5), 1)
            damage_result = target.take_damage(partial_damage, effective_threshold)
            
            result["damage"] = damage_result["damage"]
            result["absorbed"] = damage_result.get("absorbed", False)

            if damage_result.get("absorbed", False):
                result["description"] = f"{target.name}'s armor partially absorbed {self.name}'s critical."
            else:
                result['description'] = f"{target.name} partially dodges {self.name}'s critical hit and takes {damage_result['damage']} damage."
        
        else:
            damage_result = target.take_damage(damage, effective_threshold)
            result["damage"] = damage_result["damage"]
            result["absorbed"] = damage_result.get("absorbed", False)
            
            if damage_result.get("absorbed", False):
                result["description"] = f"{target.name}'s armor absorbed {self.name}'s blow."
            else:
                if is_critical:
                    result["description"] = f"{target.name} takes {damage_result['damage']} damage from {self.name}'s critical hit"
                else:
                    result["description"] = f"{target.name} takes {damage_result['damage']} damage from {self.name}'s attack."

        return result
    
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

    def process_status_effects_at_turn_start(self):
        results = []

        return results
    
    def process_status_effects_at_turn_end(self):
        results = []

        for status_name in list(self.statuses.keys()):
            self.statuses[status_name]["duration"] -= 1

            if self.statuses[status_name]["duration"] <= 0:
                message = f"{status_name} has worn off from {self.name}"
                results.append(message)
                self.remove_status_effect(status_name)
        
        return results
    
    def update_statuses(self):
        regen_amount = self.calculate_mana_regen()
        self.mana = min(self.mana + regen_amount, self.max_mana)
        print(f"{self.name} regenerated {regen_amount:.1f} mana.")
        
        status_keys = list(self.statuses.keys())

        for status in status_keys:
            self.statuses[status]['duration'] -= 1

        if self.statuses[status]['duration'] <= 0:
            if status == 'rage':
                self.strength -= self.statuses[status]['params']['bonus_strength']
                self.armor += self.statuses[status]['params']['armor_loss']
                print(f"{self.name}'s rage subsides.")
            elif status == 'armor_up':
                self.armor -= self.statuses[status]['params']['armor_bonus']
                print(f"{self.name}'s armor returns to normal.")

            elif status == 'stun':
                print(f"{self.name} is no longer stunned.")

            del self.statuses[status]

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

    def add_ability(self, name, cost, description, effect_function, is_aoe=False):
        self.abilities[name] = {
            "cost": cost,
            "description": description,
            "effect": effect_function,
            "is_aoe": is_aoe
        }

    def use_ability(self, ability_name, target=None, all_enemies=None):
        if ability_name not in self.abilities:
           return {
               "type": "error",
               "description": f"{self.name} doesn't know {ability_name}."
           }
        ability = self.abilities[ability_name]

        if self.mana < ability["cost"]:
            return {
                "type": "error",
                "description": f"{self.name} doesn't have enough mana to use {ability_name}."
            }
        
        self.mana -= ability["cost"]

        if ability.get("is+aoe", False):
            return ability["effect"](self, all_enemies)
        else:
            return ability["effect"](self, target)
    
    def is_alive(self):
        return self.health > 0
    
    def is_defeated(self):
        
        return not self.is_alive()
    
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
        self.type_name = "Barbarian"
        self.strength += 5
        self.vitality += 3
        self.intelligence -= 3
        self.luck += 1
        self.speed = 9

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
            if "rage" in self.statuses:
                return{
                    "type":"ability",
                    "name": "Rage",
                    "description": " is already raging.",
                    "failed": True
                }
            
            current_turn = getattr(self, 'current_turn', 0)
            last_rage_turn = getattr(self, 'last_rage_turn', -999)

            if current_turn - last_rage_turn < 3:
                return {
                    "type": "ability",
                    "name": "Rage",
                    "description": " tries to rage but is too tired.",
                    "failed": True
                }
            
            
            bonus_strength = 10
            armor_loss = 5
            self.strength += bonus_strength
            self.armor -= armor_loss
            self.apply_status("rage", 3, bonus_strength=bonus_strength, armor_loss=armor_loss)

            self.last_rage_turn = current_turn

            return{
                "type": "ability",
                "name": "Rage",
                "description": " begins to Rage!",
            }
        
        self.add_ability("Rage", 5, "Increases strength and health at the loss of armor for 3 turns", rage_effect, is_aoe=True)

        def ground_stomp_effect(self, target):
            damage = self.strength * 0.5
            effective_threshold = 5
            target.take_damage(damage, effective_threshold)
            target.apply_status("stun", 1)
            return {
                "type": "ability",
                "name": "Ground Stomp",
                "description": " slams the ground at ",
                "effect_description": f"causing {damage} damage. All enemies stunned for 1 turn."
            }
        
        self.add_ability("Ground Stomp", 10, "Damages and stuns all enemies for 1 turn", ground_stomp_effect)

    def choose_action(self, targets):
        valid_enemies = [t for t in targets if t.team != self.team and t.is_alive()]

        if not valid_enemies:
            return lambda x: {"description": " does nothing.", "effect_description": "no effect."}, None
        
        possible_actions = []

        if len(valid_enemies) >= 2 and "ground_stomp" in self.abilities and self.mana >= self.abilities["ground_stomp"]["cost"]:
           possible_actions.append(("ground_stomp", valid_enemies, True))
        
        current_turn = getattr(self, 'current_turn', 0)
        last_rage_turn = getattr(self, 'last_rage_turn', -999)
        rage_cooldown = 3
        
        if "Rage" in self.abilities and self.mana >= self.abilities["Rage"]["cost"]:
            if (self.health <= self.max_health * 0.5 and "rage" not in self.statuses and current_turn - last_rage_turn >= rage_cooldown):
                self.last_rage_turn = current_turn
                possible_actions.append(("Rage", self, True))

        if possible_actions:
            return random.choice(possible_actions)

        target = random.choice(valid_enemies)
        return self.attack, target, False

class Knight(Character):
    def __init__(self, name):
        super().__init__(name)
        self.type_name = "Knight"
        self.strength += 3
        self.vitality += 4
        self.dexterity -= 2
        self.luck -= 1
        self.speed = 8

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

        def armor_up_effect(self, target=None):
            bonus_armor = 15
            self.armor += bonus_armor
            self.apply_status("armor_up", 3, armor_bonus=bonus_armor)
            return{
                "type": "ability",
                "name": "Armor Up",
                "description": f"{self.name}'s armor increased by {bonus_armor}"
            }
        
        self.add_ability("Armor Up", 5, "Increases armor for 3 turns", armor_up_effect)

        def veteran_strike_effect(self, target):
            if not target:
               return {
                   "type": "ability",
                   "name": "Veteran Strike",
                    "description": "This ability needs a target.",
                    "failed": True
               }
            
            damage = self.strength * 1.5
            effective_threshold = 8
            damage_result = target.take_damage(damage, effective_threshold)
            heal_amount = round(damage * 0.3,1)
            heal_amount = round(heal_amount, 1)
            self.health = round(min(self.max_health, self.health + heal_amount), 1)
            return {
               "type": "ability",
               "name": "Veteran Strike",
                "description": f"{target.name} takes {damage_result['damage']} damage from {self.name}'s powerful strike."
                }
        
        self.add_ability("Veteran Strike", 10, "Strikes target and regains a portion of damage as health", veteran_strike_effect)

    def choose_action(self, targets):
        valid_enemies = [t for t in targets if t.team != self.team and t.is_alive()]

        if not valid_enemies:
            return lambda x: {"description": " does nothing.", "effect_description": "no effect"}, None
        
        current_turn = getattr(self, 'current_turn', 0)
        self.current_turn = current_turn + 1

        possible_actions = []

        if "armor_up" in self.abilities and self.mana >= self.abilities["armor_up"]["cost"]:
            if self.health <= self.max_health * 0.5:
                possible_actions.append((lambda target: self.use_ability("armor_up", target), self))

        if valid_enemies and "veteran_strike" in self.abilities and self.mana >= self.abilities["veteran_strike"]["cost"]:
            target = random.choice(valid_enemies)
            possible_actions.append((lambda target: self.use_ability("veteran_strike", target), target))

        if possible_actions and random.random() < 0.4:
            action, target, is_ability = random.choice(possible_actions)
            return action, target, is_ability
        
        target = random.choice(valid_enemies)
        return self.attack, target, False
    

class Cleric(Character):
    def __init__(self, name):
        super().__init__(name)
        self.type_name = "Cleric"
        self.intelligence += 4
        self.vitality += 2
        self.strength -= 2
        self.dexterity -= 1
        self.speed = 8

        self.max_health = self.calculate_max_health()
        self.max_mana = self.calculate_max_mana()
        self.armor -= 2
        self.armor_threshold = self.calculate_armor_threshold()

        self.health = self.max_health
        self.mana = self.max_mana

        self.initialize_abilities()

    def calculate_base_damage(self):
        base = self.intelligence * 0.4
        return round(base * random.uniform(0.9, 1.1), 1)
    
    def initialize_abilities(self):
        def divine_heal_effect(self, target=None):
            if not target:
                target = self

            heal_amount = self.intelligence * 0.8 + self.vitality * 0.2
            heal_amount = round(heal_amount * random.uniform(0.9, 1.1), 1)

            target.health = min(target.max_health, target.health + heal_amount)
        
        self.add_ability("Divine Heal", 15, "Heals target based on intelligence", divine_heal_effect)

        def smite_effect(self, target=None):
            if not target:
               return {
                   "type": "ability",
                   "name": "Smite",
                   "description": "this ability needs a target.",
                   "failed": True
               }
            damage = self.intelligence * 1.2
            effective_threshold = 0
            damage_result = target.take_damage(damage, effective_threshold)

            return {
                "type": "ability",
                "name": "Smite",
                "description": f"{self.name} smites {target.name} for {damage_result['damage']} damage."
            }
        
        self.add_ability("Smite", 12, "Deals magic damage based on intelligence", smite_effect)

    def choose_action(self,targets):
        valid_enemies = [t for t in targets if t.team != self.team and t.is_alive()]
        valid_allies = [t for t in targets if t.team == self.team and t.is_alive()]

        if not valid_enemies and not valid_allies:
            return lambda x: {"description": " does nothing.", "effect_description": "no effect"}
        
        possible_actions = []

        if valid_allies and "divine_heal" in self.abilities and self.mana >= self.abilities["divine_heal"]["cost"]:
            injured_allies = [ally for ally in valid_allies if ally.health < ally.max_health * 0.7]
            if injured_allies:
                target = min(injured_allies, key=lambda ally: ally.health / ally.max_health)
                possible_actions.append((lambda target: self.use_ability("divine_heal", target), target))

        if valid_enemies and "smite" in self.abilities and self.mana >= self.abilities["smite"]["cost"]:
            target = random.choice(valid_enemies)
            possible_actions.append((lambda target: self.use_ability("smite", target), valid_enemies))

        if possible_actions:
            return random.choice(possible_actions)
        
        target = random.choice(valid_enemies)
        return self.attack, target
    

class Druid(Character):
    def __init__(self, name):
        super().__init__(name)
        self.type_name = "Druid"
        self.intelligence += 3
        self.vitality += 2
        self.dexterity += 1
        self.strength -= 2
        self.speed = 9

        self.max_health = self.calculate_max_health()
        self.max_mana = self.calculate_max_mana()
        self.armor -= 1
        self.armor_threshold = self.calculate_armor_threshold()

        self.health = self.max_health
        self.mana = self.max_mana

        self.initalize_abilities()

    def calculate_base_damage(self):
        base = self.intelligence * 0.45
        return round(base * random.uniform(0.9, 1.1), 1)
    
    def initalize_abilities(self):
        def nature_blessing_effect(user, target):
            if not target:
                target = user

            heal_amount = user.intelligence * 0.5 + user.vitality * 0.3
            heal_amount = round(heal_amount * random.uniform(0.9, 1.1), 1)

            target.health = min(target.max_health, target.health + heal_amount)
            regen_per_turn = round(heal_amount * 0.2, 1)
            target.apply_status("regeneration", 3, heal_per_turn=regen_per_turn)

            return {
                "type": "ability",
                "name": "Nature's Blessing",
                "description": f"{self.name} blesses {target.name} with nature's healing for {heal_amount}",
                "effect_description": f"{target.name} will regenerate {regen_per_turn} health for 3 turns."
            }
        
        self.add_ability("Nature's Blessing", 14, "Heals target and applies regeneration", nature_blessing_effect)

        def thornwhip_effect(user, target=None):
            if not target:
                return {
                    "type": "ability",
                    "name": "Thornwhip",
                    "description": "This ability needs a target.",
                    "failed": True
                }
            
            damage = user.intelligence * 1.1
            effective_threshold = 0
            damage_result = target.take_damage(damage, effective_threshold)
            
            bleed_damage = round(user.intelligence * 0.2, 1)
            target.apply_status("bleeding", 3, damage_per_turn=bleed_damage)

            return {
                "type": "ability",
                "name": "Thornwhip",
                "description": f"{self.name} lashes {target.name} with thorny vines for {damage_result['damage']} damage.",
                "effect_description": f"{target.name} is bleeding and will take {bleed_damage} bleed damage for 3 turns."
            }
        
        self.add_ability("Thornwhip", 10, "Deals nature damage and applies bleeding", thornwhip_effect)

    def choose_action(self, targets):
        valid_enemies = [t for t in targets if t.team != self.team and t.is_alive()]
        valid_allies = [t for t in targets if t.team == self.team and t.is_alive()]

        if not valid_enemies and not valid_allies:
            return lambda x: {"description": " does nothing.", "effect_description": "no effect"}, None
        
        possible_actions = []

        if valid_allies and "Nature's Blessing" in self.ablities and self.mana >= self.abilities["Nature's Blessing"]["cost"]:
            injured_allies = [ally for ally in valid_allies if ally.health < ally.max_health * 0.8]
            if injured_allies:
                target = min(injured_allies, key=lambda ally: ally.health / ally.max_health)
                possible_actions.append((lambda target: self.use_ability("Nature's Blessing", target), target))

        if valid_enemies and "thorn_whip" in self.abilities and self.mana >= self.abilities["thorn_whip"]["cost"]:
            target = random.choice(valid_enemies)
            possible_actions.append((lambda target: self.use_ability("thorn_whip", target), valid_enemies))

        if possible_actions:
            return random.choice(possible_actions)
        
        if valid_enemies:
            target = random.choice(valid_enemies)
            return self.attack, target
        
        else:
            return lambda x: {"description": " does nothing.", "effect_description": "no effect."}, None