from django.db import models
from django.utils import timezone
from catalog.models import Book
from members.models import Member

# Create your models here.
class Borrowing(models.Model):
    STATUS_CHOICES = (
        ("BORROWING", "Đang mượn"),
        ("RETURNED", "Đã trả"),
        ("OVERDUE", "Quá hạn"),
        ("LOST", "Mất sách")
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings", verbose_name="Tên sách")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="borrowings", verbose_name="Người mượn")
    borrow_date = models.DateField(default=timezone.now, verbose_name="Ngày mượn")
    due_date = models.DateField(verbose_name="Ngày hẹn trả")
    return_date = models.DateField(blank=True, null=True, verbose_name="Ngày trả thực tế")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="BORROWING", verbose_name="Trạng thái")
    note = models.TextField(blank=True, null=True, verbose_name="Ghi chú")

    class Meta:
        ordering = ["-borrow_date"]
        verbose_name = verbose_name_plural = "Mượn sách"

    def __str__(self):
        return f"{self.borrow_date} - {self.member.user.get_full_name()} - {self.book.title}"
    
    
    def save(self, *args, **kwargs):
        # Cập nhật số lượng sách có sẵn khi lưu bản ghi có người mượn
        if not self.pk:  # Nếu đây là bản ghi mới (sách đã có người mượn)
            self.book.available_copies -= 1
            self.book.save()
        elif self.status == "RETURNED" and not self.return_date: # Nếu sách được trả (nếu muốn bỏ cái vụ not kia thì phải cài trigger ở DB)
            self.book.available_copies += 1
            self.book.save()
            self.return_date = timezone.now().date()

        # Kiểm tra có trả quá hạn không
        if self.is_overdue():
            self.status = "OVERDUE"

        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        return self.status == "BORROWING" and self.due_date < timezone.now().date()
    
class Reservation(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Đang chờ'),
        ('FULFILLED', 'Đã thực hiện'),
        ('CANCELLED', 'Đã hủy'),
        ('EXPIRED', 'Hết hạn'),
    )
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations', verbose_name="Tên sách")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='reservations', verbose_name="Người đặt trước")
    reservation_date = models.DateField(default=timezone.now, verbose_name="Ngày đặt")
    expiry_date = models.DateField(verbose_name="Ngày hết hạn")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING', verbose_name="Trạng thái")
    
    class Meta:
        ordering = ['-reservation_date']
        verbose_name = verbose_name_plural = "Đặt trước"
    
    def __str__(self):
        return f"{self.reservation_date} - {self.member.user.get_full_name()} - {self.book.title}"
    
    @property
    def is_expired(self):
        return self.expiry_date < timezone.now().date()