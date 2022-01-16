from bs4 import BeautifulSoup
import requests
import re
from app import db


class Part(db.Model):
    __tablename__ = 'parts'

    part_id = db.Column(db.String(100), primary_key=True)
    part_number = db.Column(db.String(100))
    description = db.Column(db.String(200), primary_key=True)
    distributor_name = db.Column(db.String(100), primary_key=True)
    stock = db.Column(db.Integer)
    prices = db.relationship('Price')

    def __init__(self, part_id, part_number, stock, distributor_name, description):
        self.part_id = part_id
        self.part_number = part_number
        self.description = description
        self.distributor_name = distributor_name
        self.stock = stock


class Price(db.Model):
    __tablename__ = 'prices'
    listing_id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.String(100), db.ForeignKey('parts.part_id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __init__(self, listing_id, part_id, quantity, price):
        self.listing_id = listing_id
        self.part_id = part_id
        self.quantity = quantity
        self.price = price


def stringchecker(value):
    try:
        e = int(value)
        result = e
    except:
        result = 0
    return result


def findchipsscraper(partnumber, quantity_required):
    db.drop_all()
    db.create_all()
    url_partnumber = partnumber.replace('/', '%2F').replace(',', '%2C')
    html_text = requests.get(f'https://www.findchips.com/search/{url_partnumber}?currency=GBP').text
    soup = BeautifulSoup(html_text, 'lxml')
    distributors = soup.find_all('div', class_='distributor-results')
    i = 0

    for distributor in distributors:
        distributor_name = distributor.find('h3', class_='distributor-title').text.replace(' ', '').replace('\n', '')
        for listing in distributor.find_all('tr', class_='row'):
            stock = listing.find('td', class_='td-stock').text
            numeric_string = re.sub("[^0-9]", "", stock)

            if stringchecker(numeric_string) != 0:
                part_id = listing.find('td', class_='td-part first').text.replace(' ', '').replace('\n', '')
                description = listing.find('td', class_='td-desc more').text.replace('\n', '').replace('  ', '')
                part = Part(part_id, partnumber, numeric_string, distributor_name, description)
                db.session.add(part)
                for x, price in enumerate(listing.find_all('ul', class_='price-list')):
                    quantity = price.find('span', class_='label').text.replace(' ', '')
                    value = price.find('span', class_='value').text.replace('£', '').replace(' ', '')
                    price_per_quantity = Price(i ,part_id, quantity, value)
                    db.session.add(price_per_quantity)
                    i = i+1

                    print(f'''
                                Distributor: {distributor_name}
                                Part number: {part_id}
                                stock: {numeric_string}
                                Quantity required: {quantity_required}
                                price for quantity: {price_per_quantity}
                                ''')

    db.session.commit()


if __name__ == '__main__':
    findchipsscraper('MPTC-02-80-02-6.30-01-L-V', 30)
