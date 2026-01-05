from auth import AuthSystem
from game import Game
from utils import print_header, show_loading_screen
import time

def main():
    """Главная функция программы"""
    auth_system = AuthSystem()
    
    while True:
        # Показываем меню авторизации
        if not auth_system.show_menu():
            break
        
        # Если авторизация успешна, запускаем игру
        show_loading_screen("Подготовка игры...")
        
        while True:
            game = Game()
            game.play()
            
            # Спрашиваем, хочет ли игрок сыграть еще раз
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

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nИгра прервана пользователем.")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        print("Пожалуйста, перезапустите игру.")
