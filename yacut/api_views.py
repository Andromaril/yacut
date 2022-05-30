import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db, lenght_short_id
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .views import get_unique_short_id


def random(custom_id):
    if URL_map.query.filter_by(short=custom_id).first() is not None:
        message = (f'Имя {custom_id} уже занято, отправьте запрос ещё раз.')
        raise InvalidAPIUsage(message, HTTPStatus.BAD_REQUEST)


@app.route('/api/id/', methods=['POST'])
def add_link():

    if request.json is None:
        raise InvalidAPIUsage('Отсутствует тело запроса', HTTPStatus.BAD_REQUEST)
    data = request.get_json()

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', HTTPStatus.BAD_REQUEST)

    regex = "^[a-zA-Z0-9]{1,16}$"
    pattern = re.compile(regex)
    if data['custom_id']:
        if pattern.search(data['custom_id']) is None:
        #regex = "^[a-zA-Z0-9]{1,16}$"
        #string = data['custom_id']
        #pattern = re.compile(regex)
        #if (pattern.search(string) is None):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', HTTPStatus.BAD_REQUEST)
        if URL_map.query.filter_by(short=data['custom_id']).first() is not None:
            name = data['custom_id']
            raise InvalidAPIUsage(f'Имя "{name}" уже занято.', HTTPStatus.BAD_REQUEST)
    elif not data['custom_id']:
        data['custom_id'] = get_unique_short_id(lenght_short_id)
        #link = URL_map(original=data['url'], short=data['custom_id'])

    

    #try:
        #data = request.get_json()
        #if data:
            #data['url']
    #except Exception:
        #raise InvalidAPIUsage('"url" является обязательным полем!', HTTPStatus.BAD_REQUEST)

    #try:
        #data = request.get_json()
        #data['url']
    #except Exception:
        #raise InvalidAPIUsage('Отсутствует тело запроса', HTTPStatus.BAD_REQUEST)

    #if 'custom_id' not in data:
        #data['custom_id'] = get_unique_short_id(lenght_short_id)
        #random(data['custom_id'])

    #elif not data['custom_id']:
        #data['custom_id'] = get_unique_short_id(lenght_short_id)
        #random(data['custom_id'])
    #else:
        #regex = "^[a-zA-Z0-9]{1,16}$"
        #string = data['custom_id']
        #pattern = re.compile(regex)
        #if (pattern.search(string) is None):
            #raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', HTTPStatus.BAD_REQUEST)

    #if URL_map.query.filter_by(short=data['custom_id']).first() is not None:
        #name = data['custom_id']
        #raise InvalidAPIUsage(f'Имя "{name}" уже занято.', HTTPStatus.BAD_REQUEST)

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
