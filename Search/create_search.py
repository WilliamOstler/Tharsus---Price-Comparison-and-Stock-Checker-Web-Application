"""
Main search file. Contains the main method which will call all required methods in order for
a complete part such to be carried out.
"""
from Search import excel_process
from Search import database_process
from sqlalchemy import func
from Search.findchips_scraper import findchipsscraper
from Search.search_octopart import SearchOctopart
from models import Results
from app import db


def get_search_id():
    """
    This method calculates the current search id to be used. This enables searches to executed
     simultaneously across multiple systems with no interference from each other.
    :return: The search id to be used for the search.
    """
    # If the Results table has no current entries. i.e., there are no searches currently being
    # executed
    if db.session.query(Results).count() == 0:
        search_id = 1
    # There are entries inside the Results table. i.e., there are currently searches being executed
    # by other users.
    else:
        # Add one to the current largest search id.
        search_id = int(db.session.query(func.max(Results.searchnumber)).scalar()) + 1
    return search_id


def search(data, quantity, search_id):
    """
    The main method, which is called when a search is created. It calls all methods relating to
    searching in the correct order, resulting in a successful search process.
    :param data: Contents of the BOM spreadsheet, formatted within an array of arrays format ([[]])
    :param quantity: The BOM quantity field.
    :param search_id: The search id, calculated for this search.
    """
    # For all parts within the BOM data.
    for parts in data:
        # Extract the part number
        part_number = parts[0]
        # Calculate the quantity required by multiplying the BOM quantity with the part quantity
        # within the BOM
        quantity = parts[1] * int(quantity)

        # Search Octopart for this part
        #octopart = SearchOctopart(part_number, quantity, search_id)
        #octopart.search_parts()

        # Search FindChips for this part
        findchipsscraper(part_number, quantity, search_id)

    # Filter the Results retrieved from Octopart and FindChips, so only the best combination of
    # suppliers are remaining
    database_process.filter_results(search_id, data)

    # Convert the search results to an Excel format
    excel_process.format_results(search_id)

    # Clear contents of the Results table from this search's data
    database_process.remove_search_rows(search_id)
