from unittest import mock
from django.test import TestCase

from .models import Book
from .utils import fetch_title_author
from .constants import MOCK_FETCH_TITLE_AUTHOR_RTN_VALUE
from .constants import MOCK_GOOGLE_API_RESPONSE
from .constants import GOOGLE_API_KEY
from .constants import GOOGLE_API_URL


class BookModelTestCase(TestCase):
    @mock.patch('catalogue.models.utils')
    def test_save_book_calls_google_api(self, mock_utils):
        mock_utils.fetch_title_author.return_value = MOCK_FETCH_TITLE_AUTHOR_RTN_VALUE

        book = Book(
                    title='Some title',
                    isbn='12345'
                )
        book.save()

        self.assertEqual(book.original_author, 'Google Author')
        self.assertEqual(book.original_title, 'Google Title')
        mock_utils.fetch_title_author.assert_called_once_with('12345')


class GetOriginalTitleAndNameTestCase(TestCase):
    @mock.patch('catalogue.utils.requests.get')
    def test_get_original_title_and_name_from_google_api(self, mock_get):
        function_return_value = MOCK_FETCH_TITLE_AUTHOR_RTN_VALUE
        fake_response_value = MOCK_GOOGLE_API_RESPONSE
        mock_response = mock.Mock()
        mock_response.json.return_value = fake_response_value
        mock_response.status_code = 200

        # Define fake API response
        mock_get.return_value = mock_response

        # Function call with fake data
        result = fetch_title_author('12345')

        self.assertEqual(result, function_return_value)
        mock_get.assert_called_with(GOOGLE_API_URL, params={
                                    'key': GOOGLE_API_KEY,
                                    'q': 'isbn:12345',
                                    'printType': 'books',
                                    })
