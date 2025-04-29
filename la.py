# 1. Считываем строку с числами
print("Введите элементы массива в одну строку через пробел:")
input_data = input()

# 2. Обрабатываем строку и формируем массив чисел
array = []
num_str = ""  # Временная строка для накопления цифр числа
for char in input_data:
    if char == ' ':
        if num_str:  # Если строка не пустая
            array.append(int(num_str))  # Добавляем число в массив
            num_str = ""  # Сбрасываем временную строку
    else:
        num_str += char  # Добавляем символ к текущему числу

# Добавляем последнее число (если строка не заканчивается пробелом)
if num_str:
    array.append(int(num_str))

# 3. Вычисляем сумму элементов массива
sum_elements = 0
for num in array:
    sum_elements += num
print("Сумма элементов массива:", sum_elements)

# 4. Вычисляем произведение элементов массива
product_elements = 1
for num in array:
    product_elements *= num
print("Произведение элементов массива:",product_elements)

# 5. Заменяем нулевые элементы на среднее арифметическое
average = sum_elements / len(array)  # Вычисляем среднее арифметическое
for i in range(len(array)):
    if array[i] == 0:
        array[i] = average

# 6. Выводим измененный массив
print("Массив после замены нулей на среднее арифметическое:")
print(array)