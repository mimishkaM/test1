from Mysite import app


@app.route('/')
@app.route('/main')
def index():
    return '<h1>Добро пожаловать на мой сайт!</h1>'