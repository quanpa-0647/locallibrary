from django.contrib import admin
from .models import Book, BookInstance, Genre, Author

# Register your models here.
admin.site.register(Genre)

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

admin.site.register(Author, AuthorAdmin)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

# Define the admin class for Book
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inline = BookInstanceInline

admin.site.register(Book, BookAdmin)

# Define the admin class for BookInstance
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

admin.site.register(BookInstance, BookInstanceAdmin)
