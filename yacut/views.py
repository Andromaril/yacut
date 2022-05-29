import random
import string
from datetime import datetime

from flask import flash, redirect, render_template, url_for

from . import app, db, lenght_short_id
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
        original_link = form.original_link.data
        custom_id = form.custom_id.data

        if custom_id and URL_map.query.filter_by(short=custom_id).first() is not None:
            message = (f'Имя {custom_id} уже занято!')
            flash(message)
            return redirect(url_for('index_view'))

        if not custom_id:
            custom_id = get_unique_short_id(lenght_short_id)
            if URL_map.query.filter_by(short=custom_id).first() is not None:
                message = (f'Имя {custom_id} уже занято, нажмите "создать" ещё раз.')
                flash(message)
                return redirect(url_for('index_view'))

        new_link = URL_map(
            original=original_link, short=custom_id, timestamp=datetime.now())
        db.session.add(new_link)
        db.session.commit()
        short_url = url_for('link_view', short=custom_id, _external=True)

        return render_template('link.html', short_url=short_url, form=form)

    return render_template('link.html', form=form)


@app.route('/<short>')
def link_view(short):
    link = URL_map.query.filter_by(short=short).first_or_404()
    return redirect(link.original)