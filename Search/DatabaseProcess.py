from app import db
from models import Results, Supplier


# Add a new row to the Results table.
def addRow(row):

    new_row = Results(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    db.session.add(new_row)
    db.session.commit()

# Filter the search results in the table. Removing blacklisted items and retrieving the best prices.
def filterResults(searchID):

    # Delete blacklisted suppliers
    for supplier in (Supplier.query.filter(Supplier.blacklisted == True)).all():
        for listing in (Results.query.filter(Results.searchnumber == searchID).all()):

            if supplier.name == listing.supplier:

                Results.query.filter(Results.supplier == listing.supplier).delete()
                db.session.commit()


    #Find the cheapest supplier for each part
    # TODO: Add DB Query to remove part prices which are not the cheapest price.


def removeSearchrows(searchID):

    Results.query.filter(Results.searchnumber == searchID).delete()
    db.session.commit

