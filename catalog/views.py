import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from catalog.forms import RenewBookForm
from catalog.models import Book, BookInstance, Author
from .constants import (
    LoanStatus,
    DEFAULT_RENEWAL_WEEKS,
    MAX_BOOK_PAGINATE,
    MAX_AUTHOR_PAGINATE,
)

def index(request):
    """View function for home page of site."""
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(
        status=LoanStatus.AVAILABLE
    ).count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = MAX_BOOK_PAGINATE
    

class BookDetailView(generic.DetailView):
    model = Book


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    paginate_by = MAX_BOOK_PAGINATE
    template_name = 'catalog/bookinstance_list_borrowed_user.html'


def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', {'book': book})


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=DEFAULT_RENEWAL_WEEKS)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = MAX_AUTHOR_PAGINATE
    
class AuthorDetailView(generic.DetailView):
    model = Author

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name = 'catalog/author_form.html'


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name = 'catalog/author_form.html'


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    template_name = 'catalog/author_confirm_delete.html'
