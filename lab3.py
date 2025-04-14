from flask import Blueprint, request, jsonify
lab3 = Blueprint('lab3', __name__)
import random
import requests

# Раздел I. Подготовка сервера с API.

@lab3.route('/number/')
def no_number():
    return "Ошибка 400. Не передан парметр.", 400


@lab3.route('/number/<int:param>', methods=['GET'])
def get_number(param):
    
    # Генерируем рандомное число 
    random_number = random.random()
    
    # Умножаем рандомное число на значение параметра
    result = random_number * param
    
    # Возвращаем результат в формате JSON
    return jsonify({'result': result})
    

@lab3.route('/number/', methods=['POST'])
def post_number():
    # Получаем JSON-данные из тела запроса
    data = request.get_json()
    
    # Извлекаем значение поля 'jsonParam' из JSON
    json_param = data.get('jsonParam')
    
    # Проверяем, было ли передано поле 'jsonParam'
    if json_param is None:
        # Если поле отсутствует, возвращаем ошибку 400 с сообщением
        return jsonify({'error': 'Поле jsonParam отсутствует'}), 400
    
    # Генерируем случайное число от 0 до 1
    random_number = random.random()
    
    # Случайным образом выбираем операцию из списка: сложение, вычитание, умножение, деление
    operation = random.choice(['+', '-', '*', '/'])
    
    # Выполняем выбранную операцию между случайным числом и значением jsonParam
    if operation == '+':
        result = random_number + json_param
    elif operation == '-':
        result = random_number - json_param
    elif operation == '*':
        result = random_number * json_param
    elif operation == '/':
        # Если операция деления и jsonParam равен 0, возвращаем None (деление на ноль невозможно)
        result = random_number / json_param if json_param != 0 else None
    
    # Если результат None (например, при делении на ноль), возвращаем ошибку 400
    if result is None:
        return jsonify({'error': 'Деление на ноль невозможно'}), 400
    
    # Возвращаем результат в формате JSON
    return jsonify({
        'random_number': random_number,  # Сгенерированное случайное число
        'jsonParam': json_param,         # Значение, переданное в jsonParam
        'operation': operation,          # Выбранная операция
        'result': result                 # Итоговый результат операции
    })


@lab3.route('/number/', methods=['DELETE'])
def delete_number():
    # Генерируем случайное число от 0 до 1
    random_number = random.random()
    
    # Случайным образом выбираем операцию из списка: сложение, вычитание, умножение, деление
    operation = random.choice(['+', '-', '*', '/'])
    
    # Возвращаем результат в формате JSON
    return jsonify({
        'random_number': random_number,  # Сгенерированное случайное число
        'operation': operation           # Выбранная операция
    })

# Раздел II. Отправка запросов на сервер с API.
# Функция для отправки GET запроса
def send_get():
    # Генерируем случайное число от 1 до 10
    number = random.randint(1, 10)
    # Отправляем GET запрос к API
    response = requests.get(f"http://127.0.0.1:5000/number/{number}")
    # Если запрос успешен, возвращаем результат
    if response.status_code == 200:
        return response.json()['result']
    else:
        return None

# Функция для отправки POST запроса
def send_post():
    # Генерируем случайное число от 1 до 10
    number = random.randint(1, 10)
    # Подготавливаем данные для отправки
    data = {"jsonParam": number}
    # Указываем заголовок Content-Type
    headers = {"Content-Type": "application/json"}
    # Отправляем POST запрос к API
    response = requests.post(f"http://127.0.0.1:5000/number/", json=data, headers=headers)
    # Если запрос успешен, возвращаем результат и операцию
    if response.status_code == 200:
        result = response.json()
        return result['result'], result['operation']
    else:
        return None, None

# Функция для отправки DELETE запроса
def send_delete():
    # Отправляем DELETE запрос к API
    response = requests.delete(f"http://127.0.0.1:5000/number/")
    # Если запрос успешен, возвращаем число и операцию
    if response.status_code == 200:
        result = response.json()
        return result['random_number'], result['operation']
    else:
        return None, None

# Функция для вычисления результата
def calculate(get_result, post_result, post_operation, delete_number, delete_operation):
    # Преобразуем все значения в числа
    get_result = float(get_result)
    post_result = float(post_result)
    delete_number = float(delete_number)

    # Выполняем первую операцию (между GET и POST результатами)
    if post_operation == '+':
        step1 = get_result + post_result
    elif post_operation == '-':
        step1 = get_result - post_result
    elif post_operation == '*':
        step1 = get_result * post_result
    elif post_operation == '/':
        step1 = get_result / post_result

    # Выполняем вторую операцию (между результатом step1 и DELETE числом)
    if delete_operation == '+':
        step2 = step1 + delete_number
    elif delete_operation == '-':
        step2 = step1 - delete_number
    elif delete_operation == '*':
        step2 = step1 * delete_number
    elif delete_operation == '/':
        step2 = step1 / delete_number

    # Возвращаем итоговый результат как целое число
    return int(step2)

# Роут для выполнения всех шагов
@lab3.route('/execute', methods=['GET'])
def execute():
    # Шаг 1: Отправляем GET запрос
    get_result = send_get()

    # Шаг 2: Отправляем POST запрос
    post_result, post_operation = send_post()

    # Шаг 3: Отправляем DELETE запрос
    delete_number, delete_operation = send_delete()

    # Если все шаги выполнены успешно
    if get_result is not None and post_result is not None and delete_number is not None:
        # Вычисляем итоговый результат
        final_result = calculate(get_result, post_result, post_operation, delete_number, delete_operation)
        # Возвращаем ответ в формате JSON
        return jsonify({
            "GET result": get_result,
            "POST result": post_result,
            "POST operation": post_operation,
            "DELETE result": delete_number,
            "DELETE operation": delete_operation,
            "Final result": final_result
        })
    else:
        # Если что-то пошло не так, возвращаем ошибку
        return jsonify({"error": "Что-то пошло не так при выполнении запросов."}), 400
    

# Раздел III. Отправка запросов на сервер с API (curl).
    
# for /f "tokens=*" %a in ('powershell -Command "Get-Random -Minimum 1 -Maximum 10"') do curl -X GET "http://127.0.0.1:5000/number/%a"

# for /f "tokens=*" %a in ('powershell -Command "Get-Random -Minimum 1 -Maximum 10"') do curl -X POST -H "Content-Type: application/json" -d "{\"jsonParam\": %a}" http://127.0.0.1:5000/number/

# curl -X DELETE "http://127.0.0.1:5000/number/"

# curl "http://127.0.0.1:5000/execute"