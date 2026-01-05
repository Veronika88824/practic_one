import random
import time
import sys
import hashlib

# ===================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====================
def print_slow(text, delay=0.03):
    """Медленный вывод текста для драматического эффекта"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_header(title):
    """Вывод заголовка"""
    print("\n" + "="*60)
    print(f"{title:^60}")
    print("="*60)

def show_loading_screen(message="Загрузка игры..."):
    """Показать экран загрузки"""
    print_header("ЗАГРУЗКА")
    print(f"\n{message}")
    for i in range(3):
        print(".", end='', flush=True)
        time.sleep(0.5)
    print("\n")

# ===================== КЛАСС АВТОРИЗАЦИИ =====================
class AuthSystem:
    def __init__(self):
        self.users = {
            "12345": self._hash_password("zachet")  # Логин: 12345, Пароль: zachet
        }
        self.max_attempts = 3
        self.lock_time = 30  # секунд
    
    def _hash_password(self, password):
        """Хеширование пароля"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self):
        """Процесс входа в систему"""
        print_header("ВХОД В ИГРУ 'ОЧЕНЬ СТРАННЫЕ ДЕЛА'")
        
        attempts = 0
        
        while attempts < self.max_attempts:
            print(f"\nПопытка {attempts + 1} из {self.max_attempts}")
            username = input("Введите логин: ")
            password = input("Введите пароль: ")
            
            if username in self.users:
                hashed_password = self._hash_password(password)
                if self.users[username] == hashed_password:
                    print("\n✓ Авторизация успешна!")
                    print(f"Добро пожаловать, пользователь {username}!")
                    time.sleep(1)
                    return True
                else:
                    print("✗ Неверный пароль!")
            else:
                print("✗ Пользователь не найден!")
            
            attempts += 1
            
            if attempts < self.max_attempts:
                print(f"Осталось попыток: {self.max_attempts - attempts}")
        
        print(f"\n✗ Превышено количество попыток входа!")
        print(f"Система заблокирована на {self.lock_time} секунд...")
        
        for i in range(self.lock_time, 0, -1):
            print(f"До разблокировки: {i} секунд", end='\r')
            time.sleep(1)
        
        print("\nСистема разблокирована. Попробуйте снова.")
        return False
    
    def register(self):
        """Регистрация нового пользователя"""
        print_header("РЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ")
        
        while True:
            username = input("\nВведите новый логин (минимум 3 символа): ")
            
            if len(username) < 3:
                print("Логин должен содержать минимум 3 символа!")
                continue
            
            if username in self.users:
                print("Этот логин уже занят!")
                continue
            
            password = input("Введите пароль (минимум 4 символа): ")
            
            if len(password) < 4:
                print("Пароль должен содержать минимум 4 символа!")
                continue
            
            confirm_password = input("Подтвердите пароль: ")
            
            if password != confirm_password:
                print("Пароли не совпадают!")
                continue
            
            self.users[username] = self._hash_password(password)
            print(f"\n✓ Регистрация успешна! Пользователь {username} создан.")
            
            print("Выполняется автоматический вход...")
            time.sleep(2)
            return True
    
    def show_menu(self):
        """Главное меню авторизации"""
        while True:
            print_header("ИГРА 'ОЧЕНЬ СТРАННЫЕ ДЕЛА'")
            print("1. Войти в игру")
            print("2. Зарегистрироваться")
            print("3. Выйти")
            print("="*60)
            
            choice = input("Выберите действие (1-3): ")
            
            if choice == "1":
                if self.login():
                    return True
            elif choice == "2":
                self.register()
            elif choice == "3":
                print("До свидания!")
                return False
            else:
                print("Неверный выбор! Попробуйте снова.")

# ===================== КЛАССЫ ПЕРСОНАЖЕЙ =====================
class Hero:
    def __init__(self, name, health, damage, ability, ability_desc):
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage
        self.ability = ability
        self.ability_desc = ability_desc
        self.artifacts = []
        self.next_attack_double = False
    
    def attack(self, enemy):
        damage_dealt = self.damage
        
        if self.next_attack_double:
            damage_dealt *= 2
            self.next_attack_double = False
            print(f"{self.name} использует двойную атаку!")
        
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
        elif friend_name == "Лукас":
            print("Лукас метко стреляет из рогатки и наносит 18 урона!")
            return 18, "single"
        elif friend_name == "Нэнси":
            print("Нэнси стреляет из ружья и наносит 22 урона!")
            return 22, "single"
        
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
        self.stunned = True
    
    def is_alive(self):
        return self.health > 0

