from flask import Flask, url_for

from lab3 import lab3

app = Flask(__name__)

app.register_blueprint(lab3)

@app.route("/")
@app.route("/index")
def labs():
    return '''<!DOCTYPE html>
<body >
    <header>
        НГТУ, ФБ, Разработка программных приложений. Список лабораторных
    </header>
    <main>
        <h1>Лабораторные работы по Разработке программных приложений</h1>
        <div>
        <a href="/number/">Лабораторная работа 3</a><br>
        </div>
    </main>
</body>
</html>
'''