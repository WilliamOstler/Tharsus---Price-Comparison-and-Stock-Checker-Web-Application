from sqlalchemy import func
from app import db
from models import Results
from SearchOctopart import SearchOctopart
import DatabaseProcess


# TODO: This is sample data, this data will be retrieved from the Excel BOM once complete.
BOMQuantity = 5
BOM = [['AT0603FRE0747KL', 3],
       ['MPTC-02-80-02-6.30-01-L-V', 15],
       ['TLV3702IDGKR', 20],
       ['SMCJ51A-E3/57T', 2],
       ['IPB017N10N5LF', 6],
       ['TCAN1051HVDR', 4],
       ['STM32F427IIT6', 4],
       ['AG1012F', 100]]


# Retrieve respected SearchID to use for this search
if db.session.query(Results).count() == 0:
    searchID = 1
else:
    searchID = int(db.session.query(func.max(Results.searchnumber)).scalar()) + 1

# Loop for all items in the BOM
for parts in BOM:

    # Retrieve the partnumber and quantity for the current BOM item.
    partnumber = parts[0]
    quantity = parts[1]*BOMQuantity

    # Search Octopart for the part
    octopart = SearchOctopart(partnumber, quantity, searchID)
    octopart.searchParts()

    # Search FindCips for the part
    #findchips = SearchFindChips(partnumber, quantity, searchID)
    #findchips.searchParts()


# Filter the Results retrieved, so the best combination of suppliers are found
DatabaseProcess.filterResults(searchID, BOM)

# Convert the results to an Excel format
#searchResults = convertToExcel()



