import requests
from Search import DatabaseProcess


class SearchOctopart:

    # Constructor method
    def __init__(self, part_number, quantity, searchID):
        self.part_number = part_number
        self.quantity = quantity
        self.searchID = searchID

    # Searches Octopart for part listings
    def searchParts(self):

        results = requests.post(

            # Set up header information
            'https://octopart.com/api/v4/endpoint',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'token': 'd5a2518a-5e6d-411f-abf5-4b0640a30153'
            },

            # GraphQL query
            json={
                'query': '''
                query Search($q: String!) { 
                    search_mpn(q: $q) { 
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
                    'q': '%s' % self.part_number
                },
            },
        )

        # Format results from JSON format into Array format
        results = self.formatResults(results.json())

        # Add the listings found to the database
        for listing in results:
            DatabaseProcess.addRow(listing)

    # Format the results found from octopart from a JSON format into an Array format
    def formatResults(self, results):

        formatted_results = []

        # For each of the listings
        for listing in (results['data']['search_mpn']['results'][0]['part']['sellers']):

            supplier = listing['company']['name']
            stock = listing['offers'][0]['inventory_level']

            # Find the correct price for the amount of stock required to buy
            current_optimum_listing = 0
            for price in (listing['offers'][0]["prices"]):

                if price['quantity'] <= self.quantity:
                    if price['quantity'] > current_optimum_listing:
                        part_cost = price['price']


            link = listing['offers'][0]['click_url']

            # Add data retrived to the formatted_results IF the supplier has enough stock
            if stock > 0:
                formatted_results.append(["Octopart", self.part_number, self.part_number, supplier, stock,
                                          self.quantity, part_cost, part_cost * self.quantity, link, self.searchID])

        return formatted_results
