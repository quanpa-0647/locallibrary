from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import uuid

from catalog.constants import (
    MAX_LENGTH_GENRE_NAME,
    MAX_LENGTH_BOOK_TITLE,
    MAX_LENGTH_BOOK_SUMMARY,
    MAX_LENGTH_ISBN,
    MAX_LENGTH_AUTHOR_NAME,
    MAX_LENGTH_BOOK_IMPRINT,
    LOAN_STATUS
)


class Genre(models.Model):
    """Model representing a book genre."""

    name = models.CharField(
        max_length=MAX_LENGTH_GENRE_NAME,
        help_text=_('Enter a book genre (e.g. Science Fiction)')
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""

    title = models.CharField(max_length=MAX_LENGTH_BOOK_TITLE)

    author = models.ForeignKey(
        'Author',
        on_delete=models.SET_NULL,
        null=True
    )

    summary = models.TextField(
        max_length=MAX_LENGTH_BOOK_SUMMARY,
        help_text=_('Enter a brief description of the book')
    )

    isbn = models.CharField(
        'ISBN',
        max_length=MAX_LENGTH_ISBN,
        unique=True,
        help_text=_('13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    )

    genre = models.ManyToManyField(
        'Genre',
        help_text=_('Select a genre for this book')
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Model representing a specific copy of a book."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text=_('Unique ID for this particular book across whole library')
    )

    book = models.ForeignKey('Book', on_delete=models.RESTRICT)

    imprint = models.CharField(max_length=MAX_LENGTH_BOOK_IMPRINT)

    due_back = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text=_('Book availability'),
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Model representing an author."""

    first_name = models.CharField(max_length=MAX_LENGTH_AUTHOR_NAME)
    last_name = models.CharField(max_length=MAX_LENGTH_AUTHOR_NAME)

    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(_('Died'), null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
