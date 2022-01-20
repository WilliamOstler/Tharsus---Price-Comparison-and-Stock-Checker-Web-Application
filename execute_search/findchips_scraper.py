"""
Containns the Web Scraper for scraping listings from FindChips.com
"""
import re
from bs4 import BeautifulSoup
import requests
from execute_search import database_process


def string_checker(value):
    """
    This method checks if a string could be converted to an int, if it cannot
    then it is converted to a 0.
    :param value: any string value
    :returns integer
    :author Nojus Ivanauskas

    """
    try:
        test = int(value)
        result = test
    except ValueError:
        result = 0
    return result


def findchipsscraper(partnumber, quantity_required, search_id):
    """
    This method adds arrays of results to the database after scraping the findchips website
    :param partnumber: the number of the part that is needed to be scraped
    :param quantity_required: how many parts are needed
    :param search_id: the id which was calculated for this search

    @author Nojus Ivanauskas

    """
    url_partnumber = partnumber.replace('/', '%2F').replace(',', '%2C')
    html_text = requests.get(f'https://www.findchips.com/search/{url_partnumber}?currency=GBP').text
    soup = BeautifulSoup(html_text, 'lxml')
    for script in soup.find_all('a', href='javascript:void(0)'):
        script.decompose()  # loop gets rid of all javascript in the html
    html = soup.findAll(lambda tag: not tag.contents)
    [tag.extract() for tag in html]  # removes all empty html tags
    distributors = soup.find_all('div', class_='distributor-results')
    part_source = 'Findchips'

    for distributor in distributors:
        distributor_name = distributor.find('h3', class_='distributor-title').\
            text.replace(' ', '').replace('\n', '').\
            replace(
            '\xC2', '').replace('\x95', '').replace('ECIA(NEDA)MemberAuthorizedDistributor', '').\
            replace('AuthorizedDistributor', '').\
            replace('Manufacturer Direct – Inventory Available for Immediate and Future Delivery',
                    '').replace(
            "ECIA(NEDA)", ''
        )
        for listing in distributor.find_all('tr', class_='row'):
            # removes all non-numeric characters from a string
            stock = listing.find('td', class_='td-stock').text
            numeric_string = re.sub("[^0-9]", "", stock)

            if string_checker(numeric_string) != 0 and string_checker(numeric_string) >= \
                    quantity_required:
                part_id = listing.find('td', class_='td-part first').text.replace(' ', '')\
                    .replace('\n', '')
                link = f"https:{listing.td.div.a['href']}"
                for price in listing.find_all('li'):
                    quantity = price.find('span', class_='label').text
                    value = price.find('span', class_='value').text.replace('£', '')
                    if int(quantity) <= quantity_required:
                        result = [part_source, partnumber, part_id, distributor_name,
                                  numeric_string, quantity_required, float(value),
                                  float(value) * quantity_required, link, search_id]
                        database_process.add_row(result)
