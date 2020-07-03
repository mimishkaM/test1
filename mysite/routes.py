from flask import render_template, flash, redirect
from mysite import app
from mysite.forms import LoginForm



@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html', title='Главная')


@app.route('/documentation')
def documentation():
  return render_template('documentation.html', title='Документация')

@app.route('/about')
def about_us():
  return render_template('about.html', title='О нас')


@app.route('/sign_in', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    flash(f'Пользователь {form.username.data}, поле "запомнить": {form.remember_me.data}', 'info')
    return redirect('/index')
  return render_template('login.html', title='Вход', form=form)

@app.route('/help')
def help():
  return render_template('help.html', title='Помощь')

@app.route('/achievements')
def achievements():
  return render_template('achievements.html', title='Наши достижения')

@app.route('/blog')
def blog():
  return render_template('blog.html', title='Блог')



