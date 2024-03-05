from django.contrib import admin

from books.models import Book, Customer, BookCopy, BookAuthor, Department


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    pass


@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass