from rest_framework import serializers

from book.serializers import BookListSerializer
from borrowing.models import Borrowing


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book_id = BookListSerializer(many=True, read_only=True)
    borrow_date = serializers.DateField(read_only=True)
    expected_return_date = serializers.DateField(read_only=True)

    class Meta:
        model = Borrowing
        exclude = ("user_id",)


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        exclude = ("actual_return_date", "user_id")


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id",)
