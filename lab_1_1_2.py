# 1.2 Считать с клавиатуры три произвольных числа, 
#               вывести в консоль те числа, которые попадают в интервал [1, 50].  

def get_number_1(numb_x):
    while True:
        try:
            num = float(input(numb_x))
            return num
        except ValueError:
            print("Ошибка: введите число!")

# Используем функцию для ввода всех трёх чисел
num1 = get_number_1("Введите первое число: ")
num2 = get_number_1("Введите второе число: ")
num3 = get_number_1("Введите третье число: ")

numbers = [num1, num2, num3]
result = [num for num in numbers if 1 <= num <= 50]

if result:  
    print("Числа, попадающие в интервал [1, 50]:", result)
else:  
    print("Ни одно число не попадает в интервал [1, 50].")
