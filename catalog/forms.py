import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .constants import MAX_RENEWAL_WEEKS, DEFAULT_RENEWAL_WEEKS

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text=_(f"Enter a date between now and {MAX_RENEWAL_WEEKS} weeks (default {DEFAULT_RENEWAL_WEEKS}).")
    )

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=MAX_RENEWAL_WEEKS):
            raise ValidationError(_(f'Invalid date - renewal more than {MAX_RENEWAL_WEEKS} weeks ahead'))

        # Always return the cleaned data.
        return data
