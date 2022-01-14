from bs4 import BeautifulSoup
import requests
import re
from app import db

class Part(db.Model):
    __tablename__ = 'parts'

    part_id = db.Column(db.String(100), primary_key=True)
    part_number = db.Column(db.String(100))
    distributor_name = db.Column(db.String(100))
    stock = db.Column(db.Integer)
    prices = db.relationship('Price')


    def __init__(self, part_id, part_number, stock, distributor_name):
        self.part_id = part_id
        self.part_number = part_number
        self.distributor_name = distributor_name
        self.stock = stock


class Price(db.Model):
    __tablename__ ='prices'

    part_id = db.Column(db.String(100), db.ForeignKey(Part.part_id), primary_key=True)
    db.ForeignKey(Part.part_id)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __init__(self, part_id, quantity, price):
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

    for distributor in distributors:
        distributor_name = distributor.find('h3', class_='distributor-title').text.replace(' ', '').replace('\n', '')
        for listing in distributor.find_all('tr', class_='row'):
            stock = listing.find('td', class_='td-stock').text
            numeric_string = re.sub("[^0-9]", "", stock)

            if stringchecker(numeric_string) != 0:
                part_id = listing.find('td', class_='td-part first').text.replace(' ', '')
                price = listing.find('td', class_='td-price').text.replace('$', '').replace(
                    '£', '').replace('€', '').replace('See More', '')
                clean_price = ' '.join(price.split()).replace(' ', ',')
                if clean_price != '':
                    price_for_quantity = tuple(map(float, clean_price.split(',')))
                    if len(price_for_quantity) != 2:
                        res = tuple(price_for_quantity[n:n + 2] for n, i in enumerate(price_for_quantity)
                                    if n % 2 == 0)
                        quantity_ratio_to_price = res
                    else:
                        quantity_ratio_to_price = price_for_quantity

                    print(f'''
                                Distributor: {distributor_name}
                                Part number: {partnumber}
                                stock: {numeric_string}
                                Quantity required: {quantity_required}
                                price for quantity: {quantity_ratio_to_price}
                                ''')
                    part = Part(part_id, partnumber, numeric_string, distributor_name)
                    #price = Price(part_id, quantity_ratio_to_price[0], quantity_ratio_to_price[1])
                    db.session.add(part)
                    #db.session.add(price)
    db.session.commit()


if __name__ == '__main__':
    findchipsscraper('TLV3702IDGKR', 30)
