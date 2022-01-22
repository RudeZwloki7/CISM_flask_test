from blog import app
from blog import db
from flask import render_template, redirect, url_for, flash, request
from blog.forms import RegisterForm, LoginForm, PostForm
from blog.models import BlogUser, Post
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/info')
def info_page():
    return render_template('info.html')


@app.route('/feed', methods=['GET', 'POST'])
def feed_page():
    form = PostForm()
    presented_posts = Post.query.filter_by(is_presented=True).order_by(Post.post_date.desc()).all()
    if form.validate_on_submit():
        post = Post(content=form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Пост успешно опубликован!', 'success')
        return redirect(url_for('feed_page'))

    return render_template('feed.html', form=form,
                           posts=presented_posts)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = BlogUser(login=form.login.data,
                            password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f'Регистрация прошла успешно! Добро пожаловать, {new_user.login}', category='success')
        return redirect(url_for('feed_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Во время регистрации нового пользователя произошла ошибка:{err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = BlogUser.query.filter_by(login=form.login.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Вы успешно авторизованы как {attempted_user.login}', category='success')
            return redirect(url_for('feed_page'))
        else:
            flash('Неверный логин или пароль. Попробуйте еще раз.', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('Вы успешно вышли из аккаунта!', category='info')
    return redirect(url_for('feed_page'))


@app.route('/archive/<post_id>')
def archive_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.soft_delete()
    flash('Выбранный пост успешно архивирован.', category='success')
    return redirect(url_for('feed_page'))


@app.route('/recover/<post_id>')
def recover_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.recover()
    flash('Выбранный пост успешно восстановлен.', category='success')
    return redirect(url_for('archive_page'))


@app.route('/delete/<post_id>')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Выбранный пост успешно удален.', category='success')
    except:
        flash('При удалении поста возникла ошибка, попробуйте снова.', 'danger')
    return redirect(url_for('archive_page'))


@app.route('/archive')
@login_required
def archive_page():

    archived_posts = Post.query.filter_by(is_presented=False, author_id=current_user.id).order_by(
        Post.post_date.desc()).all()

    return render_template('archive.html', posts=archived_posts)
