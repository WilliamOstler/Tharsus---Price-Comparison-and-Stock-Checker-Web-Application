from bs4 import BeautifulSoup
import requests
import re
from app import db


class Part(db.Model):
    __tablename__ = 'parts'

    part_id = db.Column(db.String(100), primary_key=True)
    part_source = db.Column(db.String(100))
    part_number = db.Column(db.String(100))
    description = db.Column(db.String(200), primary_key=True)
    distributor_name = db.Column(db.String(100), primary_key=True)
    stock = db.Column(db.Integer)
    link= db.Column(db.String(200))
    prices = db.relationship('Price')

    def __init__(self, part_id, part_source, part_number, stock, distributor_name, description, link):
        self.part_id = part_id
        self.part_source = part_source
        self.part_number = part_number
        self.description = description
        self.distributor_name = distributor_name
        self.stock = stock
        self.link = link


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

    def __str__(self):
        return self.quantity



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
    for script in soup.find_all('a', href='javascript:void(0)'):
        script.decompose()
    html = soup.findAll(lambda tag: not tag.contents)
    [tag.extract() for tag in html]
    distributors = soup.find_all('div', class_='distributor-results')
    part_source = 'Findchips'
    i = 0

    for distributor in distributors:
        distributor_name = distributor.find('h3', class_='distributor-title').text.replace(' ', '').replace('\n', '')
        for listing in distributor.find_all('tr', class_='row'):
            stock = listing.find('td', class_='td-stock').text
            numeric_string = re.sub("[^0-9]", "", stock)

            if stringchecker(numeric_string) != 0 and stringchecker(numeric_string) >= quantity_required:
                part_id = listing.find('td', class_='td-part first').text.replace(' ', '').replace('\n', '')
                description = listing.find('td', class_='td-desc more').text.replace('\n', '').replace('  ', '')
                link = listing.td.div.a['href']
                part = Part(part_id, part_source, partnumber, numeric_string, distributor_name, description, link)
                db.session.add(part)
                for price in listing.find_all('li'):
                    quantity = price.find('span', class_='label').text
                    value = price.find('span', class_='value').text
                    if int(quantity) <= quantity_required:
                        price_per_quantity = Price(i, part_id, quantity, value)
                        db.session.add(price_per_quantity)
                        i = i+1
                        print(f'''
                                Distributor: {distributor_name}
                                Part number: {part_id}
                                stock: {numeric_string}
                                Quantity required: {quantity_required}
                                price for quantity: {price_per_quantity}
                                link: {link}
                                ''')
    db.session.commit()


if __name__ == '__main__':
    findchipsscraper('ICF-308-T-O-TR', 500)
