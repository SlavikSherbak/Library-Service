from rest_framework import serializers

from book.serializers import BookListSerializer
from borrowing.models import Borrowing


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookListSerializer(many=False, read_only=True)
    borrow_date = serializers.DateField(read_only=True)
    expected_return_date = serializers.DateField(read_only=True)

    class Meta:
        model = Borrowing
        exclude = ("user",)


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        exclude = ("actual_return_date", "user")


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id",)
