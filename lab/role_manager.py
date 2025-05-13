from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        dbname="razrab-labs_1",
        user="polina_tyrykina_knowledge_base",
        password="123",
        host="localhost",
        port="5432",
        client_encoding="utf8"
    )

conn = get_db_connection()
cur = conn.cursor()


@app.route('/is_admin', methods=['GET'])
def is_admin():
    chat_id = request.args.get('chat_id')
    if not chat_id:
        return jsonify({"error": "chat_id parameter is required"}), 400

    try:
        cur.execute("SELECT 1 FROM admins WHERE chat_id = %s", (chat_id,))
        is_admin = cur.fetchone() is not None
        return jsonify({"is_admin": is_admin}), 200
    except:
        return jsonify({"error": "Internal server error"}), 500
    

@app.route('/admins', methods=['GET'])
def get_admins():
    try:
        cur.execute("SELECT chat_id FROM admins")
        admins = [row[0] for row in cur.fetchall()]
        return jsonify({"admins": admins}), 200
    except:
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(port=5003)
    cur.close()
    conn.close()

