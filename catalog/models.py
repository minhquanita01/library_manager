from django.db import models
from django.urls import reverse

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên tác giả")
    biography = models.TextField(blank=True, null=True, verbose_name="Tiểu sử")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Ngày sinh")
    date_of_death = models.DateField(blank=True, null=True, verbose_name="Ngày mất")
    
    class Meta:
        ordering = ["name"]
        verbose_name = verbose_name_plural = "Tác giả"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse(viewname="author-detail", args=[str(self.id)])
    
class BookCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên thể loại")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")

    class Meta:
        ordering = ["name"]
        verbose_name = verbose_name_plural = "Thể loại"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse(viewname="category-detail", args=[str(self.id)])
    
class Publisher(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên nhà xuất bản")
    address = models.TextField(blank=True, null=True, verbose_name="Địa chỉ")
    website = models.URLField(blank=True, null=True, verbose_name="Website")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    
    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = "Nhà xuất bản"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('publisher-detail', args=[str(self.id)])

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tên sách")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    author = models.ManyToManyField(Author, related_name="books", verbose_name="Tác giả")
    category = models.ForeignKey(BookCategory, on_delete=models.SET_NULL, null=True, related_name="books", verbose_name="Thể loại")
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name="books", verbose_name="Nhà xuất bản")
    publication_date = models.DateField(blank=True, null=True, verbose_name="Ngày xuất bản")
    summary = models.TextField(blank=True, null=True, verbose_name="Tóm tắt")
    total_copies = models.PositiveIntegerField(default=1, verbose_name="Tổng số bản")
    available_copies = models.PositiveIntegerField(default=1, verbose_name="Số bản có sẵn")
    language = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ngôn ngữ")
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name="Ảnh bìa")
    page_count = models.PositiveIntegerField(blank=True, null=True, verbose_name="Số trang")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        ordering = ['title']
        verbose_name = verbose_name_plural = "Sách"
    
    def __str__(self):
        return self.title
    
    @property
    def is_available(self):
        return self.available_copies > 0
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])