# ===================== ОСНОВНОЙ КЛАСС ИГРЫ =====================
class Game:
    def __init__(self):
        self.hero = None
        self.artifacts = []
        self.portal_open = False
        self.vecna_defeated = False
        
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
            "Секретные записи (раскрывают слабости врагов)",
            "Зуб демодога (увеличивает урон на 3)",
            "Записная книжка (открывает секреты Изнанки)",
            "Компас (помогает ориентироваться в Изнанке)",
            "Светящаяся палочка (отпугивает тварей Изнанки)",
            "Старый транзистор (ловит сигналы из Изнанки)"
        ]
        
        self.heroes = {
            "1": ("Майк", Hero("Майк", 100, 15, "heal", "Мотивация: восстанавливает здоровье себе и союзникам")),
            "2": ("Дастин", Hero("Дастин", 90, 18, "stun", "Стратег: оглушает врага на один ход")),
            "3": ("Уилл", Hero("Уилл", 80, 20, "double_attack", "Связь с Изнанкой: следующая атака наносит двойной урон")),
            "4": ("Оди (чит)", Hero("Оди", 120, 25, "instant_kill", "Секретное оружие: мгновенно побеждает Векну"))
        }
        
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
                elif ability_result == "heal":
                    if demogorgon.is_alive():
                        demogorgon.attack(self.hero)
            
            elif choice == "3":
                if "Рация (позволяет позвать друга в любой момент)" in self.hero.artifacts:
                    print("\nКого вы хотите позвать?")
                    for i, friend in enumerate(self.friends[:6], 1):
                        print(f"{i}. {friend}")
                    
                    try:
                        friend_choice = int(input("Выберите друга: ")) - 1
                        if 0 <= friend_choice < 6:
                            friend = self.friends[friend_choice]
                            friend_damage, damage_type = self.hero.call_friend(friend)
                            
                            if isinstance(friend_damage, int):
                                if damage_type == "all":
                                    demogorgon.health -= friend_damage
                                else:
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
                if self.hero.artifacts:
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
                            elif "Волейбольный мяч" in artifact:
                                print("Волейбольный мяч напоминает о дружбе и дает +10 HP!")
                                self.hero.health = min(self.hero.max_health, self.hero.health + 10)
                    except:
                        print("Не удалось использовать артефакт!")
                else:
                    print("У вас нет артефактов для использования!")
            
            else:
                print("Неверный выбор! Пропускаете ход.")
                if demogorgon.is_alive():
                    demogorgon.attack(self.hero)
            
            if not self.hero.is_alive():
                print(f"\n✗ {self.hero.name} побежден! Игра окончена.")
                return False
        
        if not demogorgon.is_alive():
            print(f"\n✓ ПОБЕДА! Вы победили {enemy_name}!")
            
            if random.random() < 0.7:
                new_artifact = random.choice(self.available_artifacts)
                if new_artifact not in self.hero.artifacts:
                    self.hero.artifacts.append(new_artifact)
                    print(f"Вы нашли новый артефакт: {new_artifact}")
            
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
            
            for hero in all_heroes:
                if hero.is_alive() and vecna.is_alive():
                    print(f"\n{'-'*30}")
                    print(f"Ход {hero.name}:")
                    
                    if hero == self.hero:
                        print("1. Атаковать Векну")
                        print("2. Использовать способность")
                        print("3. Позвать дополнительную помощь")
                        print("4. Использовать артефакт")
                        
                        choice = input("Ваш выбор: ")
                        
                        if choice == "1":
                            hero.attack(vecna)
                        
                        elif choice == "2":
                            ability_result = hero.use_ability()
                            
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
                                        elif "Энергия Верхнего мира" in artifact:
                                            print("Энергия Верхнего мира усиливает всех героев!")
                                            for h in all_heroes:
                                                if h.is_alive():
                                                    h.health += 10
                                except:
                                    print("Не удалось использовать артефакт!")
                    else:
                        if random.random() < 0.4:
                            hero.use_ability()
                        else:
                            hero.attack(vecna)
            
            if vecna.is_alive():
                print(f"\n{'-'*30}")
                print("Ход Векны:")
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
        
        self.choose_hero()
        self.choose_artifacts()
        
        input("\nНажмите Enter, чтобы начать игру...")
        
        print_header("1984 ГОД, ХОУКИНС")
        print_slow("1984 год, Хоукинс, Индиана.")
        print_slow(f"{self.hero.name} и его друзья замечают странные явления в городе.")
        print_slow("Люди исчезают, животные ведут себя странно, а из леса доходят жуткие звуки...")
        
        input("\nНажмите Enter, чтобы продолжить...")
        if not self.battle_with_demogorgon():
            return
        
        input("\nНажмите Enter, чтобы продолжить...")
        self.open_portal()
        
        input("\nНажмите Enter, чтобы продолжить...")
        print("\nЕще больше демогоргонов появляется из портала!")
        if not self.battle_with_demogorgon("Демогоргон-альфа", 80, 15):
            return
        
        print("\nВы слышите голос Векны в своей голове...")
        print_slow("Векна: 'Приди ко мне... Хоукинс будет моим...'")
        
        input("\nНажмите Enter, чтобы начать финальную битву...")
        if self.final_battle_with_vecna():
            self.close_portal()
            
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

# ===================== ГЛАВНАЯ ФУНКЦИЯ =====================
def main():
    """Главная функция программы"""
    auth_system = AuthSystem()
    
    while True:
        if not auth_system.show_menu():
            break
        
        show_loading_screen("Подготовка игры...")
        
        while True:
            game = Game()
            game.play()
            
            print_header("ГЛАВНОЕ МЕНЮ")
            print("1. Начать новую игру")
            print("2. Сменить пользователя")
            print("3. Выйти из игры")
            
            choice = input("\nВыберите действие (1-3): ")
            
            if choice == "1":
                print("Запуск новой игры...")
                time.sleep(1)
                continue
            elif choice == "2":
                print("Возврат к экрану входа...")
                time.sleep(1)
                break
            elif choice == "3":
                print("\nСпасибо за игру! До свидания!")
                return
            else:
                print("Неверный выбор!")

# ===================== ЗАПУСК ПРОГРАММЫ =====================
if __name__ == "__main__":
    try:
        print("\n" + "="*60)
        print("ОЧЕНЬ СТРАННЫЕ ДЕЛА: БИТВА ЗА ХОУКИНС")
        print("="*60)
        print("Добро пожаловать в игру!")
        print("Для входа используйте:")
        print("Логин: 12345")
        print("Пароль: zachet")
        print("="*60)
        time.sleep(2)
        
        main()
    except KeyboardInterrupt:
        print("\n\nИгра прервана пользователем.")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        print("Пожалуйста, перезапустите игру.")
    finally:
        input("\nНажмите Enter для выхода...")
