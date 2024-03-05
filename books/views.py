from django.shortcuts import render
from rest_framework import viewsets
from books.models import Book, Customer, BookCopy, Department
from books.serializers import BookSerializer, CustomerListSerializer, CustomerDetailSerializer, BookCopySerializer, \
    DepartmentSerializer


# Create your views here.


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('department').prefetch_related('authors')
    serializer_class = BookSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        author = self.request.query_params.get('author', None)
        if author is not None:
            qs = qs.filter(authors__id=author)

        publishing_year = self.request.query_params.get('publishing_year', None)
        if publishing_year is not None:
            qs = qs.filter(year_publishing=publishing_year)

        department = self.request.query_params.get('department', None)
        if department is not None:
            qs = qs.filter(department__id=department)

        is_book_available = self.request.query_params.get('is_book_available', None)
        if is_book_available == 'true':
            qs = qs.filter(is_book_available=True)
        elif is_book_available == 'false':
            qs = qs.filter(is_book_available=False)

        return qs


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.prefetch_related('taken_books__book')

    def get_serializer_class(self):
        if getattr(self, 'action', None) == 'list':
            return CustomerListSerializer
        return CustomerDetailSerializer


class BookCopyViewSet(viewsets.ModelViewSet):
    queryset = BookCopy.objects.select_related('book')
    serializer_class = BookCopySerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
