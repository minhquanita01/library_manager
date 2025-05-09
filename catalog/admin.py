from django.contrib import admin
from .models import Book, BookCategory, Author, Publisher
# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'date_of_death')
    fields = ['name', 'biography', ('date_of_birth', 'date_of_death')]
    search_fields = ('name',)

@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'email')
    search_fields = ('name',)

class AuthorInline(admin.TabularInline):
    model = Book.author.through
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_authors', 'isbn', 'category', 'publisher', 'available_copies')
    list_filter = ('category', 'publisher')
    fieldsets = (
        (None, {
            'fields': ('title', 'isbn', 'category', 'publisher', 'summary')
        }),
        ('Availability', {
            'fields': ('total_copies', 'available_copies')
        }),
        ('Additional Info', {
            'fields': ('publication_date', 'language', 'page_count', 'cover_image')
        }),
    )
    inlines = [AuthorInline]
    search_fields = ('title', 'isbn', 'authors__name')

    def display_authors(self, obj):
        return ", ".join([author.name for author in obj.authors.all()[:3]])