"""
Contains functionality which involves interaction with the Results data table.
"""
import random
from sqlalchemy.orm import make_transient
from app import db
from models import Results, Supplier


def add_row(row):
    """
    Adds a new row to the Results data table. This occurs when a new listing has been found.
    :param row: A list containing the data to be added to the row.
    """
    new_row = Results(row[0], row[1], row[2], row[3], row[4],
                      row[5], row[6], row[7], row[8], row[9])
    db.session.add(new_row)
    db.session.commit()



def filter_results(search_id, bill_of_materials):
    """
    This method contins functionality which filters through the complete set of listings found for
    a BOM, leaving just one listing for each part in the data table for that search.
    The method firstly removes blacklisted suppliers, then finds the cheapest price available
    from a supplier, with enough stock, for each part in the BOM.
    All suppliers who sell this stock, for this price, are then considered.
    If any of the remaining listings are from favourited suppliers, then the listings from
    non-favourited suppliers are removed from consideration.
    Of the final listings for that part, they are all equivalent so a random choice is made to
    obtain the chosen supplier for that part.
    :param search_id: The search ID for the given search
    :param bill_of_materials: the BOM list, containing all parts and quantities.
    """

    # final results is an array which considers all the considered listings. These listings will be
    # removed until there are only the most optimum remaining
    final_results = Results.query.filter(Results.searchnumber == search_id).all()

    # Delete blacklisted suppliers
    remove_blacklisted_suppliers(final_results)

    # Find the cheapest supplier for each part
    for parts in bill_of_materials:

        # Retrieve all listing for the part
        part_listings = Results.query.filter(Results.searchnumber == search_id). \
            filter(Results.partnumber == parts[0]).all()

        # If there are potential listings found for the part
        if len(part_listings) != 0:

            # Calculate the lowest price for the part
            lowestprice = part_listings[0]
            for item in part_listings:
                if item.totalprice <= lowestprice.totalprice:
                    lowestprice = item

            # Retrieve a list of suppliers who sell the part for the lowest price, and have enough
            # stock.
            suppliers = []
            for item in part_listings:
                if item.totalprice == lowestprice.totalprice and item.stock >= item.stockrequired:
                    suppliers.append(item)

            # If there any listings available to be considered.
            if len(suppliers) > 0:

                # Retrieve list of favourited suppliers
                favourited_supplers = Supplier.query.filter(Supplier.favourited == 1).all()
                preferred_listings = []

                # Calculate weather there are any favourites suppliers remaining.
                # If there are, then only consider these.
                for supplier in suppliers:
                    for f_supplier in favourited_supplers:
                        if supplier.supplier == f_supplier.name:
                            preferred_listings.append(supplier)

                # If no favourited suppliers remaining, make no changes to considered listings
                if len(preferred_listings) == 0:
                    preferred_listings = suppliers

                # Make random choice within the remaining listings considered
                selected_listing = random.choice(preferred_listings)

                # Remove any listings from the final results which were not selected
                for listing in (Results.query.filter(Results.searchnumber == search_id).
                        filter(Results.partnumber == parts[0]).all()):
                    if listing != selected_listing:
                        try:
                            final_results.remove(listing)
                        except:
                            print('Blacklisted')

            # If there are no listings to be considered, then remove all listings for that part and
            # add a placeholder row, indicated no stock was found.
            else:
                for listing in (Results.query.filter(Results.searchnumber == search_id).
                        filter(Results.partnumber == parts[0]).all()):
                    final_results.remove(listing)

                not_found = Results('N-A', parts[0], parts[0], 'Not Found',
                                    0, part_listings[0].stockrequired, 0, 0, 'Not Found', search_id)

                final_results.append(not_found)

        # If there are no listings to be considered, then remove all listings for that part and
        # add a placeholder row, indicated no stock was found.
        else:
            not_found = Results('N-A', parts[0], parts[0], 'Not Found', 0, 0, 0, 0, 'Not Found',
                                search_id)
            final_results.append(not_found)

    # Remove all listings, for this search, from the table and replace with only the selected ones.
    remove_search_rows(search_id)
    for item in final_results:
        make_transient(item)

    db.session.add_all(final_results)
    db.session.commit()


def remove_blacklisted_suppliers(final_results):
    """
    Responsible for removing blacklisted suppliers from the set of considered suppliers.
    :param final_results: The suppliers which are currently being cosidered.
    """
    for supplier in Supplier.query.filter(Supplier.blacklisted == True).all():
        for listing in final_results:
            # If supplier is blacklisted then remove them from consideration.
            if supplier.name == listing.supplier:
                final_results.remove(listing)


def remove_search_rows(search_id):
    """
    Removes all rows related to a search from the Results data table.
    :param search_id: The search id of the rows to be deleted.
    """
    Results.query.filter(Results.searchnumber == search_id).delete()
    db.session.commit()
