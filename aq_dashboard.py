"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq

def add_values():
    '''function to add date and values to display'''
    api = openaq.OpenAQ()

    status, body = api.measurements(city='Los Angeles', parameter='pm25')

    values = []

    for result in body['results']:
       data = list(result.items())
       date = list(data[2])
       utc = date[1]
       utc = list(utc.items())
       utc = utc[0]
       utc = utc[1]
       utc = str(utc)
       value = data[3]
       value = value[1]
       value = str(value)
       final = f'({utc}, {value})'.format(utc, value)
       values.append(final)

    return values

values =add_values()

APP = Flask(__name__)


@APP.route('/')
def root():
    """Base view."""
    danger = Record.query.filter(Record.value >= 10 ).all()
    return str(danger)

from flask_sqlalchemy import SQLAlchemy

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'DateTime:{self.datetime}, Value:{self.value}   \n'


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    for result in body['results']:
       data = list(result.items())
       date = list(data[2])
       utc = date[1]
       utc = list(utc.items())
       utc = utc[0]
       utc = utc[1]
       utc = str(utc)
       value = data[3]
       value = value[1]
       db_records = Record(datetime=utc, value=value)
       DB.session.add(db_records)  
    DB.session.commit()
    return 'Data refreshed!'
