from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map, URL_map_api
from .views import get_unique_short_id

my_set = set()



@app.route('/api/id/', methods=['POST'])
def add_link():
    
    data = request.get_json()
    
    if 'custom_id' in data:
        allowed_chars = set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') 
        validationString = data['custom_id'] 
        if set(validationString).issubset(allowed_chars) == False:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', 400)
    
    if 'url' not in data:
        raise InvalidAPIUsage('В запросе отсутствуют обязательные поля', 400)
    
    if 'custom_id' not in data:
        data['custom_id'] = get_unique_short_id(6)

    if data['custom_id'] is None:
        data['custom_id'] = get_unique_short_id(6)

    if URL_map_api.query.filter_by(custom_id=data['custom_id']).first() is not None:
        raise InvalidAPIUsage('В запросе отсутствуют обязательные поля', 400)

    if len(data['custom_id']) > 16:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', 400)

    link = URL_map_api()
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
