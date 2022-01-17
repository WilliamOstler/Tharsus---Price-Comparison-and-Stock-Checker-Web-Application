from app import db


class Results(db.Model):

    __tablename__ = 'Results'

    source = db.Column(db.VARCHAR(8), primary_key=True)
    partnumber = db.Column(db.VARCHAR(100), primary_key=True)
    supplier = db.Column(db.VARCHAR(100), primary_key=True)
    stock = db.Column(db.Integer)
    stockrequired = db.Column(db.Integer)
    priceperunit = db.Column(db.Float)
    totalprice = db.Column(db.Float)
    link = db.Column(db.VARCHAR(500))
    searchnumber = db.Column(db.Integer, primary_key=True)

    def __init__(self, source, partnumber, supplier, stock, stockrequired, priceperunit, totalprice, link, searchnumber):
        self.source = source
        self.partnumber = partnumber
        self.supplier = supplier
        self.stock = stock
        self.stockrequired = stockrequired
        self.priceperunit = priceperunit
        self.totalprice = totalprice
        self.link = link
        self.searchnumber = searchnumber

    def __str__(self):
        return self.priceperunit