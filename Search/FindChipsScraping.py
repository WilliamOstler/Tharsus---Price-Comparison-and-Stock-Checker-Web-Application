from bs4 import BeautifulSoup
import requests
import re
from Search import DatabaseProcess



def stringchecker(value):
    try:
        e = int(value)
        result = e
    except:
        result = 0
    return result


def findchipsscraper(partnumber, quantity_required, searchID):
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
        distributor_name = distributor.find('h3', class_='distributor-title').text.replace(' ', '').replace('\n', '').\
            replace(
            '\xC2','').replace('\x95', '').replace('ECIA(NEDA)MemberAuthorizedDistributor','').\
          replace('AuthorizedDistributor','').replace('Manufacturer Direct – Inventory Available for Immediate and Future Delivery','')

        for listing in distributor.find_all('tr', class_='row'):
            stock = listing.find('td', class_='td-stock').text
            numeric_string = re.sub("[^0-9]", "", stock)

            if stringchecker(numeric_string) != 0 and stringchecker(numeric_string) >= quantity_required:
                part_id = listing.find('td', class_='td-part first').text.replace(' ', '').replace('\n', '')
                link = f"https:{listing.td.div.a['href']}"
                for price in listing.find_all('li'):
                    quantity = price.find('span', class_='label').text
                    value = price.find('span', class_='value').text.replace('£','')
                    if int(quantity) <= quantity_required:
                        result = [part_source, partnumber, part_id, distributor_name, numeric_string, quantity_required,
                                         float(value), float(value)*quantity_required,link, searchID]
                        DatabaseProcess.addRow(result)