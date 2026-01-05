import hashlib
import time

class AuthSystem:
    def __init__(self):
        # Храним логины и хеши паролей
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
        print("\n" + "="*50)
        print("ВХОД В ИГРУ 'ОЧЕНЬ СТРАННЫЕ ДЕЛА'")
        print("="*50)
        
        attempts = 0
        
        while attempts < self.max_attempts:
            print(f"\nПопытка {attempts + 1} из {self.max_attempts}")
            
            username = input("Введите логин: ")
            password = input("Введите пароль: ")
            
            # Проверка учетных данных
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
        
        # Если все попытки исчерпаны
        print(f"\n✗ Превышено количество попыток входа!")
        print(f"Система заблокирована на {self.lock_time} секунд...")
        
        # Отсчет времени блокировки
        for i in range(self.lock_time, 0, -1):
            print(f"До разблокировки: {i} секунд", end='\r')
            time.sleep(1)
        
        print("\nСистема разблокирована. Попробуйте снова.")
        return False
    
    def register(self):
        """Регистрация нового пользователя (дополнительная функция)"""
        print("\n" + "="*50)
        print("РЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ")
        print("="*50)
        
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
            
            # Подтверждение пароля
            confirm_password = input("Подтвердите пароль: ")
            
            if password != confirm_password:
                print("Пароли не совпадают!")
                continue
            
            # Сохранение пользователя
            self.users[username] = self._hash_password(password)
            print(f"\n✓ Регистрация успешна! Пользователь {username} создан.")
            
            # Автоматический вход после регистрации
            print("Выполняется автоматический вход...")
            time.sleep(2)
            return True
    
    def show_menu(self):
        """Главное меню авторизации"""
        while True:
            print("\n" + "="*50)
            print("ИГРА 'ОЧЕНЬ СТРАННЫЕ ДЕЛА'")
            print("="*50)
            print("1. Войти в игру")
            print("2. Зарегистрироваться")
            print("3. Выйти")
            print("="*50)
            
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
