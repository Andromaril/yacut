import random
import string
from random import randrange
from datetime import datetime

from flask import abort, flash, redirect, render_template, url_for, request

from . import app, db
from .forms import URLForm
from .models import URL_map


def get_unique_short_id(number):
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, number))
    return rand_string

@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
    #if request.method == 'POST':
        original_link = form.original_link.data
        custom_id = form.custom_id.data

        if custom_id and URL_map.query.filter_by(short=custom_id).first() is not None:
            l = URL_map.query.filter_by(short=custom_id).first().short
            message = (f'Имя {l} уже занято!')
            flash(message)
            return redirect(url_for('index_view'))


        if not custom_id:
            custom_id = get_unique_short_id(6)

        new_link = URL_map(
            original=original_link, short=custom_id, timestamp=datetime.now())
        db.session.add(new_link)
        db.session.commit()
        short_url = request.host_url + custom_id

        return render_template('link.html', short_url=short_url, form = form)

    return render_template('link.html', form = form)



@app.route('/<short>')
def link_view(short):
    link = URL_map.query.filter_by(short=short).first()
    if link:
        return redirect(link.original)
    else:
        flash('Нерабочая ссылка!')
        return redirect(url_for('index_view'))