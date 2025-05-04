class CombatManager:
    def __init__(self):
        self.participants = []
        self.current_turn_index = 0
        self.round_number = 0
        self.is_combat_active = False
        self.battle_log = []
        self.max_rounds = 100

    def add_participants(self, character):
        self.participants.append(character)
        self.participants.sort(key=lambda x: x.speed, reverse=True)

    def run_simulation(self):
        self.is_combat_active = True
        self.round_number = 1
        self.current_turn_index =0

        self.log_event("=== Combat Begins! ===")

        while self.is_combat_active and self.round_number <= self.max_rounds:
            self._process_turn()

        return {
            "rounds_completed": self.round_number,
            "battle_log": self.battle_log,
            "winner": self._determine_winner()
        }
    
    def _process_turn(self):
        if not self.is_combat_active:
            return
        
        current_character = self.participants[self.current_turn_index]
        self.log_event(f"\n Round {self.round_number}: {current_character.name}'s turn")

        if not current_character.is_alive():
            self._end_turn()
            return
        
        self._process_status_effects(current_character)

        if not current_character.can_act():
            self.log_event(f"{current_character} cannot act this turn.")

        self._end_turn()

    def _preform_ai_action(self, character):
        targets = self._get_valid_targets(character)
        if not targets:
            self.log_event(f"{character.name} has no valid target.")
            return
        
        action, target = character.choose_action(targets)

        self._execute_action(character, action, target)

    def _get_valid_targets(self, character):
        return [p for p in self.participants if p.is_alive() and p.team != character.team]
    
    def _execute_action(self, character, action, target):
        result = action(target)
        self.log_event(f"{character.name}{result['description']}{target.name}")
        self.log_event(f" Effect: {result['effect_description']}")

        self._check_combat_end_conditions()

    def _process_status_effects(self, character):
        status_results = character.process_status_effect_at_turn_start()
        for result in status_results:
            self.log_event(f" Status Effect: {result}")

    def _end_turn(self):
        current_character = self.participants[self.current_turn_index]

        end_turn_results = current_character.process_status_effect_at_turn_end()
        for result in end_turn_results:
            self.log_event(f" End Turn Effect: {result}")

        self.current_turn_index += 1

        if self.current_turn_index >= len(self.participants):
            self.current_turn_index = 0
            self.round_number += 1

    def _check_combat_end_conditions(self):
        teams = {}
        for character in self.participants:
            if character.is_alive():
                if character.team not in teams:
                    teams[character.team] = []
                teams[character.team].append(character)
        
        if len(teams) <= 1:
            self.is_combat_active = False

        if len(teams) == 1:
            winning_team = list(teams.keys())[0]
            self.log_event(f"\n=== Team {winning_team} Wins! ===")
        else:
            self.log_event(f"\n=== Draw - All Combatants Have Fallen! ===")

        if self.round_number >= self.max_rounds:
            self.is_combat_active = False
            self.log_event(f"\n=== Combat after {self.max_rounds} rounds! ===")

    def _determine_winner(self):
        living_teams = {}
        for character in self.participants:
            if character.is_alive():
                if character.team not in living_teams:
                    living_teams[character.team] = 0
                living_teams[character.team] += 1

        if len(living_teams) == 0:
            return "draw"
        elif len(living_teams) == 1:
            return list(living_teams.keys())[0]
        else:
            return None
        
    def log_event(self, message):
        self.battle_log.append(message)
        print(message)

    def get_battle_summary(self):
        living_chars = [c for c in self.participants if c.is_alive()]
        dead_chars = [c for c in self.participants if not c.is_alive()]

        summary = {
            "rounds_completed": self.round_number,
            "battle_ended": not self.is_combat_active,
            "winner": self._determine_winner(),
            "survivors": [{
                "name": c.name,
                "team": c.team,
                "health": c.current_health,
                "percent_health": int((c.current_health / c.max_health) * 100)
            } for c in living_chars],
            "casualties": [c.name for c in dead_chars],
            "total_participants": len(self.participants),
            "survivor_count": len(living_chars)
        }

        return summary
    
    def print_battle_report(self):
        summary = self.get_battle_summary()

        print("\n=== Battle Report ===")
        print(f"Rounds completed: {summary['rounds_completed']}")

        if summary['winner']:
            if summary['winner'] == 'draw':
                print("Results: Draw - All combatants have fallen.")
            else:
                print(f"Result: Team {summary['winner']} is Victorious!")

        else:
            print("Result: Battle is still ongoing!")

        print("\nSURVIVORS:")
        for char in summary['survivors']:
            print(f" {char['name']}(Team{char['team']}): {char['health']} HP ({char['percent_health']}%)")

        print("\nCASUALTIES:")
        for name in summary['casulaties']:
            print(f"  {name} has fallen!")

        print(f"\nSurvival rate: {(summary["survivors_count"] / summary['total_participants']) * 100:.1f}%")
        print("==========")