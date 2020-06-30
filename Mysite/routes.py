from Mysite import app
from markupsafe import escape

@app.route('/')
def index():
    return '<h1>Добро пожаловать на мой сайт!</h1><p>ты хто?</p><ul><li><a href="/hello/Маша">Маша</a></li><li><a href="/hello/Cаша">Cаша</a></li></ul>'

@app.route('/hello/<name>')
def hello(name):
    return '<h1>Привет, %s!</h1>' % escape(name)
