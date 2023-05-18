import rest_framework.permissions
from drf_spectacular.types import OpenApiTypes
from rest_framework import viewsets

from book.models import Book
from book.serializers import BookListSerializer, BookDetailSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter


class BookListViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the movies with filters"""
        title = self.request.query_params.get("title")
        authors = self.request.query_params.get("authors")
        daily_fee = self.request.query_params.get("daily_fee")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if authors:
            queryset = queryset.filter(author__icontains=authors)

        if daily_fee:
            daily_fee_ids = self._params_to_ints(daily_fee)
            queryset = queryset.filter(daily_fee__in=daily_fee_ids)

        return queryset.distinct()

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "authors",
                type=OpenApiTypes.STR,
                description="Filter by authors (ex. ?authors=Smith)",
            ),
            OpenApiParameter(
                "daily_fee",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by daily_fee (ex. ?daily_fee=2,5)",
            ),
            OpenApiParameter(
                "title",
                type=OpenApiTypes.STR,
                description="Filter by book title (ex. ?title=fiction)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
