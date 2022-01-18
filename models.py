from app import db


class User(db.Model):

    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.VARCHAR(100))
    password = db.Column(db.VARCHAR(100))
    firstname = db.Column(db.VARCHAR(100))
    surname = db.Column(db.VARCHAR(100))
    admin = db.Column(db.Boolean)

    def __init__(self, email, password, firstname, surname, admin):
        self.email = email
        self.password = password
        self.firstname = firstname
        self.surname = surname
        self.admin = admin


class Supplier(db.Model):

    __tablename__ = 'Supplier'
    name = db.Column(db.VARCHAR(100), primary_key=True)
    blacklisted = db.Column(db.Boolean)
    favourited = db.Column(db.Boolean)

    def __init__(self, name, blacklisted, favourited):
        self.name = name
        self.blacklisted = blacklisted
        self.favourited = favourited


class Results(db.Model):

    __tablename__ = 'Results'

    source = db.Column(db.VARCHAR(10), primary_key=True)
    partnumber = db.Column(db.VARCHAR(100), primary_key=True)
    alternate_partnumber = db.Column(db.VARCHAR(100), primary_key=True)
    supplier = db.Column(db.VARCHAR(100), primary_key=True)
    stock = db.Column(db.Integer)
    stockrequired = db.Column(db.Integer)
    priceperunit = db.Column(db.Float, primary_key=True)
    totalprice = db.Column(db.Float)
    link = db.Column(db.VARCHAR(2000))
    searchnumber = db.Column(db.Integer, primary_key=True)

    def __init__(self, source, partnumber, alternate_partnumber, supplier, stock, stockrequired, priceperunit, totalprice, link, searchnumber):
        self.source = source
        self.partnumber = partnumber
        self.alternate_partnumber = alternate_partnumber
        self.supplier = supplier
        self.stock = stock
        self.stockrequired = stockrequired
        self.priceperunit = priceperunit
        self.totalprice = totalprice
        self.link = link
        self.searchnumber = searchnumber
db.create_all()
