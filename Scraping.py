from bs4 import BeautifulSoup
import requests
import re


def findchipsscraper(partnumber):
    html_text = requests.get(f'https://www.findchips.com/search/{partnumber}').text
    soup = BeautifulSoup(html_text, 'lxml')
    parts = soup.find_all('div', class_='distributor-results')

    for part in parts:
        stock = part.find('td', class_='td-stock').text
        numeric_string = re.sub("[^0-9]", "", stock)
        if int(numeric_string) != 0:
            distributor = part.find('h3', class_='distributor-title').text.replace(' ', '').replace('\n', '')
            price = part.find('td', class_='td-price').text.replace('$', '').replace(
                '£', '').replace('€', '').replace('See More', '')
            clean_price = ' '.join(price.split()).replace(' ', ',')
            if clean_price != '':
                price_for_quantity = tuple(map(float, clean_price.split(',')))
                if len(price_for_quantity) != 2:
                    res = tuple(price_for_quantity[n:n + 2] for n, i in enumerate(price_for_quantity)
                                if n % 2 == 0)
                    bomb = res
                else:
                    bomb = price_for_quantity

                print(f'''
                    Distributor: {distributor}
                    stock: {numeric_string}
                    price for quantity: {bomb}
                    ''')


if __name__ == '__main__':

    findchipsscraper('ICF-308-T-O-TR')