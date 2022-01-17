import random

from app import db
from models import Results, Supplier


# Add a new row to the Results table.
def addRow(row):

    new_row = Results(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    db.session.add(new_row)
    db.session.commit()

# Filter the search results in the table. Removing blacklisted items and retrieving the best prices.
def filterResults(searchID, BOM):

    # Delete blacklisted suppliers
    for supplier in (Supplier.query.filter(Supplier.blacklisted == True)).all():
        for listing in (Results.query.filter(Results.searchnumber == searchID).all()):

            if supplier.name == listing.supplier:

                print(f"Removing blacklisted supplier: {supplier.name}")
                Results.query.filter(Results.supplier == listing.supplier).delete()
                db.session.commit()


    #Find the cheapest supplier for each part
    for parts in BOM:
        i = Results.query.filter(Results.searchnumber == searchID).filter(Results.partnumber == parts[0]).all()

        lowestprice = i[0]

        for j in i:
            if j.totalprice <= lowestprice.totalprice:
                lowestprice = j


        suppliers = []
        for x in i:
            if x.totalprice == lowestprice.totalprice and x.stock >= x.stockrequired:
                suppliers.append(x)


        if len(suppliers) > 0:

            favourited_supplers = Supplier.query.filter(Supplier.favourited == 1).all()
            preferred_listings = []

            for supplier in suppliers:
                for f_supplier in favourited_supplers:
                    if supplier.supplier == f_supplier.name:
                        preferred_listings.append(supplier)

            if len(preferred_listings) == 0:
                preferred_listings = suppliers

            selected_listing = random.choice(preferred_listings)
            print(f"Listing choice for part {selected_listing.partnumber}: {selected_listing}")

            for listing in (Results.query.filter(Results.searchnumber == searchID).filter(Results.partnumber == parts[0]).all()):
                if listing != selected_listing:
                    print(f"Disregarding listing: {listing}")
                    db.session.delete(listing)
                    db.session.commit()

        else:
            for listing in (Results.query.filter(Results.searchnumber == searchID).filter(Results.partnumber == parts[0]).all()):
                print(f"Disregarding listing: {listing}")
                db.session.delete(listing)
                db.session.commit()

            not_found = Results('N\A', parts[0], 'Not Found', 0, i[0].stockrequired, 0, 0, 'Not Found', searchID)
            db.session.add(not_found)
            db.session.commit()
            print(f"No results found for {parts[0]}")


def removeSearchrows(searchID):

    Results.query.filter(Results.searchnumber == searchID).delete()
    db.session.commit


