from django.test import TestCase
from datetime import date
from book.models import Book
from borrowing.models import Borrowing
from django.urls import reverse
from user.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.utils import timezone
from borrowing.serializers import (
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer,
)


class BorrowingModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="Test Book", inventory=3, daily_fee=11.3)
        self.user = User.objects.create_user(email="test@test.com")
        self.borrowing1 = Borrowing.objects.create(
            borrow_date=date(2023, 5, 1),
            expected_return_date=date(2023, 5, 10),
            actual_return_date=None,
            user=self.user,
            book=self.book,
        )
        self.borrowing2 = Borrowing.objects.create(
            borrow_date=date(2023, 4, 15),
            expected_return_date=date(2023, 4, 25),
            actual_return_date=None,
            user=self.user,
            book=self.book,
        )
        self.borrowing3 = Borrowing.objects.create(
            borrow_date=date(2023, 6, 1),
            expected_return_date=date(2023, 6, 10),
            actual_return_date=None,
            user=self.user,
            book=self.book,
        )

    def test_str_method(self):
        self.assertEqual(
            str(self.borrowing1), "Borrowing expected return date 2023-05-10"
        )

    def test_ordering(self):
        expected_ordering = [self.borrowing2, self.borrowing1, self.borrowing3]
        self.assertEqual(list(Borrowing.objects.all()), expected_ordering)


class BorrowingViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@test.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.book = Book.objects.create(title="Test Book", inventory=3, daily_fee=11.3)
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date(),
            book=self.book,
        )

    def test_list_borrowings(self):
        url = reverse("borrowing:borrowing-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.borrowing.id)

    def test_retrieve_borrowing(self):
        url = reverse("borrowing:borrowing-detail", args=[self.borrowing.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.borrowing.id)

    def test_return_borrowing(self):
        url = reverse("borrowing:borrowing-return-borrowing", args=[self.borrowing.id])

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(id=self.book.id).inventory, 4)

    def test_return_borrowing_already_returned(self):
        self.borrowing.actual_return_date = timezone.now().date()
        self.borrowing.save()
        url = reverse("borrowing:borrowing-return-borrowing", args=[self.borrowing.id])

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BorrowingSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com", password="testpassword"
        )
        self.book = Book.objects.create(title="Test Book", inventory=3, daily_fee=11.3)
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date(),
            book=self.book,
        )

    def test_borrowing_detail_serializer(self):
        serializer = BorrowingDetailSerializer(self.borrowing)
        expected_data = {
            "id": self.borrowing.id,
            "book": serializer.data.get("book"),
            "borrow_date": serializer.data.get("borrow_date"),
            "expected_return_date": serializer.data.get("expected_return_date"),
            "actual_return_date": serializer.data.get("actual_return_date"),
        }
        self.assertEqual(dict(serializer.data), expected_data)

    def test_borrowing_create_serializer(self):
        borrow_date = str(self.borrowing.borrow_date)
        expected_return_date = str(self.borrowing.expected_return_date)
        serializer = BorrowingCreateSerializer(
            data={
                "user": self.user.id,
                "book": self.book.id,
                "borrow_date": borrow_date,
                "expected_return_date": expected_return_date,
            }
        )
        self.assertTrue(serializer.is_valid())

        borrowing = serializer.save(user=self.user)
        self.assertEqual(borrowing.user, self.user)
        self.assertEqual(borrowing.book, self.book)

    def test_borrowing_return_serializer(self):
        serializer = BorrowingReturnSerializer(self.borrowing)
        expected_data = {"id": self.borrowing.id}
        self.assertEqual(serializer.data, expected_data)
