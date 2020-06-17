from flask_wtf import FlaskForm
from wtforms import (BooleanField, FieldList, FormField, HiddenField,
                     IntegerField, PasswordField, StringField, SubmitField)
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Пользователь', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить?')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Пользователь', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другое имя.')


class ItemForm(FlaskForm):
    name = StringField(label='Предмет')
    quantity = IntegerField(label='Количество')
    class Meta:
        csrf = False


class ListForm(FlaskForm):
    id = HiddenField()
    name = StringField(label='Название списка')
    items = FieldList(FormField(ItemForm), label='Предмет')
    add_item = SubmitField(label='Добавить предмет')
    remove_item=SubmitField(label='Удалить предмет')

    submit = SubmitField(label='Сохранить')
