import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db, lenght_short_id
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_link():

    regex = "^[a-zA-Z0-9]{1,16}$"
    pattern = re.compile(regex)

    if request.json is None:
        raise InvalidAPIUsage('Отсутствует тело запроса', HTTPStatus.BAD_REQUEST)
    data = request.get_json()

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', HTTPStatus.BAD_REQUEST)

    elif 'custom_id' in data:
        if data['custom_id']:
            if pattern.search(data['custom_id']) is None:
                raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', HTTPStatus.BAD_REQUEST)
            if URL_map.query.filter_by(short=data['custom_id']).first() is not None:
                name = data['custom_id']
                raise InvalidAPIUsage(f'Имя "{name}" уже занято.', HTTPStatus.BAD_REQUEST)
        else:
            data['custom_id'] = get_unique_short_id(lenght_short_id)
    else:
        data['custom_id'] = get_unique_short_id(lenght_short_id)

    link = URL_map(original=data['url'], short=data['custom_id'])
    db.session.add(link)
    db.session.commit()
    return jsonify(link.to_dict_post()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_opinion(short_id):

    link = URL_map.query.filter_by(short=short_id).first()
    if link is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)

    return jsonify(link.to_dict_original()), HTTPStatus.OK
