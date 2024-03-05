from .models import Book, Customer, BookCopy, BookAuthor, Department
from rest_framework import serializers


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class BookAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAuthor
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source='department.name')
    authors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'authors', 'publishing_year', 'department', 'is_book_available']


class CustomerBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name']


class BookCopySerializer(serializers.ModelSerializer):
    taken_by = serializers.CharField(source='taken_by.name', required=False)

    class Meta:
        model = BookCopy
        fields = ['id', 'book', 'taken_by']

    class JSONAPIMeta:
        included_resources = ['book', 'taken_by']

    included_serializers = {
        'book': BookSerializer,
    }


class CustomerListSerializer(CustomerBaseSerializer):
    class Meta(CustomerBaseSerializer.Meta):
        fields = CustomerBaseSerializer.Meta.fields + ['taken_book_count']


class CustomerDetailSerializer(serializers.ModelSerializer):
    taken_books = serializers.StringRelatedField(many=True, required=False)

    class Meta(CustomerBaseSerializer.Meta):
        fields = CustomerBaseSerializer.Meta.fields + ['taken_books']


