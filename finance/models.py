from django.db import models
from django.utils import timezone
from members.models import Member
from circulation.models import Borrowing
from staff.models import Staff
import uuid

# Create your models here.
class Fine(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='fines', verbose_name="Độc giả")
    borrowing = models.ForeignKey(Borrowing, on_delete=models.SET_NULL, null=True, blank=True, related_name='fines', verbose_name="Giao dịch mượn")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Số tiền")
    reason = models.CharField(max_length=200, verbose_name="Lý do")
    date_issued = models.DateField(default=timezone.now, verbose_name="Ngày phạt")
    is_paid = models.BooleanField(default=False, verbose_name="Đã thanh toán")
    payment_date = models.DateField(blank=True, null=True, verbose_name="Ngày thanh toán")
    
    class Meta:
        ordering = ['-date_issued']
        verbose_name = verbose_name_plural = "Phạt"
    
    def __str__(self):
        return f"{self.member.user.get_full_name()} - {self.amount} - {self.reason}"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('PAYMENT', 'Thanh toán'),
        ('REFUND', 'Hoàn tiền'),
        ('DEPOSIT', 'Đặt cọc'),
    )
    
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="Mã giao dịch")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='transactions', verbose_name="Độc giả")
    fine = models.ForeignKey(Fine, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions', verbose_name="Tiền phạt")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Số tiền")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, verbose_name="Loại giao dịch")
    date = models.DateTimeField(default=timezone.now, verbose_name="Ngày giao dịch")
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions', verbose_name="Nhân viên xử lý")
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú")
    
    class Meta:
        ordering = ['-date']
        verbose_name = verbose_name_plural = "Giao dịch"
    
    def __str__(self):
        return f"{self.transaction_id} - {self.member.user.get_full_name()} - {self.amount}"