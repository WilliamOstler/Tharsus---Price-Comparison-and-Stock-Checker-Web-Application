from app import db

class User(db.Model):

    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.VARCHAR(100))
    password = db.Column(db.VARCHAR(100))
    firstname = db.Column(db.VARCHAR(100))
    surname = db.Column(db.VARCHAR(100))
    admin = db.Column(db.Boolean)

    def __init__(self, id, email, password, firstname, surname, admin):
        self.id = id
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

    partnumber = db.Column(db.VARCHAR(100), primary_key=True)
    supplier = db.ForeignKey('Supplier.name00')
    stock = db.Column(db.Integer)
    stockrequired = db.Column(db.Integer)
    priceperunit = db.Column(db.DECIMAL)
    totalprice = db.Column(db.DECIMAL)
    link = db.Column(db.VARCHAR(500))
    searchnumber = db.Column(db.Integer)

    def __init__(self, partnumber, supplier, stock, stockrequired, priceperunit, totalprice, link):
        self.partnumber = partnumber
        self.supplier = supplier
        self.stock = stock
        self.stockrequired = stockrequired
        self.priceperunit = priceperunit
        self.totalprice = totalprice
        self.link = link


