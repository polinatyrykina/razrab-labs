# 1.1 Считать с клавиатуры три произвольных числа, найти минимальное среди них и вывести на экран.  

# проверка на ввод числа

def get_number(numb):
    while True:
        try:
            num = float(input(numb))
            return num
        except ValueError:
            print("Ошибка: введите число!")

num1 = get_number("Введите первое число: ")
num2 = get_number("Введите второе число: ")
num3 = get_number("Введите третье число: ")

min_num = min(num1, num2, num3)

print("Минимальное число:", min_num)
