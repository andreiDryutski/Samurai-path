import os
import time

class Battle:                                          
    def __init__(self):
        self.round = 1                                    #ну просто типо 1 раунд
        self.logs = ["Битва начинается!"]                 #Уведомление о начале битвы
    
    def draw_game(self, player, enemy):                   #отрисовываем игру
        os.system('cls')                                  #очищаем поле
        
        print("=" * 55)
        print("                 П У Т Ь   С А М У Р А Я")
        print("=" * 55)
        print(f"  {player.name} (Ур. {player.level}) VS {enemy.name}")
        print("-" * 55)
        
        # Полоски здоровья
        player_percent = int((player.health / player.max_health) * 20)
        enemy_percent = int((enemy.health / enemy.max_health) * 20)
        
        player_bar = "█" * player_percent + "░" * (20 - player_percent)
        enemy_bar = "█" * enemy_percent + "░" * (20 - enemy_percent)
                                                                                                       #рисуем поле битвы
        print(f"  {player.name}: {player_bar} {player.health}/{player.max_health} HP        {enemy.name}: {enemy_bar} {enemy.health}/{enemy.max_health} HP")
        print("-" * 55)
        print(f"  РАУНД {self.round}")
        print("")
        print("  [1] АТАКА     [2] СПОСОБНОСТЬ     [3] ЗАЩИТА")
        print("")
        
        # Показываем последние 2 действия
        for log in self.logs[-2:]:
            print(f"  > {log}")
        print("")
    
    def player_turn(self, player, enemy):                           #просто ход игрока
        """Ход игрока"""
        self.draw_game(player, enemy)
        print(f"\n[ТВОЙ ХОД] {player.name}")
        print(f"Здоровье: {player.health}/{player.max_health} HP")              #говорим сколько хп у игрока
        print(f"Опыт: {player.xp}/{player.get_xp_for_next_level()} XP (до след. уровня: {player.get_xp_to_next_level()})")                   #говорим сколько xp у игрока
        
        while True:                                                                                                                          #типо защищаемся от ошибки
            choice = input("Действие (1-3): ").strip()
            if choice in ["1", "2", "3"]:
                break
            else:
                print("Неверный выбор! Введите 1, 2 или 3")
        
        if choice == "1":                                                                #делаем атаку
            dmg, is_special = player.attack(enemy)                                                              
            if is_special and player.is_ninja:                                           #крит урон для ниндзя
                self.logs.append(f"[КРИТ] {player.name} наносит {dmg} урона!")
            else:                                                                       #обычный урон
                self.logs.append(f"{player.name} наносит {dmg} урона!")                 
        
        elif choice == "2":
            message, _ = player.special_ability(enemy)                                  #особенное сообщение для каждого класса, _ значит что переменная не будет использоватся (типо 1 раз)
            self.logs.append(message)
        
        elif choice == "3":
            heal = player.defend()
            self.logs.append(f"{player.name} восстанавливает {heal} HP!")
        
        time.sleep(1.5)
    
    def enemy_turn(self, player, enemy):
        """Ход врага с ИИ"""
        self.draw_game(player, enemy)
        print(f"\n[ХОД ВРАГА] {enemy.name}")
        print(f"Здоровье: {enemy.health}/{enemy.max_health} HP")
        time.sleep(1)

        choice = enemy.ai_choise(player)
    
        if choice == 1:
            dmg, is_critical = enemy.attack(player)
            if dmg == 0:
                self.logs.append(f"{player.name} уклонился от атаки {enemy.name}!")
            elif is_critical:
                self.logs.append(f"[КРИТ] {enemy.name} наносит {dmg} урона!")
            else:
                self.logs.append(f"{enemy.name} атакует и наносит {dmg} урона!")
    
        elif choice == 2:
            if hasattr(enemy, 'special_ability'):
                message, _ = enemy.special_ability(player)
                self.logs.append(message)
            else:
                dmg, _ = enemy.attack(player)
                self.logs.append(f"{enemy.name} атакует и наносит {dmg} урона!")
    
        elif choice == 3:
            heal = enemy.defend()
            self.logs.append(f"{enemy.name} восстанавливает {heal} HP!")
    
        time.sleep(1.5)
    
    def start_battle(self, player, enemy, location_manager=None, current_location=None):
        """Запуск битвы между игроком и врагом"""
        self.round = 1
        self.logs = ["Битва начинается!"]
        
        while player.is_alive() and enemy.is_alive():
            self.player_turn(player, enemy)
            if not enemy.is_alive():
                break
            
            self.enemy_turn(player, enemy)
            if not player.is_alive():
                break
            
            self.round += 1
            
            if hasattr(player, 'evasion'):
                player.evasion = False
            if hasattr(enemy, 'evasion'):
                enemy.evasion = False
        
        self.draw_game(player, enemy)
        
        if player.is_alive():
            print(f"\n[ПОБЕДА] Ты победил {enemy.name}!")
            print(f"Получено {enemy.xp} XP!")
            player.add_xp(enemy.xp)
            enemy.health = enemy.max_health
            
            # Проверка квеста для босса
            if current_location and current_location.boss == enemy and current_location.quest:
                print(f"\n[КВЕСТ] {current_location.quest['description']}")
                if current_location.quest['item'] == "Обогащённый уран":
                    location_manager.has_artifact = True
                    print(f"[ПОЛУЧЕНО] {current_location.quest['item']}!")
                    location_manager.check_quest_completion(current_location, player)
            
            return True
        else:
            print(f"\n[ПОРАЖЕНИЕ] {enemy.name} победил тебя!")
            print(f"Ты продержался {self.round} раундов")
            return False