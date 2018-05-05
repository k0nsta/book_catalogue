import environ

env = environ.Env()

GOOGLE_API_URL = 'https://www.googleapis.com/books/v1/volumes'
GOOGLE_API_KEY = env('GOOGLE_BOOK_API_KEY')
THE_FIRST_INDEX = 0
MOCK_FETCH_TITLE_AUTHOR_RTN_VALUE = {
            'author': 'Google Author',
            'title': 'Google Title',
        }

MOCK_GOOGLE_API_RESPONSE = {
            'kind': 'books#volumes',
            'totalItems': 1,
            'items': [
                {
                    'kind': 'books#volume',
                    'id': 'IHxXBAAAQBAJ',
                    'etag': 'B3N9X8vAMWg',
                    'selfLink': 'https://www.googleapis.com/books/v1/volumes/IHxXBAAAQBAJ',
                    'volumeInfo': {
                        'title': "Google Title",
                        'authors': [
                            'Google Author'
                        ]
                    }
                }
                    ]
            }
