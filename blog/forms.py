from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, Length, EqualTo, DataRequired

from blog.models import BlogUser


class RegisterForm(FlaskForm):
    def validate_login(self, login_to_check):
        blog_user = BlogUser.query.filter_by(login=login_to_check.data).first()
        if blog_user:
            raise ValidationError('Пользователь с введеным логином уже существует!')

    login = StringField(label='Введите логин:', validators=[Length(min=7), DataRequired()])
    password = PasswordField(label='Введите пароль:', validators=[Length(min=8), DataRequired()])
    password_confirm = PasswordField(label='Повторно введите пароль:', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Создать аккаунт')


class LoginForm(FlaskForm):
    login = StringField(label='Логин:', validators=[DataRequired()])
    password = PasswordField(label='Пароль:', validators=[DataRequired()])
    submit = SubmitField(label='Войти')


class PostForm(FlaskForm):
    content = TextAreaField(label='Что у Вас нового?', validators=[DataRequired()], )
    submit = SubmitField(label='Опубликовать')
