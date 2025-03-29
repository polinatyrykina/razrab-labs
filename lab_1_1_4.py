# 1.4 Считать с клавиатуры непустую произвольную последовательность целых чисел.
                #Найти:
                    #
                    # Сумму всех чисел последовательности (решить задачу используя 
                    # циклическую конструкцию while)

                    # Количество всех чисел последовательности (решить задачу используя
                    # циклическую конструкцию while)


print("Считаем сумму. Введите числа через пробел:")
input_str = input().strip() + ' '  # Добавляем пробел для обработки всех чисел, в том числе последнего! 

total_sum = 0
i = 0
num_str = ""

while i < len(input_str):
    char = input_str[i]
    if char == ' ':
        if num_str:  # Если строка числа не пуста
            total_sum += int(num_str)
            num_str = ""  # Сброс
    else:
        num_str += char  # Накапливаем цифры числа
    i += 1

print(f"Сумма всех чисел: {total_sum}")

print("Считаем количество. Введите числа через пробел:")
input_str = input().strip() + ' ' 

count = 0
i = 0
num_str = ""

while i < len(input_str):
    char = input_str[i]
    if char == ' ':
        if num_str:
            count += 1
            num_str = ""
    else:
        num_str += char 
    i += 1

print(f"Количество всех чисел: {count}")