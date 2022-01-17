from bs4 import BeautifulSoup
import requests
import re
from models import Results



def stringchecker(value):
    try:
        e = int(value)
        result = e
    except:
        result = 0
    return result


results = []


def findchipsscraper(partnumber, quantity_required):
    url_partnumber = partnumber.replace('/', '%2F').replace(',', '%2C')
    html_text = requests.get(f'https://www.findchips.com/search/{url_partnumber}?currency=GBP').text
    soup = BeautifulSoup(html_text, 'lxml')
    for script in soup.find_all('a', href='javascript:void(0)'):
        script.decompose()
    html = soup.findAll(lambda tag: not tag.contents)
    [tag.extract() for tag in html]
    distributors = soup.find_all('div', class_='distributor-results')
    part_source = 'Findchips'

    for distributor in distributors:
        distributor_name = distributor.find('h3', class_='distributor-title').text.replace(' ', '').replace('\n', '')
        for listing in distributor.find_all('tr', class_='row'):
            stock = listing.find('td', class_='td-stock').text
            numeric_string = re.sub("[^0-9]", "", stock)

            if stringchecker(numeric_string) != 0 and stringchecker(numeric_string) >= quantity_required:
                part_id = listing.find('td', class_='td-part first').text.replace(' ', '').replace('\n', '')
                link = listing.td.div.a['href']
                for price in listing.find_all('li'):
                    quantity = price.find('span', class_='label').text
                    value = price.find('span', class_='value').text.replace('£','')
                    if int(quantity) <= quantity_required:
                        result = Results(part_source, partnumber, distributor_name, numeric_string, quantity_required, value, float(value)*quantity_required,link, '1' )
                        results.append(result)

    return results


if __name__ == '__main__':
    print(findchipsscraper('ICF-308-T-O-TR', 500))
