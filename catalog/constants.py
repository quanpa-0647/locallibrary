from django.utils.translation import gettext_lazy as _
from django.db import models

MAX_LENGTH_GENRE_NAME = 200
MAX_LENGTH_BOOK_TITLE = 200
MAX_LENGTH_BOOK_SUMMARY = 1000
MAX_LENGTH_ISBN = 13
MAX_LENGTH_AUTHOR_NAME = 100
MAX_LENGTH_BOOK_IMPRINT = 200

class LoanStatus(models.TextChoices):
    MAINTENANCE = 'm', _('Maintenance')
    ON_LOAN = 'o', _('On loan')
    AVAILABLE = 'a', _('Available')
    RESERVED = 'r', _('Reserved')

MAX_BOOK_PAGINATE = 10
MAX_RENEWAL_WEEKS = 4
DEFAULT_RENEWAL_WEEKS = 3
