from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .views import get_unique_short_id



@app.route('/api/id/', methods=['POST'])
def add_link():
    
    data = request.get_json()

    if 'short' in data:
        if data['short'] is not None:
            if URL_map.query.filter_by(short=data['short']).first() is not None:
                l = URL_map.query.filter_by(short=data['short']).first().short
                message = (f'Имя {l} уже занято.')
                raise InvalidAPIUsage(message)
        data['short'] = get_unique_short_id(6)
    else:
        data['short'] = get_unique_short_id(6)
    
    #if 'short' not in data:
        #data['short'] = get_unique_short_id(6)
    
    #if URL_map.query.filter_by(short=data['short']).first() is not None:
            #l = URL_map.query.filter_by(short=data['short']).first().short
            #message = (f'Имя {l} уже занято.')
            #raise InvalidAPIUsage(message)
    #else:
    #if 'short' not in data:
        #data['short'] = get_unique_short_id(6)
    
    
    #if 'short' not in data:
        #raise InvalidAPIUsage('"url" является обязательным полем!')

    if 'original' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    
    #if data['short'] is not None:
        #if len(data['short']) > 16:
            #raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    
    link = URL_map()
    link.from_dict(data)
    db.session.add(link)
    db.session.commit()
    return jsonify(link.to_dict_post()), 201

@app.route('/api/id/<short_id>/', methods=['GET'])
def get_opinion(short_id):
    
    #link1 = URL_map.query.get(id)
    link = URL_map.query.filter_by(short=short_id).first()

    #if link1 is None:
        #raise InvalidAPIUsage('Указанный id не найден', 404)
    if link is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)

    return jsonify(link.to_dict_original()), 200
