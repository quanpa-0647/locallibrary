from django.utils.translation import gettext_lazy as _

MAX_LENGTH_GENRE_NAME = 200
MAX_LENGTH_BOOK_TITLE = 200
MAX_LENGTH_BOOK_SUMMARY = 1000
MAX_LENGTH_ISBN = 13
MAX_LENGTH_AUTHOR_NAME = 100
MAX_LENGTH_BOOK_IMPRINT = 200

LOAN_STATUS = (
    ('m', _('Maintenance')),
    ('o', _('On loan')),
    ('a', _('Available')),
    ('r', _('Reserved')),
)
