import rest_framework.permissions
from rest_framework import viewsets

from book.models import Book
from book.serializers import BookListSerializer, BookDetailSerializer


class BookListViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_permissions(self):
        if self.action == "list":
            permission_classes = (rest_framework.permissions.AllowAny,)
        elif self.action == "retrieve":
            permission_classes = (rest_framework.permissions.AllowAny,)
        else:
            permission_classes = (rest_framework.permissions.IsAdminUser,)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        if self.action == "retrieve":
            return BookDetailSerializer
        else:
            return BookDetailSerializer
