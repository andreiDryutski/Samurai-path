from classes import RegularEnemy, Boss, Father

class Location:
    def __init__(self, name, required_level, enemies, boss, quest=None, is_father_battle=False):
        self.name = name
        self.required_level = required_level
        self.enemies = enemies
        self.boss = boss
        self.quest = quest
        self.is_completed = False
        self.quest_item = None
        self.is_father_battle = is_father_battle  # Флаг для битвы с Отцом

    def is_available(self, player_level):
        return player_level >= self.required_level

class LocationManager:
    def __init__(self):
        self.locations = self.create_locations()
        self.current_location = None
        self.quest_active = False
        self.has_artifact = False

    def create_locations(self):
        """Создание всех локаций"""
        locations = []
        
        # Локация 1: Тренировочная площадка
        enemies_1 = [
            RegularEnemy("Мечник-ученик", 50, 10, 10),
            RegularEnemy("Мечник-учитель", 400, 30, 30)
        ]
        boss_1 = Boss("Легенда меча", 600, 40, 100)
        quest_1 = {
            'name': 'Древний артефакт',
            'description': 'Достать Обогащённый уран',
            'item': 'Обогащённый уран',
            'reward_xp': 500
        }
        locations.append(Location("Тренировочная площадка", 1, enemies_1, boss_1, quest_1))
        
        # Локация 2: Лес, где обитают монстры
        enemies_2 = [
            RegularEnemy("Паук", 550, 50, 200),
            RegularEnemy("Призрак с мечом", 850, 100, 300)
        ]
        boss_2 = Boss("Королева пауков", 1400, 150, 400)
        locations.append(Location("Лес монстров", 33, enemies_2, boss_2, None))

        # Локация 3: Шахта
        enemies_3 = [
            RegularEnemy("Скелет с мечом", 1650, 150, 450),
            RegularEnemy("Скелет с топором", 2000, 200, 650)
        ]
        boss_3 = Boss("Скелет-маг", 3000, 250, 1000)
        locations.append(Location("Шахта", 66, enemies_3, boss_3, None))

        # Локация 4: Битва с Отцом (отдельная локация)
        quest_father = {
            'name': 'Победить Отца',
            'description': 'Доказать Отцу что ты сильнее',
            'item': 'Меч Отца',
            'reward_xp': 5000
        }

        father_boss = Father("Отец", 3000, 250, 1000, evasion_chance=25)
        locations.append(Location("Битва с Отцом", 100, [], father_boss, quest_father, is_father_battle=True))
        
        return locations

    def show_locations(self, player_level):
        """Показать доступные локации"""
        print("\n[ДОСТУПНЫЕ ЛОКАЦИИ]")
        available = []
        locked = []
        
        for i, loc in enumerate(self.locations, 1):
            if loc.is_available(player_level):
                status = "[ДОСТУПНА]"
                available.append((i, loc))
            else:
                status = f"[ЗАКРЫТА] (нужен {loc.required_level} уровень)"
                locked.append((i, loc))
            
            quest_status = ""
            if loc.quest and not loc.is_completed:
                quest_status = f" - КВЕСТ: {loc.quest['name']}"
            elif loc.is_completed:
                quest_status = " - КВЕСТ ВЫПОЛНЕН"
            
            print(f"{i}. {loc.name} {status}{quest_status}")
        
        return available, locked

    def select_enemy_from_location(self, location):
        """Выбор врага в локации"""
        print(f"\n[ВРАГИ В ЛОКАЦИИ: {location.name}]")
        
        if location.is_father_battle:
            print(f" ТЕБЯ ЖДЁТ СУПЕРБОСС: {location.boss.name} ")
            print(f"HP: {location.boss.health}, Урон: {location.boss.damage}, XP: {location.boss.xp}")
            if hasattr(location.boss, 'evasion_chance'):
                print(f"Шанс уворота: {location.boss.evasion_chance}%")
            print("\n1. Начать битву с Отцом")
            print("2. Вернуться в меню локаций")
            
            while True:
                choice = input("\n>>> ").strip()
                if choice == "1":
                    return location.boss
                elif choice == "2":
                    return None
                else:
                    print("Неверный выбор!")
        
        print("1. Обычные враги:")
        for i, enemy in enumerate(location.enemies, 1):
            print(f"   {i}. {enemy.name} (HP: {enemy.health}, Урон: {enemy.damage}, XP: {enemy.xp})")
        print(f"\n2. БОСС: {location.boss.name} (HP: {location.boss.health}, Урон: {location.boss.damage}, XP: {location.boss.xp})")
        print("3. Вернуться в меню локаций")
        
        while True:
            choice = input("\n>>> ").strip()
            if choice == "1":
                print("\nВыбери врага:")
                for i, enemy in enumerate(location.enemies, 1):
                    print(f"{i}. {enemy.name}")
                enemy_choice = input(">>> ").strip()
                if enemy_choice.isdigit() and 1 <= int(enemy_choice) <= len(location.enemies):
                    return location.enemies[int(enemy_choice) - 1]
                else:
                    print("Неверный выбор!")
            elif choice == "2":
                return location.boss
            elif choice == "3":
                return None
            else:
                print("Неверный выбор!")

    def check_quest_completion(self, location, player):
        """Проверка выполнения квеста"""
        if location.quest and not location.is_completed:
            if location.is_father_battle:
                print(f"\n[КВЕСТ ВЫПОЛНЕН] {location.quest['name']}")
                print(f"Получено {location.quest['reward_xp']} XP!")
                print(f"Получен артефакт: {location.quest['item']}!")
                player.add_xp(location.quest['reward_xp'])
                location.is_completed = True
                return True
            elif self.has_artifact:
                print(f"\n[КВЕСТ ВЫПОЛНЕН] {location.quest['name']}")
                print(f"Получено {location.quest['reward_xp']} XP!")
                player.add_xp(location.quest['reward_xp'])
                location.is_completed = True
                self.quest_active = False
                return True
        return False