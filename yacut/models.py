from datetime import datetime

from . import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(6), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            id = self.id,
            original = self.original,
            short = self.short,
            timestamp = self.timestamp,
        )
    
    def to_dict_original(self):
        return dict(
            url = self.original,
        )

    def to_dict_post(self):
        return dict(
            url = self.original,
            short_link = 'http://localhost/' + self.short,
        )

    def from_dict(self, data):
        for field in ['original', 'short',]:
            if field in data:
                setattr(self, field, data[field])

class URL_map_api(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url= db.Column(db.String(256), nullable=False)
    custom_id = db.Column(db.String(6), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


    def to_dict_post(self):
        return dict(  
            url = self.url,
            short_link = 'http://localhost/' + self.custom_id
        )
    
    def to_dict_original(self):
        return dict(
            url = self.url,
        )
    
    def from_dict(self, data):
        for field in ['url', 'custom_id',]:
            if field in data:
                setattr(self, field, data[field])

    