from collections import OrderedDict

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from catalogue.models import Bookmark
from catalogue.models import Book
from catalogue.models import Author
from catalogue.models import Category
from catalogue.models import Publisher


class BaseTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.test_admin = User.objects.create_user(
                                    username='test_admin',
                                    password='54321qaz',
                                    is_staff=True,
                                    is_superuser=True,
                                    )
        cls.test_user = User.objects.create_user(
                                    username='test1',
                                    password='12345qaz'
                                    )
        cls.test_admin.save()
        cls.test_user.save()

        cls.admin_login_data = {'username': 'test_admin', 'password': '54321qaz'}
        cls.test_user_login_data = {'username': 'test1', 'password': '12345qaz'}

        cls.test_author = Author.objects.create(first_name='Mike', last_name='Lee')
        cls.test_author.save()

        cls.test_publisher = Publisher.objects.create(title='Test Publisher')
        cls.test_publisher.save()

        cls.test_category = Category.objects.create(title='Test Category')
        cls.test_category.save()

        cls.test_book1 = Book.objects.create(title='Book test1',
                                             author=cls.test_author,
                                             category=cls.test_category,
                                             publisher=cls.test_publisher
                                             )
        cls.test_book2 = Book.objects.create(title='Book test2',
                                             author=cls.test_author,
                                             category=cls.test_category,
                                             publisher=cls.test_publisher
                                             )
        cls.test_book1.save()
        cls.test_book2.save()
        cls.bookmark_url = reverse('bookmark-list')
        cls.user_list_url = reverse('user-list')
        cls.books_url = reverse('book-list')


class BookmarkViewSetTest(BaseTestCase):

    def test_create_bookmark_by_authorized_user(self):
        self.login = self.client.login(**self.test_user_login_data)
        bookmark_data = {
            'in_bookmarks': True,
            'book': self.test_book1.id,
        }
        response = self.client.post(self.bookmark_url, bookmark_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bookmark.objects.filter(user=self.test_user).count(), 1)

    def test_create_only_own_bookmark_by_authorized_user(self):
        self.login = self.client.login(**self.test_user_login_data)
        bookmark_data = {
            'user': self.test_admin.id,
            'in_bookmarks': True,
            'book': self.test_book1.id,
        }
        response = self.client.post(self.bookmark_url, bookmark_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bookmark.objects.filter(user=self.test_user).count(), 1)

    def test_anonymous_user_no_access_to_bookmarks(self):
        response = self.client.get(self.bookmark_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_access_to_all_bookmarks(self):
        self.login = self.client.login(**self.admin_login_data)
        bookmark1 = Bookmark.objects.create(user=self.test_user, book=self.test_book1)
        valid_data = {
                    'id': bookmark1.id,
                    'user': self.test_user.id,
                    'user_name': self.test_user.username,
                    'book': self.test_book1.id,
                    'in_bookmarks': False,
        }

        response = self.client.get(self.bookmark_url)
        for i in response.data[0].keys():
            self.assertEqual(response.data[0][i], valid_data[i])
        self.assertEqual(response.data[0], valid_data)

    def test_admin_can_create_any_users_bookmark(self):
        self.login = self.client.login(**self.admin_login_data)
        bookmark_data = {
            'user': self.test_user.id,
            'in_bookmarks': True,
            'book': self.test_book1.id,
        }
        response = self.client.post(self.bookmark_url, bookmark_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bookmark.objects.filter(user_id=self.test_user).count(), 1)

    def test_authorized_user_cant_create_other_users_bookmarks(self):
        self.login = self.client.login(username='test1', password='12345qaz')
        bookmark_data = {
            'user': self.test_admin.id,
            'in_bookmarks': True,
            'book': self.test_book1.id,
        }
        response = self.client.post(self.bookmark_url, bookmark_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bookmark.objects.filter(user_id=self.test_user).count(), 1)


class UserViewSetTest(BaseTestCase):

    def test_anonymous_has_not_access_user_list(self):
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonumous_has_not_access_user_detail(self):
        detail_url = reverse('user-detail', args=(self.test_user.id, ))
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_has_access_user_list(self):
        self.login = self.client.login(**self.admin_login_data)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_has_access_user_detail(self):
        detail_url = reverse('user-detail', args=(self.test_user.id, ))
        self.login = self.client.login(**self.test_user_login_data)
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_has_access_own_profile(self):
        detail_url = reverse('user-detail', args=(self.test_user.id, ))
        self.login = self.client.login(**self.test_user_login_data)

        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_view_for_bookmarks_amount_in_user_list(self):
        self.login = self.client.login(**self.admin_login_data)
        bookmark1 = Bookmark.objects.create(
                                user=self.test_user,
                                book=self.test_book1,
                                in_bookmarks=True
                    )
        bookmark2 = Bookmark.objects.create(
                                user=self.test_user,
                                book=self.test_book2,
                                in_bookmarks=True
                    )

        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['bookmark_amount'], 2)

    def test_correct_view_for_bookmarks_amount_user_detail(self):
        detail_url = reverse('user-detail', args=(self.test_user.id, ))

        self.login = self.client.login(**self.admin_login_data)
        bookmark1 = Bookmark.objects.create(
                                user=self.test_user,
                                book=self.test_book1,
                                in_bookmarks=True
                    )
        bookmark2 = Bookmark.objects.create(
                                user=self.test_user,
                                book=self.test_book2,
                                in_bookmarks=True
                    )
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bookmark_amount'], 2)


class BookViewSetTest(BaseTestCase):

    def test_filter_by_exact_title(self):
        filter_string = '?title={}'.format(self.test_book1.title)
        response = self.client.get(self.books_url + filter_string)
        self.assertEqual(response.data[0]['id'], 1)

    def test_filter_by_icontains_title(self):
        filter_string = '?title__icontains=est2'
        response = self.client.get(self.books_url + filter_string)
        self.assertEqual(response.data[0]['id'], 2)
