from sqlalchemy import func
from models import Results
from app import db
from Search.FindChipsScraping import findchipsscraper
from Search.SearchOctopart import SearchOctopart
from Search import DatabaseProcess
from Search import ExcelProcess


# Retrieve respected SearchID to use for this search
def get_search_id():
    if db.session.query(Results).count() == 0:
        searchID = 1
        return searchID
    else:
        searchID = int(db.session.query(func.max(Results.searchnumber)).scalar()) + 1
        return searchID



# Loop for all items in the BOM
def search(data, quantity, searchID):
    for parts in data:
    # Retrieve the partnumber and quantity for the current BOM item.
        partnumber = parts[0]
        quantity = parts[1] * int(quantity)

    # Search Octopart for the part
        #octopart = SearchOctopart(partnumber, quantity, searchID)
        #octopart.searchParts()

    # Search FindCips for the part
        findchipsscraper(partnumber, quantity, searchID)

    # Filter the Results retrieved, so the best combination of suppliers are found
    DatabaseProcess.filterResults(searchID, data)

    # Convert the results to an Excel format
    ExcelProcess.formatResults(searchID)

    #Clear contents of DB for search
    DatabaseProcess.removeSearchrows(searchID)

    return(searchID)




