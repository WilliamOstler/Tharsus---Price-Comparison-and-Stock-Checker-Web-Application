from bs4 import BeautifulSoup
import requests
import re
def stringchecker(value):
    try:
        e = int(value)
        result = e
    except:
        result = 0
    return result


def findchipsscraper(partnumber, quantity_required):
    url_partnumber = partnumber.replace('/', '%2F').replace(',', '%2C')
    html_text = requests.get(f'https://www.findchips.com/search/{url_partnumber}').text
    soup = BeautifulSoup(html_text, 'lxml')
    distributors = soup.find_all('div', class_='distributor-results')

    for distributor in distributors:
        distributor_name = distributor.find('h3', class_='distributor-title').text.replace(' ', '').replace('\n', '')
        for listing in distributor.find_all('tr', class_='row'):
            stock = listing.find('td', class_='td-stock').text
            numeric_string = re.sub("[^0-9]", "", stock)

            if stringchecker(numeric_string) != 0 and stringchecker(numeric_string) >= quantity_required:
                price = listing.find('td', class_='td-price').text.replace('$', '').replace(
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
                                Distributor: {distributor_name}
                                Part number: {partnumber}
                                stock: {numeric_string}
                                price for quantity: {bomb}
                                ''')





if __name__ == '__main__':

    findchipsscraper('MPTC-02-80-02-6.30-01-L-V', 100)