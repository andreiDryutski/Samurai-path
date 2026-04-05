import os
import time
from classes import Sumo, Shinobi
from locations import LocationManager
from battle import Battle

class Game:
    def __init__(self):
        self.player = None
        self.location_manager = LocationManager()
        self.battle = Battle()
        self.current_location = None

    def select_warrior(self):
        """Выбор персонажа игрока"""
        print("\n[ВЫБОР ПЕРСОНАЖА]")
        print("1. Сумоист-толстяк (Много здоровья, способность: восстановление)")
        print("2. Синоби-ниндзя (Критический урон, способность: уклонение)")
        
        while True:
            choice = input(">>> ").strip()
            if choice in ["1", "2"]:
                break
            print("Неверный выбор! Введите 1 или 2")
        
        name = input("Имя воина: ").strip()
        if not name:
            name = "Безымянный самурай"
        
        if choice == "1":
            return Sumo(name)
        else:
            return Shinobi(name)

    def show_player_stats(self):
        """Показать статистику игрока"""
        print("\n" + "=" * 50)
        print(f"[СТАТИСТИКА] {self.player.name} (Уровень {self.player.level})")
        print(f"Здоровье: {self.player.health}/{self.player.max_health} HP")
        print(f"Урон: {self.player.damage}")
        print(f"Опыт: {self.player.xp}/{self.player.get_xp_for_next_level()} XP")
        print(f"До следующего уровня: {self.player.get_xp_to_next_level()} XP")
        if self.location_manager.has_artifact:
            print(f"Артефакт: Обогащённый уран [В РЮКЗАКЕ]")
        print("=" * 50)

    def show_main_menu(self):
        """Показать главное меню"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 55)
        print("                  П У Т Ь   С А М У Р А Я")
        print("=" * 55)
        print("1. НАЧАТЬ ИГРУ")
        print("2. ВЫХОД")
        print("=" * 55)

    def show_location_menu(self):
        """Показать меню локаций"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.show_player_stats()
            
            available, locked = self.location_manager.show_locations(self.player.level)
            
            print("\n[ДЕЙСТВИЯ]")
            print("0. Выйти в главное меню")
            
            choice = input("\nВыбери локацию или действие: ").strip()
            
            if choice == "0":
                return False
            
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(self.location_manager.locations):
                    location = self.location_manager.locations[idx]
                    if location.is_available(self.player.level):
                        self.explore_location(location)
                    else:
                        print(f"\n[ОШИБКА] Локация недоступна! Нужен {location.required_level} уровень")
                        time.sleep(2)
                else:
                    print("\n[ОШИБКА] Неверный выбор!")
                    time.sleep(1)
            else:
                print("\n[ОШИБКА] Неверный выбор!")
                time.sleep(1)

    def explore_location(self, location):
        """Исследование локации"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.show_player_stats()
            print(f"\n[ЛОКАЦИЯ] {location.name}")
            
            enemy = self.location_manager.select_enemy_from_location(location)
            
            if enemy is None:
                break
            
            print(f"\n[БОЙ] Противник: {enemy.name}")
            print(f"HP: {enemy.health}, Урон: {enemy.damage}")
            input("Нажми Enter, чтобы начать бой...")
            
            victory = self.battle.start_battle(self.player, enemy, self.location_manager, location)
            
            if not victory:
                print("\n[ИГРА ОКОНЧЕНА] Ты погиб в бою...")
                print("Начни новую игру!")
                input("\nНажми Enter для продолжения...")
                return False
            
            # Восстановление после боя
            self.player.health = self.player.max_health
            print("\n[ОТДЫХ] Ты полностью восстановил здоровье!")
            
            input("\nНажми Enter для продолжения...")
        
        return True

    def new_game(self):
        """Начать новую игру"""
        self.player = self.select_warrior()
        print(f"\n[ДОБРО ПОЖАЛОВАТЬ] {self.player.name}, твой путь начинается!")
        print(f"Твой уровень: {self.player.level}")
        print(f"Здоровье: {self.player.max_health} HP")
        print(f"Урон: {self.player.damage}")
        input("\nНажми Enter, чтобы продолжить...")
        
        while True:
            if not self.show_location_menu():
                break

    def run(self):
        """Запуск игры"""
        while True:
            self.show_main_menu()
            
            choice = input(">>> ").strip()
            if choice == "1":
                self.new_game()
            elif choice == "2":
                print("\n[ПРОЩАНИЕ] Путь самурая окончен... До встречи!")
                break
            else:
                print("\n[ОШИБКА] Неверный выбор!")
                time.sleep(1)

if __name__ == "__main__":
    game = Game()
    game.run()