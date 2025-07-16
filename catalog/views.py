from django.shortcuts import render
from catalog.models import Book, BookInstance, Author, Genre
from django.views import generic
from django.shortcuts import get_object_or_404
from .constants import LoanStatus

# Create your views here.
def index(request):
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact=LoanStatus.AVAILABLE).count()
    # The 'all()' is implied by default.
    num_authors = Author.objects.count()  # The 'all()' is implied by default.
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BookListView, self).get_context_data(**kwargs)
        
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        
        return context

class BookDetailView(generic.DetailView):
    model = Book
    
def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    
    return render(request, 'catalog/book_detail.html', context={'book': book})
