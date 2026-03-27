import numpy as np

#Шкала Саати
saaty_scale = [
    [1,  "Равная важность "],
    [2,  "Промежуточное (1-3) "],
    [3,  "Некоторое преобладание "],
    [4,  "Промежуточное (3-5) "],
    [5,  "Существенное преобладание "],
    [6,  "Промежуточное (5-7) "],
    [7,  "Значительное преобладание "],
    [8,  "Промежуточное (7-9) "],
    [9,  "Абсолютное преобладание "]
]

#Список допустимых значений шкалы Саати
saaty_values = [item[0] for item in saaty_scale]

print('-' * 70)
print('Здравствуйте, для начала подбора работы ознакомьтесь со шкалой Саати')
print('Она поможет с процессом подбора')
print('-' * 70)
print(f"{'Степень значимости':<25} {'Определение':25}")
print('-' * 70)
for item in saaty_scale:
    print(f"{' '*8}{item[0]:<16} {item[1]:<25}")

#Функция создания матрицы попарных сравнений
def create_matrix(n, name=''):

    print('-'*70)
    print(f'Сейчас вам необходимо заполнить матрицу: {name}')
    print('-'*70)
    matrix = np.ones((n, n), dtype=float)
    
    #Заполнение матрицы
    for i in range(n):
        for j in range(i + 1, n):
            while True:
                try:
                    print('-' * 70)
                    print('*Вводите ценность критериев относительно шкалы Саати - от 1 до 9*')
                    print('-' * 70)
                    value = int(input(f'Введите важность элемента {i+1} относительно элемента {j+1}: '))
                    
                    #Проверка наличия значения в шкале Саати
                    if value in saaty_values:
                        matrix[i, j] = value        # Прямое значение
                        matrix[j, i] = 1.0 / value  # Обратное значение (свойство обратносимметричности)
                        print(f'✓ Значение {value} принято!')
                        break
                    else:
                        print('-' * 70)
                        print(f'ОШИБКА: Значение {value} не в шкале Саати!')
                        print('Допустимые значения:', saaty_values)
                        print('-' * 70)
                        
                except ValueError:
                    print('-' * 70)
                    print('ОШИБКА: Введите целое число от 1 до 9!')
                    print('-' * 70)

    print('=' * 70)
    print(f'Матрица "{name}" создана успешно!')
    print('=' * 70)
    print('\nИтоговая матрица:')
    print(matrix)
    return matrix

#Функция нормализации созданной матрицы
def normalization_matrix(matrix):

    columns_amount = np.sum(matrix, axis=0)  #axis=0 - сумма по столбцам матрицы
    normalized = matrix / columns_amount     #Деление каждого элемента на сумму столбца
    return normalized

#Функция расчёта приоритетов (весов) - среднее значение по строке
def calculation_weights(normalized_matrix):

    weights = np.mean(normalized_matrix, axis=1)#axis=1 - среднее по строкам
    return weights

#Функция проверки согласованности выставленных оценок
def checking_logic(matrix, weights):
    
    n = len(matrix)  # Размер матрицы
    
    #Умножаем матрицу на вектор весов для расчёта максимального собственного значения
    Aw = np.dot(matrix, weights)
    
    #Находим максимальное собственное значение (λ_max)
    lyam_max = np.mean(Aw / weights)
    
    #Индекс согласованности (CI) - показывает отклонение от идеальной согласованности
    CI = (lyam_max - n) / (n - 1)
    
    #Случайный индекс согласованности (RI) - табличные значения
    RI_table = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}
    RI = RI_table.get(n, 1.45)
    
    # Отношение согласованности (CR)
    if RI != 0:
        CR = CI / RI
    else:
        CR = 0 

    print(f'Проверка согласованности:')

    print(f'Отношение согласованности (CR) = {CR}')
    
    if CR <= 0.1:
        print('Суждения согласованы (CR ≤ 0.1)')
    else:
        print('Суждения несогласованы (CR > 0.1). Рекомендуется пересмотреть оценки!')
    
    return CR

# Функция расчёта итоговых весов альтернатив
def calculate_final_weights(criteria_weights, alternatives_matrices):

    num_alternatives = len(alternatives_matrices[0])
    final_weights = np.zeros(num_alternatives)
    
    #Для каждой альтернативы суммируем взвешенные оценки по всем критериям
    for i in range(num_alternatives):
        for j, alt_weights in enumerate(alternatives_matrices):
            final_weights[i] += alt_weights[i] * criteria_weights[j]
    
    return final_weights

