import random
from sqlalchemy.orm import make_transient

from app import db
from models import Results, Supplier


# Add a new row to the Results table.
def addRow(row):

    new_row = Results(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
    db.session.add(new_row)
    db.session.commit()

# Filter the search results in the table. Removing blacklisted items and retrieving the best prices.
def filterResults(searchID, BOM):

    final_results = Results.query.filter(Results.searchnumber == searchID).all()
    #final_results.remove(Results.query.filter(Results.supplier == 'CONFIRM').all())

    # Delete blacklisted suppliers
    for supplier in (Supplier.query.filter(Supplier.blacklisted == True)).all():
        for listing in (final_results):
            if supplier.name == listing.supplier:
                print(final_results)
                print(listing)
                final_results.remove(listing)
                print("removed")


    #Find the cheapest supplier for each part
    for parts in BOM:

        print(parts)
        i = Results.query.filter(Results.searchnumber == searchID).filter(Results.partnumber == parts[0]).all()

        if (len(i) != 0):

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

                for listing in (Results.query.filter(Results.searchnumber == searchID).filter(Results.partnumber == parts[0]).all()):
                    if listing != selected_listing:
                        try:
                            final_results.remove(listing)
                        except:
                            print('Blacklisted')

            else:
                for listing in (Results.query.filter(Results.searchnumber == searchID).filter(Results.partnumber == parts[0]).all()):
                    final_results.remove(listing)


                not_found = Results('N\A', parts[0], parts[0], 'Not Found', 0, i[0].stockrequired, 0, 0, 'Not Found', searchID)
                final_results.append(not_found)

        else:
            not_found = Results('N\A', parts[0], parts[0], 'Not Found', 0, 0, 0, 0, 'Not Found',
                                searchID)
            final_results.append(not_found)

    removeSearchrows(searchID)
    for item in final_results:
        make_transient(item)
    print(len(final_results))
    db.session.add_all(final_results)
    db.session.commit()

def removeSearchrows(searchID):

    Results.query.filter(Results.searchnumber == searchID).delete()
    db.session.commit()
