from flask import render_template, flash, redirect, url_for, request
from mysite import app, db
from mysite.forms import LoginForm, RegistrationForm, AccountUpdateForm, FeedbackForm
from flask_login import current_user, login_user, logout_user, login_required
from mysite.models import User, Zvonok
import secrets
import os
from PIL import Image


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = FeedbackForm()
    if form.validate_on_submit():
        zvonok = Zvonok(body=form.body.data, phone=form.phone.data, user_username=current_user.username)
        db.session.add(zvonok)
        db.session.commit()

        flash('Обращение отправлена', 'success')
        return redirect('index')

    return render_template('index.html', title='Главная', form=form)


@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Контакты')


@app.route('/about')
def about_us():
    return render_template('about.html', title='О нас')


@app.route('/sign_in', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()

        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя пользователя и/или пароль', 'danger')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('login.html', title='Вход', form=form)


@app.route('/sign_out')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/sign_up', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Вы успешно зарегестрировались!', 'success')
        login_user(user)
        return redirect(url_for('index'))


    return render_template('register.html', title='Регистрация', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, p_ext = os.path.splitext(form_picture.filename)
    p_filename = random_hex + p_ext

    picture_path = os.path.join(app.root_path, 'static/img/avatar', p_filename)

    resize = (125,125)
    image = Image.open(form_picture)
    image.thumbnail(resize)
    image.save(picture_path)

    return p_filename




@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()
    avatar = url_for('static', filename='img/avatar/' + current_user.avatar)

    feedback = Zvonok.query.all()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.avatar = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Информация обновлена!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('account.html', title='Личный кабинет', avatar=avatar, form=form, feedback=feedback)
