# 2.8 Задание
# 1. Считать с клавиатуры произвольную строку.
# 2. Вывести количество слов в строке.

input_string = input("Введите строку: ")
word_count = 0
in_word = False

# Проходим по каждому символу в строке
for char in input_string:
    if char != ' ' and not in_word:
        word_count += 1
        in_word = True
    # Если символ является пробелом
    elif char == ' ':
        in_word = False

print("Количество слов в строке:", word_count)