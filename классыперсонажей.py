import random

class Hero:
    def __init__(self, name, health, damage, ability, ability_desc):
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage
        self.ability = ability
        self.ability_desc = ability_desc
        self.artifacts = []
        self.friends = []
        self.next_attack_double = False
    
    def attack(self, enemy):
        damage_dealt = self.damage
        
        # Проверка на двойную атаку
        if self.next_attack_double:
            damage_dealt *= 2
            self.next_attack_double = False
            print(f"{self.name} использует двойную атаку!")
        
        # Артефакты могут увеличивать урон
        for artifact in self.artifacts:
            if "Усиление атаки" in artifact:
                damage_dealt += 5
            elif "Энергия Верхнего мира" in artifact:
                damage_dealt += random.randint(2, 8)
        
        print(f"{self.name} атакует {enemy.name} и наносит {damage_dealt} урона!")
        enemy.health -= damage_dealt
        return damage_dealt
    
    def use_ability(self):
        print(f"{self.name} использует способность: {self.ability_desc}")
        
        if self.ability == "heal":
            heal_amount = 15
            for artifact in self.artifacts:
                if "Аптечка Хоппера" in artifact:
                    heal_amount += 10
                elif "Кристалл из Изнанки" in artifact:
                    heal_amount += random.randint(5, 15)
            
            self.health = min(self.max_health, self.health + heal_amount)
            print(f"{self.name} восстанавливает {heal_amount} здоровья! Теперь у него {self.health} HP")
            return "heal"
        
        elif self.ability == "stun":
            print(f"{self.name} оглушает противника на один ход!")
            return "stun"
        
        elif self.ability == "double_attack":
            print(f"{self.name} готовится к двойной атаке в следующем ходу!")
            self.next_attack_double = True
            return "double_attack"
        
        elif self.ability == "instant_kill":
            print("ОДИ АКТИВИРУЕТ СВОЮ СУПЕРСПОСОБНОСТЬ!")
            return "instant_kill"
        
        return None
    
    def is_alive(self):
        return self.health > 0
    
    def call_friend(self, friend_name):
        print(f"{self.name} зовет на помощь {friend_name}!")
        
        if friend_name == "Элевен":
            print("Элевен использует телекинез и наносит 25 урона всем врагам!")
            return 25, "all"
        elif friend_name == "Хоппер":
            print("Хоппер стреляет из ружья и наносит 20 урона!")
            return 20, "single"
        elif friend_name == "Стив":
            print("Стив размахивает битой с гвоздями и наносит 15 урона!")
            return 15, "single"
        elif friend_name == "Макс":
            print("Макс отвлекает врагов, снижая их атаку на 5!")
            return "debuff", "all"
        
        return 0, "single"

class Enemy:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage
        self.stunned = False
    
    def attack(self, hero):
        if self.stunned:
            print(f"{self.name} оглушен и пропускает ход!")
            self.stunned = False
            return 0
        
        damage_dealt = self.damage
        print(f"{self.name} атакует {hero.name} и наносит {damage_dealt} урона!")
        hero.health -= damage_dealt
        return damage_dealt
    
    def stun(self):
        """Оглушить врага"""
        self.stunned = True
    
    def is_alive(self):
        return self.health > 0
