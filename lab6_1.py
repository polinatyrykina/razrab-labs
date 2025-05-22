
from flask import Blueprint, request, jsonify
lab6_1 = Blueprint('lab6_1', __name__)


@lab6_1.route('/check_all/', methods=['POST'])
def check_all():
    data = request.get_json()
    
    # Извлекаем слова из JSON
    word1 = data.get('word1')
    word2 = data.get('word2')
    word3 = data.get('word3')
    
    # Проверяем, что все слова переданы
    if None in [word1, word2, word3]:
        return jsonify({'error': 'Не переданы все три слова'}), 400
    
    # Проверяем, совпадают ли все три слова
    result = word1 == word2 == word3
    
    return jsonify({'result': result})


@lab6_1.route('/check_length/', methods=['POST'])
def check_length():
    data = request.get_json()
    
    word1 = data.get('word1')
    word2 = data.get('word2')
    word3 = data.get('word3')

    if None in [word1, word2, word3]:
        return jsonify({'error': 'Не переданы все три слова'}), 400
    
    # Считаем количество слов длиннее 3  - считаем сумму - каждому слову присваеваем 1 если его длина больше чем 3 символа
    count = sum(1 for word in [word1, word2, word3] if len(word) > 3)
    
    result = count >= 2
    
    return jsonify({'result': result})