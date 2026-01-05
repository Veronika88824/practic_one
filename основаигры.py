from characters import Hero, Enemy
from utils import print_slow, print_header, get_random_artifact, show_loading_screen
import random

class Game:
    def __init__(self):
        self.hero = None
        self.artifacts = []
        self.portal_open = False
        self.vecna_defeated = False
        
        # Артефакты
        self.available_artifacts = [
            "Эгго-вафли (усиливают лечение на 10 HP)",
            "Фонарик (ослепляет демогоргонов)",
            "Рация (позволяет позвать друга в любой момент)",
            "Кристалл из Изнанки (случайное усиление способностей)",
            "Аптечка Хоппера (усиливает лечение)",
            "Кассета с любимой музыкой (ослабляет Векну)",
            "Плакат с Дэвидом Боуи (дает силу Верхнего мира)",
            "Рождественские огоньки (защита от холода Изнанки)",
            "Усиление атаки (увеличивает базовый урон на 5)",
            "Энергия Верхнего мира (добавляет случайный урон)",
            "Карта Хоукинса (позволяет найти укрытие)",
            "Фотоаппарат (вспышка ослепляет врагов)",
            "Волейбольный мяч (символ дружбы, дает +10 HP)",
            "Научный журнал (дает тактические преимущества)",
            "Секретные записи (раскрывают слабости врагов)"
        ]
        
        # Персонажи
        self.heroes = {
            "1": ("Майк", Hero("Майк", 100, 15, "heal", "Мотивация: восстанавливает здоровье себе и союзникам")),
            "2": ("Дастин", Hero("Дастин", 90, 18, "stun", "Стратег: оглушает врага на один ход")),
            "3": ("Уилл", Hero("Уилл", 80, 20, "double_attack", "Связь с Изнанкой: следующая атака наносит двойной урон")),
            "4": ("Оди (чит)", Hero("Оди", 120, 25, "instant_kill", "Секретное оружие: мгновенно побеждает Векну"))
        }
        
        # Друзья для вызова
        self.friends = ["Элевен", "Хоппер", "Стив", "Макс", "Лукас", "Нэнси", "Робин", "Эрика"]
    
    def choose_hero(self):
        print_header("ВЫБОР ПЕРСОНАЖА")
        print("Выберите своего героя:")
        for key, (name, hero) in self.heroes.items():
            print(f"{key}. {name} - {hero.ability_desc}")
        print("-" * 60)
        
        while True:
            choice = input("Ваш выбор (1-4): ")
            if choice in self.heroes:
                self.hero = self.heroes[choice][1]
                print(f"\n✓ Отличный выбор! Вы играете за {self.hero.name}!")
                return
            else:
                print("✗ Пожалуйста, выберите число от 1 до 4")
    
    def choose_artifacts(self):
        print_header("ВЫБОР АРТЕФАКТОВ")
        print("Выберите 3 артефакта для начала игры:")
        print("Они дадут вам особые способности!")
        
        selected_artifacts = []
        for i in range(3):
            print(f"\nАртефакт {i+1}:")
            for idx, artifact in enumerate(self.available_artifacts, 1):
                print(f"{idx}. {artifact}")
            
            while True:
                try:
                    choice = int(input(f"Выберите артефакт {i+1} (1-{len(self.available_artifacts)}): "))
                    if 1 <= choice <= len(self.available_artifacts):
                        selected_artifact = self.available_artifacts[choice-1]
                        if selected_artifact not in selected_artifacts:
                            selected_artifacts.append(selected_artifact)
                            self.hero.artifacts.append(selected_artifact)
                            print(f"✓ Вы выбрали: {selected_artifact}")
                            break
                        else:
                            print("✗ Этот артефакт уже выбран!")
                    else:
                        print("✗ Неверный выбор!")
                except ValueError:
                    print("✗ Введите число!")
        
        print(f"\n✓ Вы выбрали артефакты: {', '.join(selected_artifacts)}")
    
    def open_portal(self):
        print_header("ОТКРЫТИЕ ПОРТАЛА")
        print_slow("ГРОМ И МОЛНИИ... ПОРТАЛ В ИЗНАНКУ ОТКРЫВАЕТСЯ!")
        print_slow("Из портала выходят демогоргоны и начинают атаковать Хоукинс!")
        print_slow("Небо становится кроваво-красным...")
        self.portal_open = True
    
    def battle_with_demogorgon(self, enemy_name="Демогоргон", health=60, damage=12):
        print_header(f"БИТВА С {enemy_name.upper()}")
        print_slow(f"{enemy_name.upper()} ПОЯВЛЯЕТСЯ ПЕРЕД ВАМИ!")
        demogorgon = Enemy(enemy_name, health, damage)
        
        stunned_turns = 0
        
        while self.hero.is_alive() and demogorgon.is_alive():
            print(f"\n{'─' * 40}")
            print(f"{self.hero.name}: {self.hero.health}/{self.hero.max_health} HP")
            print(f"{demogorgon.name}: {demogorgon.health} HP")
            print(f"{'─' * 40}")
            print("1. Атаковать")
            print("2. Использовать способность")
            print("3. Позвать друга на помощь")
            print("4. Использовать артефакт")
            
            choice = input("\nВаш выбор: ")
            
            if choice == "1":
                self.hero.attack(demogorgon)
                if demogorgon.is_alive():
                    demogorgon.attack(self.hero)
            
            elif choice == "2":
                ability_result = self.hero.use_ability()
                if ability_result == "stun":
                    demogorgon.stun()
                    stunned_turns = 1
                elif ability_result == "heal":
                    if demogorgon.is_alive():
                        demogorgon.attack(self.hero)
            
            elif choice == "3":
                if "Рация (позволяет позвать друга в любой момент)" in self.hero.artifacts:
                    print("\nКого вы хотите позвать?")
                    for i, friend in enumerate(self.friends[:4], 1):
                        print(f"{i}. {friend}")
                    
                    try:
                        friend_choice = int(input("Выберите друга: ")) - 1
                        if 0 <= friend_choice < 4:
                            friend = self.friends[friend_choice]
                            friend_damage, damage_type = self.hero.call_friend(friend)
                            
                            if isinstance(friend_damage, int):
                                demogorgon.health -= friend_damage
                            elif friend_damage == "debuff":
                                demogorgon.damage = max(5, demogorgon.damage - 5)
                                print(f"Атака {demogorgon.name} уменьшена до {demogorgon.damage}!")
                    except ValueError:
                        print("Неверный выбор!")
                else:
                    print("У вас нет рации! Вы не можете позвать друга.")
                    continue
                
                if demogorgon.is_alive():
                    demogorgon.attack(self.hero)
            
            elif choice == "4":
                print("\nВаши артефакты:")
                for i, artifact in enumerate(self.hero.artifacts, 1):
                    print(f"{i}. {artifact}")
                
                try:
                    artifact_choice = int(input("Выберите артефакт для использования: ")) - 1
                    if 0 <= artifact_choice < len(self.hero.artifacts):
                        artifact = self.hero.artifacts[artifact_choice]
                        print(f"Используется {artifact}")
                        
                        if "Фонарик" in artifact:
                            print("Фонарик ослепляет демогоргона на 1 ход!")
                            demogorgon.stun()
                        elif "Эгго-вафли" in artifact:
                            print("Эгго-вафли восстанавливают 15 HP!")
                            self.hero.health = min(self.hero.max_health, self.hero.health + 15)
                        elif "Фотоаппарат" in artifact:
                            print("Вспышка фотоаппарата ослепляет врага!")
                            demogorgon.health -= 10
                except:
                    print("Не удалось использовать артефакт!")
            
            else:
                print("Неверный выбор! Пропускаете ход.")
                if demogorgon.is_alive():
                    demogorgon.attack(self.hero)
            
            # Проверка на смерть героя
            if not self.hero.is_alive():
                print(f"\n✗ {self.hero.name} побежден! Игра окончена.")
                return False
        
        # Проверка на победу
        if not demogorgon.is_alive():
            print(f"\n✓ ПОБЕДА! Вы победили {enemy_name}!")
            
            # Награда за победу
            if random.random() < 0.7:  # 70% шанс найти артефакт
                new_artifact = get_random_artifact()
                if new_artifact not in self.hero.artifacts:
                    self.hero.artifacts.append(new_artifact)
                    print(f"Вы нашли новый артефакт: {new_artifact}")
            
            # Восстановление здоровья
            heal_amount = random.randint(15, 25)
            self.hero.health = min(self.hero.max_health, self.hero.health + heal_amount)
            print(f"Ваше здоровье восстановлено на {heal_amount} HP. Теперь у вас {self.hero.health} HP")
            return True
        
        return False
    
    def final_battle_with_vecna(self):
        print_header("ФИНАЛЬНАЯ БИТВА")
        print_slow("ФИНАЛЬНАЯ БИТВА С ВЕКНОЙ!")
        print_slow("Все герои Хоукинса собираются для решающей битвы!")
        print_slow("Векна: 'Хоукинс будет поглощен Изнанкой! Ничто не остановит меня!'")
        
        # Создаем всех героев для финальной битвы
        all_heroes = [
            self.hero,
            Hero("Майк", 100, 15, "heal", "Мотивация"),
            Hero("Дастин", 90, 18, "stun", "Стратег"),
            Hero("Уилл", 80, 20, "double_attack", "Связь с Изнанкой"),
            Hero("Элевен", 120, 25, "heal", "Телекинез"),
            Hero("Хоппер", 150, 20, "stun", "Сила полицейского"),
            Hero("Лукас", 85, 22, "double_attack", "Меткий стрелок"),
            Hero("Стив", 110, 18, "heal", "Защитник")
        ]
        
        vecna = Enemy("Векна", 250, 30)
        
        # Артефакты против Векны
        if "Кассета с любимой музыкой (ослабляет Векну)" in self.hero.artifacts:
            print("Кассета с любимой музыкой ослабляет Векну!")
            vecna.damage -= 8
            vecna.health -= 40
            print("Векна вздрагивает от звуков музыки!")
        
        if "Секретные записи (раскрывают слабости врагов)" in self.hero.artifacts:
            print("Секретные записи помогают найти слабость Векны!")
            vecna.damage -= 5
        
        round_num = 1
        while vecna.is_alive() and any(hero.is_alive() for hero in all_heroes):
            print_header(f"РАУНД {round_num}")
            print(f"Векна: {vecna.health} HP")
            print("\nГерои:")
            for hero in all_heroes:
                if hero.is_alive():
                    print(f"  {hero.name}: {hero.health} HP")
                else:
                    print(f"  {hero.name}: 💀 ПОВЕРЖЕН")
            
            # Ход героев
            for hero in all_heroes:
                if hero.is_alive() and vecna.is_alive():
                    print(f"\n{'-'*30}")
                    print(f"Ход {hero.name}:")
                    
                    if hero == self.hero:  # Игрок управляет главным героем
                        print("1. Атаковать Векну")
                        print("2. Использовать способность")
                        print("3. Позвать дополнительную помощь")
                        print("4. Использовать артефакт")
                        
                        choice = input("Ваш выбор: ")
                        
                        if choice == "1":
                            hero.attack(vecna)
                        
                        elif choice == "2":
                            ability_result = hero.use_ability()
                            
                            # Особенность Оди
                            if ability_result == "instant_kill":
                                print("\n" + "!"*60)
                                print("ОДИ ИСПОЛЬЗУЕТ СЕКРЕТНОЕ ОРУЖИЕ!")
                                print("ВЕКНА ПОЛНОСТЬЮ УНИЧТОЖЕН!")
                                print("!"*60)
                                vecna.health = 0
                                break
                        
                        elif choice == "3":
                            if "Рация (позволяет позвать друга в любой момент)" in hero.artifacts:
                                friend = random.choice(self.friends)
                                friend_damage, damage_type = hero.call_friend(friend)
                                if isinstance(friend_damage, int):
                                    vecna.health -= friend_damage
                        
                        elif choice == "4":
                            if self.hero.artifacts:
                                print("\nВаши артефакты:")
                                for i, artifact in enumerate(self.hero.artifacts, 1):
                                    print(f"{i}. {artifact}")
                                
                                try:
                                    artifact_choice = int(input("Выберите артефакт: ")) - 1
                                    if 0 <= artifact_choice < len(self.hero.artifacts):
                                        artifact = self.hero.artifacts[artifact_choice]
                                        print(f"Используется {artifact}")
                                        
                                        if "Кристалл" in artifact:
                                            print("Кристалл усиливает атаку всех героев!")
                                            for h in all_heroes:
                                                if h.is_alive():
                                                    h.damage += 5
                                        elif "Рождественские огоньки" in artifact:
                                            print("Огоньки защищают героев!")
                                            vecna.damage -= 3
                                except:
                                    print("Не удалось использовать артефакт!")
                    else:
                        # Другие герои атакуют автоматически
                        if random.random() < 0.4:  # 40% шанс использовать способность
                            hero.use_ability()
                        else:
                            hero.attack(vecna)
            
            # Ход Векны
            if vecna.is_alive():
                print(f"\n{'-'*30}")
                print("Ход Векны:")
                # Векна атакует случайных живых героев (1-3 за ход)
                alive_heroes = [h for h in all_heroes if h.is_alive()]
                attacks = random.randint(1, min(3, len(alive_heroes)))
                
                for _ in range(attacks):
                    if alive_heroes and vecna.is_alive():
                        target = random.choice(alive_heroes)
                        vecna.attack(target)
                        if not target.is_alive():
                            alive_heroes.remove(target)
                            print(f"{target.name} пал в бою...")
            
            round_num += 1
            input("\nНажмите Enter для продолжения...")
        
        if not vecna.is_alive():
            print_header("ПОБЕДА!")
            print("ВЕКНА ПОБЕЖДЕН!")
            print("Портал в Изнанку начинает закрываться...")
            self.vecna_defeated = True
            return True
        else:
            print_header("ПОРАЖЕНИЕ")
            print("Все герои повержены...")
            print("Хоукинс поглощен Изнанкой...")
            return False
    
    def close_portal(self):
        print_header("ЗАКРЫТИЕ ПОРТАЛА")
        print_slow("С ПОРАЖЕНИЕМ ВЕКНЫ, ПОРТАЛ В ИЗНАНКУ НАЧИНАЕТ ЗАКРЫВАТЬСЯ!")
        print_slow("Элевен использует все свои силы, чтобы навсегда закрыть портал...")
        print_slow("МОЛНИЯ БЬЕТ В ЦЕНТР ПОРТАЛА...")
        print_slow("ПОРТАЛ ЗАКРЫВАЕТСЯ! ХОУКИНС В БЕЗОПАСНОСТИ!")
        self.portal_open = False
    
    def play(self):
        show_loading_screen()
        
        print_header("ОЧЕНЬ СТРАННЫЕ ДЕЛА: БИТВА ЗА ХОУКИНС")
        
        # Выбор персонажа
        self.choose_hero()
        
        # Выбор артефактов
        self.choose_artifacts()
        
        # Начало игры
        input("\nНажмите Enter, чтобы начать игру...")
        
        # Введение
        print_header("1984 ГОД, ХОУКИНС")
        print_slow("1984 год, Хоукинс, Индиана.")
        print_slow(f"{self.hero.name} и его друзья замечают странные явления в городе.")
        print_slow("Люди исчезают, животные ведут себя странно, а из леса доходят жуткие звуки...")
        
        # Битва с демогоргоном
        input("\nНажмите Enter, чтобы продолжить...")
        if not self.battle_with_demogorgon():
            return
        
        # Открытие портала
        input("\nНажмите Enter, чтобы продолжить...")
        self.open_portal()
        
        # Еще одна битва
        input("\nНажмите Enter, чтобы продолжить...")
        print("\nЕще больше демогоргонов появляется из портала!")
        if not self.battle_with_demogorgon("Демогоргон-альфа", 80, 15):
            return
        
        # Финальная битва с Векной
        input("\nНажмите Enter, чтобы начать финальную битву...")
        if self.final_battle_with_vecna():
            # Закрытие портала
            self.close_portal()
            
            # Финал
            print_header("ИГРА ПРОЙДЕНА УСПЕШНО!")
            print("\nВаши достижения:")
            print(f"Герой: {self.hero.name}")
            print(f"Собрано артефактов: {len(self.hero.artifacts)}")
            print("\nХоукинс спасен! Но...")
            print_slow("Изнанка всегда будет рядом...")
            print_slow("Конец... или начало?")
            print("\n✓ Спасибо за игру!")
        else:
            print("\n✗ Попробуйте еще раз! Возможно, выберите другие артефакты или персонажа.")
        
        input("\nНажмите Enter, чтобы вернуться в главное меню...")
