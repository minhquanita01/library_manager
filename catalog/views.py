from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Book, Author, BookCategory, Publisher

# Create your views here.
def index(request):
    """View function cho trang chủ của trang web"""

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()
    num_categories = BookCategory.objects.all().count()
    num_publishers = Publisher.objects.all().count()

    # Số lượng sách có sẵn
    num_available_books = Book.objects.filter(available_copies__gt = 0).count()

    context = {
        "num_books": num_books,
        "num_authors": num_authors,
        "num_categories": num_categories,
        "num_publishers": num_publishers,
        "num_available_books": num_available_books,
    }

    return render(request, "catalog/index.html", context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    template_name = "catalog/book_list.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Book.objects.filter(
                Q(title__icontains = query) |
                Q(author__name__icontains = query) |
                Q(isbn__icontains = query)
            ).distinct()
        return Book.objects.all()
    
class BookDetailView(generic.DetailView):
    model = Book
    template_name = "catalog/book_detail.html"

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
    template_name = "catalog/author_list.html"

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "catalog/author_detail.html"

class BookCategoryListView(generic.ListView):
    model = BookCategory
    template_name = "catalog/book_category_list.html"

class BookCategoryDetailView(generic.DetailView):
    model = BookCategory
    template_name = "catalog/book_category_detail.html"

class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Book
    fields = ["title", "isbn", "authors", "category", "publisher", "publication_date", 
              "summary", "total_copies", "available_copies", "language", "cover_image", "page_count"]
    permission_required = "catalog.add_book"
    template_name = "catalog/book_form.html"

class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Book
    fields = ["title", "isbn", "authors", "category", "publisher", "publication_date", 
              "summary", "total_copies", "available_copies", "language", "cover_image", "page_count"]
    permission_required = "catalog.change_book"
    template_name = "catalog/book_form.html"

class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Book
    success_url = reverse_lazy("books")
    permission_required = "catalog.delete_book"
    template_name = "catalog/book_confirm_delete.html"