from borrowing.views import BorrowingViewSet
from rest_framework.routers import DefaultRouter

app_name = "borrowing"


router = DefaultRouter()
router.register("", BorrowingViewSet)
urlpatterns = router.urls
