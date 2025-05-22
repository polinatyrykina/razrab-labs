from flask import Flask, request, jsonify

app = Flask(__name__)

# Статические курсы валют
CURRENCY_RATES = {
    "USD": 78.00,
    "EUR": 90.00
}

@app.route('/rate')
def get_rate():
    currency = request.args.get('currency', '').upper()
    
    if currency not in CURRENCY_RATES:
        return jsonify({"message": "UNKNOWN CURRENCY"}), 400
    
    try:
        return jsonify({"rate": CURRENCY_RATES[currency]}), 200
    except Exception as e:
        print(f"Ошибка сервера: {e}")
        return jsonify({"message": "UNEXPECTED ERROR"}), 500


if __name__ == '__main__':
    app.run(port=5000)