import environ

env = environ.Env()

GOOGLE_API_URL = 'https://www.googleapis.com/books/v1/volumes'
GOOGLE_API_KEY = env('GOOGLE_BOOK_API_KEY')
THE_FIRST_INDEX = 0
# API_RESPONSE = env('API_RESPONSE_BOOK_CATALOGUE_TEST')




