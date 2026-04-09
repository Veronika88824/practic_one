from pathlib import Path
import os

#Автоматический поиск пути к файлу с кодом
script_dir = Path(__file__).parent

file1_path = script_dir / "file1.txt" #Построение пути файла "file1.txt"
file2_path = script_dir / "file2.txt" #Построение пути файла "file2.txt"

#Главная функция программы
def calculate():
    #Главный цикл
    while True:
        #Чтение файлов
        try:
            with open(file1_path, 'r') as f1:
                set1 = set(f1.read().strip().split(","))

            with open(file2_path, 'r') as f2:
                set2 = set(f2.read().strip().split(","))

        except FileNotFoundError:
            print("Ошибка: Файлы file1.txt или file2.txt не найдены в папке со скриптом!")
            exit()

        #Список допустимых действий
        ops = ['Пересечение', 'Объединение', 'Разность', 'Симметрическая разность', 'Декартево произведение', 'Редактировать множества', 'Закрыть кальклятор']
        
        print('\n''Приветствуем вас в КАЛЬКУЛЯТОРЕ МНОЖЕСТВ!')
        print('='*50)
        print('Доступные операции:')
        print('-'*26)
        for n, i in enumerate(ops, 1):
            print(f"{n}. {i}")
        print('='*50)

        #Цикл проверки ввода запроса от пользователя
        while True:
            try:
                ch = int(input('Выберите операцию над множеством (1-7): '))
                if 1 <= ch <= 7:
                    break #Запрос удовлитворяет условия
                else:
                    print('='*50)
                    print("❌ Введите допустимый вариант ❌")
                    print('='*50)
            except ValueError:
                print('='*50)
                print("❌ Введите корректный запрос ❌")
                print('='*50)
        
        print('='*50)
        print("✅ Ваш запрос принят!")
        print('='*50)
        print(' ')
        print('='*50)
        print('🔽 Исходные множества 🔽')
        print('-'*50)
        print(f'Множество А: {set1}')
        print(f'Множество Б: {set2}')

        #Выполнения операции в зависимости от выбора пользователя
        if ch == 1:
            res = set1 & set2 #Пересечение
        
        elif ch == 2:
            res = set1 | set2 #Объединение
        
        elif ch == 3:
            res = set1 - set2 #Разность
        
        elif ch == 4:
            res = set1 ^ set2 #Симметрическая разность
        
        elif ch == 5:
            print('-'*50)
            res = {(a, b) for a in set1 for b in set2}
            print("🔽 Результат вашего запроса 🔽")
            print(f'{sorted(res)}')
            print('-'*50)
            print("🔽 Мощность по вашему запросу 🔽")
            print(f'{len(res)}')
            print('='*50)
        
        elif ch == 6:
            print('='*50)
            print('⚠️  Редактирование множеств ⚠️')
            print('-'*50)
            print('Вам необходимо ввести новые элементы множества')
            print('-'*50)
            print('-> Все элементы вводятся через запятую')
            print('-> Для создания пустого множества нажмите Enter')
            print('-> Для отмены можете ввести слово <<отмена>>')
            print('='*50)

            #Работа с новым множеством в первом файле
            set_inp_f1 = input('Для множества А (file1.txt): ').strip()
            if set_inp_f1.lower() == 'отмена': #Случай, если пользователь отемнит редактирование
                print('='*50)
                print('⚠️  Вы отменили редактирование ⚠️')
                print('-'*50)
                print('Возвращаем исходные множества')
                print('='*50)
            if set_inp_f1 == '': #Случай, если пользователь создает пустое множетво
                print('-'*50)
                print('-> Множество А - пустое')
                print('-'*50)

            #Работа с новым множеством во втором файле
            set_inp_f2 = input('Для множества Б (file2_txt): ').strip()
            if set_inp_f2.lower() == 'отмена':
                print('='*50)
                print('⚠️  Вы отменили редактирование ⚠️')
                print('-'*50)
                print('Возвращаем исходные множества')
                print('='*50)
                continue
            if set_inp_f2 == '':
                print('-'*50)
                print('-> Множество Б - пустое')

            #Перезапись файлов со множествами
            try:
                with open (file1_path, 'w') as f1:
                    f1.write(set_inp_f1) #Перезапись первого файла
                with open (file2_path, 'w') as f2:
                    f2.write(set_inp_f2) #Перезапись второго файла
                print('='*50)
                print('✅ Редактирование прошлло упешно')
                print('='*50)
                continue
            except Exception:
                print('-'*50)
                print(f'Ошибка редактирования {Exception}')
                print('='*50)
                continue

        elif ch == 7:
            print('='*50)
            print("🔚 До вчтречи!")
            print('='*50)
            res = None
            break
        else:
            res = None
            print('='*50)
            print("❌ Введите допутсимый вариант действия ❌")
        
        #Вывод результата при корректном запросе пользователя
        if res is not None and ch != 5:
            print('-'*50)
            print("🔽 Результат вашего запроса 🔽")
            print('-'*50)
            print(sorted(list(res)))
            print('='*50)

calculate()