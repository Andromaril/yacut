from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, ValidationError


def my_length_check(form, field):

    allowed_chars = set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    if field.data is not None:
        if set(field.data).issubset(allowed_chars) is False:
            raise ValidationError('Указано недопустимое имя для короткой ссылки')


class URLForm(FlaskForm):
    original_link = StringField(
        'Введите оригинальную длинную ссылку',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(0, 16, message='Число символов не должно превышать 16!'), my_length_check],
    )
