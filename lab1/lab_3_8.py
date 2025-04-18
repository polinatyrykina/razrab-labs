# Задание 3.8
# 1. Считать из параметров командной строки одномерный массив, 
#               состоящий из N целочисленных элементов.
# 2. Вывести в консоль сумму элементов списка.
# 3. Вывести в консоль произведение элементов списка.
# 4. Заменить все нулевые элементы на среднее арифметическое всех 
#               элементов массива. Вывести результат в консоль.

import sys

# 1. Считать массив из параметров командной строки
arr = list(map(int, sys.argv[1:]))

# 2. Вывести сумму элементов
print('Сумма:', sum(arr))

# 3. Вывести произведение элементов
product = 1
for num in arr:
    product *= num
print('Произведение:', product)

# 4. Заменить нулевые элементы на среднее арифметическое
if len(arr) > 0:
    average = sum(arr) / len(arr)
    new_arr = [average if num == 0 else num for num in arr]
    print('Массив после замены нулей:', new_arr)
else:
    print('Массив пуст')