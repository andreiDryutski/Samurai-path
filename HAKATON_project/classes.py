import random

class Warrior:
    def __init__(self, name, health, damage = 1, level=100, xp=0):
        self.name = name
        self.base_health = health
        self.base_damage = damage
        self.level = level
        self.xp = xp
        self.max_health = int(health * (1.1 ** (level - 1)))
        self.health = self.max_health
        self.damage = int(damage * (1.1 ** (level - 1)))
        self.evasion = False
        self.is_ninja = False

    def recalc_stats(self):
        self.max_health = int(self.base_health * (1.1 ** (self.level - 1)))
        self.damage = int(self.base_damage * (1.1 ** (self.level - 1)))
        self.health = self.max_health

    def add_xp(self, amount):
        self.xp += amount
        xp_needed = self.get_xp_for_next_level()
        
        while self.xp >= xp_needed:
            self.xp -= xp_needed
            self.level += 1
            self.recalc_stats()
            print(f"\n[ПОЗДРАВЛЯЮ] Ты достиг {self.level} уровня!")
            print(f"Здоровье: {self.max_health}")
            print(f"Урон: {self.damage}")
            xp_needed = self.get_xp_for_next_level()
            input("\nНажми Enter для продолжения...")
    
    def get_xp_for_next_level(self):
        return 10 * self.level
    
    def get_xp_to_next_level(self):
        return self.get_xp_for_next_level() - self.xp

    def attack(self, target):
        dmg = self.damage
        target.health -= dmg
        if target.health < 0:
            target.health = 0
        return dmg, False

    def special_ability(self, target):
        return "Обычная техника...", False

    def defend(self):
        heal = int(self.max_health * 0.1)
        self.health = min(self.max_health, self.health + heal)
        return heal

    def is_alive(self):
        return self.health > 0


class Sumo(Warrior):
    def __init__(self, name):
        super().__init__(name, health=150, damage=10)
        self.is_ninja = False

    def special_ability(self, target=None):
        heal = int(self.max_health * 0.15)
        self.health = min(self.max_health, self.health + heal)
        return f"Ням-Ням лапша! +{heal} HP (теперь {self.health})", False


class Shinobi(Warrior):
    def __init__(self, name):
        super().__init__(name, health=80, damage=25)
        self.is_ninja = True

    def attack(self, target):
        is_critical = random.random() < 0.3
        dmg = self.damage * 2 if is_critical else self.damage
        
        if target.evasion and random.random() < 0.5:
            target.evasion = False
            return 0, True
        
        target.health -= dmg
        if target.health < 0:
            target.health = 0
        return dmg, is_critical

    def special_ability(self, target=None):
        self.evasion = True
        return "ТЕНЕВОЕ УКЛОНЕНИЕ! Следующая атака может не попасть", False


class Enemy:
    def __init__(self, name, health, damage, xp):
        self.name = name
        self.health = health
        self.max_health = health
        self.damage = damage
        self.xp = xp
        self.evasion = False
    
    def attack(self, target):
        if target.evasion and random.random() < 0.5:
            target.evasion = False
            return 0, True
        
        dmg = self.damage
        target.health -= dmg
        if target.health < 0:
            target.health = 0
        return dmg, False
    
    def defend(self):
        heal = int(self.max_health * 0.1)
        self.health = min(self.max_health, self.health + heal)
        return heal
    
    def is_alive(self):
        return self.health > 0
    
    def ai_choise(self, player):
        return random.choices([1, 3], weights=[80, 20])[0]
    
    def special_ability(self, target):
        return "Обычная атака...", False


class RegularEnemy(Enemy):
    def __init__(self, name, health, damage, xp):
        super().__init__(name, health, damage, xp)
    
    def ai_choise(self, player):
        return random.choices([1, 3], weights=[80, 20])[0]


class Boss(Enemy):
    def __init__(self, name, health, damage, xp):
        super().__init__(name, health, damage, xp)
        self.special_cooldown = 0
    
    def special_ability(self, target):
        dmg = self.damage * 2
        target.health -= dmg
        if target.health < 0:
            target.health = 0
        self.special_cooldown = 3
        return f"НЕОЖИДАННЫЙ УДАР СО СПИНЫ! {dmg} урона!", False
    
    def ai_choise(self, player):
        if self.special_cooldown > 0:
            self.special_cooldown -= 1
        
        if player.health < self.damage * 2 and self.special_cooldown == 0:
            return 2
        
        if self.health < self.max_health * 0.3:
            return random.choices([1, 3], weights=[60, 40])[0]
        
        return random.choices([1, 3, 2], weights=[60, 30, 10])[0]



class Father(Enemy):
    def __init__(self, name, health, damage, xp, evasion_chance=15):
        super().__init__(name, health, damage, xp)
        self.evasion_chance = evasion_chance
        self.stand_ready = False
        self.super_damage = 600
        self.special_cooldown = 0
    
    def check_evasion(self):
        """Пассивный шанс увернуться от атаки"""
        if self.evasion_chance > 0 and random.random() * 100 < self.evasion_chance:
            return True
        return False
    
    def special_ability(self, target):
        if not self.stand_ready:
            self.stand_ready = True
            return "Отец встает в стойку... Следующая атака будет смертельной!", False
        else:
            dmg = self.super_damage
            if target.evasion and random.random() < 0.5:
                target.evasion = False
                self.stand_ready = False
                return "Отец взмывает мечом, но самурай уклоняется! Отец начинает чувствовать уважение", False
            else:
                target.health -= dmg
                if target.health < 0:
                    target.health = 0
                self.stand_ready = False
                return f"Отец взмывает мечом и наносит {dmg} урона!", False
    
    def ai_choise(self, player):
        if self.special_cooldown > 0:
            self.special_cooldown -= 1
        
        if self.stand_ready:
            return 2
        

        if player.health < self.damage * 2 and self.special_cooldown == 0:
            return 2
        

        if self.health < self.max_health * 0.3:
            return random.choices([1, 3], weights=[60, 40])[0]
        
        return random.choices([1, 3, 2], weights=[60, 30, 10])[0]