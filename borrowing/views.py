from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from book.models import Book
from borrowing.models import Borrowing
from borrowing.permissions import IsOwnerOrAdmin
from borrowing.serializers import (
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Borrowing.objects.all()
        else:
            queryset = Borrowing.objects.filter(user=user)

        is_active = self.request.query_params.get("is_active")
        if is_active:
            queryset = queryset.filter(actual_return_date__isnull=True)

        user = self.request.query_params.get("user")
        if user and self.request.user.is_staff:
            queryset = queryset.filter(user=user)

        return queryset

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return BorrowingDetailSerializer
        elif self.action == "create":
            return BorrowingCreateSerializer
        elif self.action == "return_borrowing":
            return BorrowingReturnSerializer
        return BorrowingDetailSerializer

    def perform_create(self, serializer):
        book = serializer.validated_data["book"]
        user = self.request.user

        book = get_object_or_404(Book, id=book.pk)
        if book.inventory == 0:
            raise serializers.ValidationError("Book is out of stock.")

        book.inventory -= 1
        book.save()

        serializer.save(user=user)

    @action(detail=True, methods=["post"])
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            raise serializers.ValidationError("Borrowing has already been returned.")

        borrowing.actual_return_date = timezone.now().date()
        borrowing.save()

        book = Book.objects.filter(id=borrowing.book.pk)
        book.update(inventory=models.F("inventory") + 1)

        serializer = self.get_serializer(borrowing)
        return Response(serializer.data, status=status.HTTP_200_OK)
