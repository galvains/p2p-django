from gino import Gino
from datetime import datetime
from sqlalchemy import ForeignKey

db = Gino()


class TicketsTable(db.Model):
    __tablename__ = 'app_ticketstable'

    id = db.Column(db.Integer, primary_key=True)
    nick_name = db.Column(db.String(50))
    price = db.Column(db.Float())
    orders = db.Column(db.Integer())
    available = db.Column(db.Float())
    max_limit = db.Column(db.Float())
    min_limit = db.Column(db.Float())
    rate = db.Column(db.Float())
    pay_methods = db.Column(db.Text())
    currency = db.Column(db.String(5))
    coin = db.Column(db.String(5))
    trade_type = db.Column(db.Boolean())
    link = db.Column(db.Text())
    time_create = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    exchange_id = db.Column(db.Integer, ForeignKey('app_exchangetable.id'))


class ExchangeTable(db.Model):
    __tablename__ = 'app_exchangetable'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
