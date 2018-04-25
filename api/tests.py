from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from catalogue.models import Bookmark
from catalogue.models import Book
from catalogue.models import Author
from catalogue.models import Category
from catalogue.models import Publisher


class BookmarkViewSetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_admin = User.objects.create_user(
                                    username='test_admin',
                                    password='54321qaz',
                                    is_superuser=True
                                    )
        cls.test_user = User.objects.create_user(
                                    username='test1',
                                    password='12345qaz'
                                    )
        cls.test_admin.save()
        cls.test_user.save()

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

    def test_create_bookmark_by_authorized_user(self):
        self.login = self.client.login(username='test1', password='12345qaz')
        # print('User from bookmark :', self.test_admin)
        print('Book :', self.test_book1)
        bookmark_data = {
            'user': self.login,
            'in_bookmarks': True,
            'book': self.test_book1
        }
        print('data :', bookmark_data)
        response = self.client.post(self.bookmark_url, bookmark_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bookmark.objects.filter(user=self.test_user).count(), 1)

    # def test_create_only_own_bookmark_by_authorized_user(self):
    #     self.login = self.client.login(username='test1', password='12345qaz')
    #     bookmark_data = {
    #         'user': self.test_admin.id,
    #         'in_bookmarks': True,
    #         'book': self.test_book1.id,
    #     }
    #     response = self.client.post(self.bookmark_url, bookmark_data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Bookmark.objects.count(), 1)

    # def test_anonymous_user_no_access_to_bookmarks(self):
    #     response = self.client.get(self.bookmark_url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_admin_access_to_all_bookmarks(self):
    #     self.login = self.client.login(username='test_admin', password='54321qaz')
    #     bookmark = Bookmark.objects.create(user=self.test_user, book=self.test_book1)
    #     response = self.client.get(self.bookmark_url)
    #     print(response)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIsNotNone(bookmark)

    # def test_admin_can_create_any_users_bookmark(self):
    #     self.login = self.client.login(username='test_admin', password='54321qaz')
    #     bookmark_data = {
    #         'user': self.test_user.id,
    #         'in_bookmarks': True,
    #         'book': self.test_book1.id,
    #     }
    #     response = self.client.post(self.bookmark_url, bookmark_data)
    #     # print(response.status_code)
    #     # print(Bookmark.objects.filter(user_id=self.test_user))
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     # self.assertEqual(Bookmark.objects.filter(user_id=self.test_user).count(), 1)

    # def test_authorized_user_cant_create_other_users_bookmarks(self):
    #     pass




class UserViewSetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def test_only_admin_has_access_user_list(self):
        pass

    def test_only_admin_has_access_user_detail(self):
        pass

    def test_user_hasnot_access_user_list(self):
        pass

    def test_user_hasnot_access_user_detail(self):
        pass

    def test_correct_view_for_bookmarks_amount_user_list(self):
        pass

    def test_correct_view_for_bookmarks_amount_user_detail(self):
        pass
