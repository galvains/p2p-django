from sqlalchemy import ForeignKey
from gino import Gino

db = Gino()


class TicketsTable(db.Model):
    __tablename__ = 'TicketsTable'

    id = db.Column(db.Integer, primary_key=True)
    nick_name = db.Column(db.String(50))
    price = db.Column(db.Float())
    orders = db.Column(db.String(7))
    available = db.Column(db.Float())
    max_limit = db.Column(db.Float())
    min_limit = db.Column(db.Float())
    rate = db.Column(db.String(8))
    pay_methods = db.Column(db.Text())
    currency = db.Column(db.String(5))
    coin = db.Column(db.String(5))
    trade_type = db.Column(db.Boolean())
    link = db.Column(db.Text())
    time_create = db.Column(db.DateTime())
    exchange = db.Column(db.Integer, ForeignKey('ExchangeTable.id'))

    # ip_address = db.Column(db.String(16))
    # country = db.Column(db.String(40))
    # cert = db.Column(db.String(80))
    # url = db.Column(db.String(80))
    # keys_available = db.Column(db.SmallInteger)
    # keys_max_allowed = db.Column(db.SmallInteger)

    # def __str__(self):
    #     return f"\n{self.ip_address} | {self.country} | {self.keys_max_allowed - self.keys_available}"
    #
    # def __repr__(self):
    #     return f"\n{self.ip_address} | {self.country} | {self.keys_max_allowed - self.keys_available}"


class ExchangeTable(db.Model):
    __tablename__ = 'ExchangeTable'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    # id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.BigInteger)
    # vpn_key = db.Column(db.String(110))
    # server_id = db.Column(db.Integer, ForeignKey('servers.id'))
    # closing_date = db.Column(db.DateTime)

    # def __str__(self):
    #     return f"\n{self.vpn_key} | {self.closing_date}"
    #
    # def __repr__(self):
    #     return f"\n{self.vpn_key} | {self.closing_date}"