#Функция запуска программы
def main():
    
    #Ввод количества критериев
    n_criteria = int(input('Введите количество критериев (не менее 5): '))
    
    #Ввод названий критериев
    criteria_names = []
    print('Введите названия критериев:')
    for i in range(n_criteria):
        name = input(f'Критерий {i+1}: ')
        criteria_names.append(name)
    
    #Ввод количества альтернатив
    n_alternatives = int(input('Введите количество вариантов работы (не менее 3): '))
    while n_alternatives < 3:
        print('Должно быть не менее 3 вариантов работы!')
        n_alternatives = int(input('Введите количество вариантов работы (не менее 3): '))
    
    #Ввод названий альтернатив
    alternative_names = []
    print('Введите названия вариантов работы:')
    for i in range(n_alternatives):
        name = input(f'Вариант {i+1}: ')
        alternative_names.append(name)
    
    #Построение матрицы попарных сравнений критериев
    print('\n' + '-' * 70)
    print('ЭТАП 1: Сравнение критериев между собой')
    print('-' * 70)
    criteria_matrix = create_matrix(n_criteria, 'Сравнение критериев')
    
    #Нормализация матрицы критериев и расчёт весов
    criteria_normalized = normalization_matrix(criteria_matrix)
    criteria_weights = calculation_weights(criteria_normalized)
    
    #Проверка согласованности матрицы критериев
    checking_logic(criteria_matrix, criteria_weights)
    
    #Вывод весов критериев
    print('\n' + '=' * 70)
    print('ВЕСА КРИТЕРИЕВ:')
    print('=' * 70)
    for i, name in enumerate(criteria_names):
        print(f'{name}: {criteria_weights[i]:.4f} ({criteria_weights[i]*100:.1f}%)')
    
    #Построение матриц попарных сравнений альтернатив по каждому критерию
    print('\n' + '=' * 70)
    print('ЭТАП 2: Сравнение альтернатив по каждому критерию')
    print('=' * 70)
    
    alternatives_weights_matrix = []  # Матрица весов альтернатив по критериям
    
    for i, crit_name in enumerate(criteria_names):
        print(f'\n--- Критерий: {crit_name} ---')
        alt_matrix = create_matrix(n_alternatives, f'Альтернативы по критерию "{crit_name}"')
        
        # Нормализация и расчёт весов альтернатив по текущему критерию
        alt_normalized = normalization_matrix(alt_matrix)
        alt_weights = calculation_weights(alt_normalized)
        
        # Проверка согласованности
        checking_logic(alt_matrix, alt_weights)
        
        alternatives_weights_matrix.append(alt_weights)
    
    #Расчёт итоговых весов альтернатив
    print('\n' + '-' * 70)
    print('ЭТАП 3: Расчёт итоговых приоритетов альтернатив')
    print('-' * 70)
    
    final_weights = calculate_final_weights(criteria_weights, alternatives_weights_matrix)
    
    #Вывод результатов
    print('Итоговые веса альтернатив:')
    print('-' * 70)
    for i, name in enumerate(alternative_names):
        print(f'{name}: {final_weights[i]:.4f} ({final_weights[i]*100:.1f}%)')
    
    #Определение лучшей альтернативы
    best_index = np.argmax(final_weights)
    print('\n' + '-' * 70)
    print(f'Лучший вариант - {alternative_names[best_index]}')
    print(f'С весом: {final_weights[best_index]*100:.1f}%')
    print('=' * 70)
    
    #Вывод матрицы весов альтернатив по критериям (для анализа)
    print('МАТРИЦА ВЕСОВ АЛЬТЕРНАТИВ ПО КРИТЕРИЯМ:')
    print('-' * 70)
    print(f'{"":<20}', end='')
    for crit_name in criteria_names:
        print(f'{crit_name[:10]:<12}', end='')
    print()
    
    for i, alt_name in enumerate(alternative_names):
        print(f'{alt_name[:20]:<20}', end='')
        for j in range(n_criteria):
            print(f'{alternatives_weights_matrix[j][i]:.3f}       ', end='')
        print()

#Запуск программы
if __name__ == '__main__':
    main()