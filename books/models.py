import datetime

from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.functional import cached_property


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


# Create your models here.
class Book(models.Model):
    name = models.CharField("Название книги", max_length=255, null=False, blank=False)
    authors = models.ManyToManyField("BookAuthor", verbose_name="Автор книги", related_name="books",
                                     blank=False)
    publishing_year = models.PositiveIntegerField("Год издания", validators=[max_value_current_year])
    department = models.ForeignKey("Department", verbose_name="Отдел", related_name="books",
                                   on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    @cached_property
    def book_count(self) -> int:
        return self.book_copies.count()

    @cached_property
    def book_count_available(self) -> int:
        return self.book_copies.filter(taken_by__isnull=True).count()

    @cached_property
    def is_book_available(self) -> bool:
        return self.book_count_available > 0

    def __str__(self):
        return f"{', '.join([author.name for author in self.authors.all()])}. {self.name}"


class Customer(models.Model):
    name = models.CharField("Имя посетителя", max_length=255, null=False, blank=False)

    @cached_property
    def taken_book_count(self) -> int:
        return self.taken_books.count()

    class Meta:
        verbose_name = 'Посетитель'
        verbose_name_plural = 'Посетители'

    def __str__(self):
        return self.name


class BookCopy(models.Model):
    book = models.ForeignKey("Book", verbose_name="Книга", related_name="book_copies", on_delete=models.CASCADE,
                             null=False)
    taken_by = models.ForeignKey("Customer", verbose_name="Посетитель, взявший книгу", on_delete=models.CASCADE,
                                 related_name="taken_books", null=True, blank=True)

    class Meta:
        verbose_name = 'Экземпляр книги'
        verbose_name_plural = 'Экземпляры книги'

    def __str__(self):
        return f"Экземпляр книги ID{self.id} ({self.book})"


class BookAuthor(models.Model):
    name = models.CharField("Имя писателя", max_length=255, null=False, blank=False)

    class Meta:
        verbose_name = 'Писатель'
        verbose_name_plural = 'Писатели'

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField("Название отдела", max_length=255, null=False, blank=False)

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.name
