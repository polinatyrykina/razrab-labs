# 1.2 Считать с клавиатуры три произвольных числа, 
#               вывести в консоль те числа, которые попадают в интервал [1, 50].  

def get_number_1(numb_x):
    while True:
        try:
            num = float(input(numb_x))
            return num
        except ValueError:
            print("Ошибка: введите число!")

num1 = float(input("Введите первое число: "))
num2 = float(input("Введите второе число: "))
num3 = float(input("Введите третье число: "))

numbers = [num1, num2, num3]
result = [num for num in numbers if 1 <= num <= 50]

if result:  
    print("Числа, попадающие в интервал [1, 50]:", result)
else:  
    print(str("Ни одно число не попадает в интервал [1, 50]."))
