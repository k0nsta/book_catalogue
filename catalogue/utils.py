import requests
import environ

env = environ.Env()

GOOGLE_API_URL = 'https://www.googleapis.com/books/v1/volumes'
GOOGLE_API_KEY = env('GOOGLE_BOOK_API_KEY')
THE_FIRST_INDEX = 0


def get_original_title_and_name(isbn, **kawargs):
    isbn_search_string = 'isbn:{}'.format(isbn)
    payload = {
        'key': GOOGLE_API_KEY,
        'q': isbn_search_string,
        'printType': 'books',
    }
    r = requests.get(GOOGLE_API_URL, params=payload)
    response = r.json()
    title = response['items'][THE_FIRST_INDEX]['volumeInfo']['title']
    author = response['items'][THE_FIRST_INDEX]['volumeInfo']['authors'][THE_FIRST_INDEX]

    return {
        'title': title,
        'author': author
    }
