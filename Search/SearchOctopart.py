import json
import requests


class SearchOctopart:

    def __init__(self, part_number):
        self.part_number = part_number

    def searchParts(self):

        results = requests.post(
            'https://octopart.com/api/v4/endpoint',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'token': 'd5a2518a-5e6d-411f-abf5-4b0640a30153'
            },
            json={
                'query': '''
                query Search($q: String!) { 
                    search_mpn(q: $q) { 
                        results { 
                            part { 
                                mpn
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

        return json.dumps(results.json(), indent=2)


if __name__ == '__main__':
    search = SearchOctopart('CS4200V-01L')
    results = search.part_number()
