from rest_framework import routers

from book.views import BookListViewSet

router = routers.DefaultRouter()
router.register("book_list", BookListViewSet)


urlpatterns = router.urls

app_name = "book"
