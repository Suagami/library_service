from django.urls import path, include
from rest_framework import routers

from books.views import BookViewSet, CustomerViewSet, DepartmentViewSet, BookCopyViewSet

router = routers.DefaultRouter()
router.register('books', BookViewSet)
router.register('customers', CustomerViewSet)
router.register('departments', DepartmentViewSet)
router.register('book_copies', BookCopyViewSet)
urlpatterns = [
    path('api/v1/', include(router.urls)),
]