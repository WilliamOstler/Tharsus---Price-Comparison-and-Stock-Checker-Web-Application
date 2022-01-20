"""
Responsible for retrieving data from Octopart.com, using the OctopartAPI
Adds results found to the Results data table.
"""
import requests
from Search import database_process

class SearchOctopart:
    """
    This class is responsible for retriving part listings from Octopart. The class has the
    attributes: part_number, quantity and search_id.
    """

    # Constructor method
    def __init__(self, part_number, quantity, search_id):
        self.part_number = part_number
        self.quantity = quantity
        self.search_id = search_id


    def search_parts(self):
        """"
        The method, searchparts, will search for all lisitngs for the given part number and return
        the data in a JSON format. The query is made up of a GraphQL statement. After results are
        retrieved, they are formatted and added to the database table.
        """
        results = requests.post(

            # Set up header information
            'https://octopart.com/api/v4/endpoint',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'token': '04c50e63-6c02-4797-9df5-5db1cb7d2b2e'
            },

            # GraphQL query
            json={
                'query': '''
                query Search($q: String!, $currency: String!) { 
                    search_mpn(q: $q, currency: $currency) { 
                        results { 
                            part { 
                                sellers {
                                    company{
                                        name
                                    }
                                    offers {
                                        click_url
                                        inventory_level
                                        prices {
                                          price
                                          currency
                                          quantity
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                ''',

                'variables': {
                    'q': f'{self.part_number}',
                    'currency': 'GBP'
                },
            },
        )

        # Format results from JSON format into Array format
        results = self.format_results(results.json())

        # Add the listings found to the database
        for listing in results:
            database_process.add_row(listing)



    def format_results(self, results):
        """
        This method takes the results, outputted from the GraphQL query, from a JSON format to an
        array format. It uses for loops to loop through the JSON data, extracting relevant data.
        """

        # Array containing formatted results
        formatted_results = []

        # For each of the listings found within the JSON data
        for listing in (results['data']['search_mpn']['results'][0]['part']['sellers']):

            # Extract each supplier that sells the part, and their stock level.
            supplier = listing['company']['name']
            stock = listing['offers'][0]['inventory_level']

            # Find the correct price for the amount of stock required to buy. i.e., some suppliers
            # have different prices for different purchasing quantities.
            current_optimum_listing = 0
            for price in (listing['offers'][0]["prices"]):

                if price['quantity'] <= self.quantity:
                    if price['quantity'] > current_optimum_listing:
                        part_cost = price['price']

            # Extract the listing link
            link = listing['offers'][0]['click_url']

            # Add data retrived to the formatted results, IF the supplier has enough stock
            if stock > 0:
                formatted_results.append(["Octopart", self.part_number, self.part_number,
                                          supplier, stock, self.quantity, part_cost,
                                          part_cost * self.quantity, link,
                                          self.search_id])

        return formatted_results
