from datetime import datetime

from flask import url_for

from . import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(6), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp,
        )

    def to_dict_original(self):
        return dict(
            url=self.original,
        )

    def to_dict_post(self):
        return dict(
            url=self.original,
            short_link=url_for('link_view', short=self.short, _external=True)
        )
