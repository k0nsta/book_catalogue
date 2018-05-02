import sys
import json

import requests
from .constants import GOOGLE_API_KEY, GOOGLE_API_URL, THE_FIRST_INDEX


def get_original_title_and_name(isbn, **kawargs):
    connection_attempts = 3
    isbn_search_string = 'isbn:{}'.format(isbn)
    payload = {
        'key': GOOGLE_API_KEY,
        'q': isbn_search_string,
        'printType': 'books',
    }
    r = requests.get(GOOGLE_API_URL, params=payload)
    response = r.json()
    while connection_attempts > 0:
        try:
            r = requests.get(GOOGLE_API_URL, params=payload)
            response = r.json()
            if 'items' in response.keys():
                title = response['items'][THE_FIRST_INDEX]['volumeInfo']['title']
                author = response['items'][THE_FIRST_INDEX]['volumeInfo']['authors'][THE_FIRST_INDEX]

                return {
                    'title': title,
                    'author': author
                }
            else:
                return None
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout) as e:
            connection_attempts -= 1
            if not connection_attempts:
                return None


if __name__ == '__main__':
    resp = get_original_title_and_name(sys.argv[1])
    print(json.dumps(resp, indent=4))
