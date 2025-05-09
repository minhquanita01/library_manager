from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Staff(models.Model):
    ROLE_CHOICES = (
        ('LIBRARIAN', 'Thủ thư'),
        ('ADMIN', 'Quản trị'),
        ('ASSISTANT', 'Trợ lý'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_profile", verbose_name="Nhân viên")
    staff_id = models.CharField(max_length=20, unique=True, verbose_name="Mã nhân viên")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ASSISTANT', verbose_name="Vai trò")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Ngày sinh")
    address = models.TextField(blank=True, null=True, verbose_name="Địa chỉ")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Số điện thoại")
    hiring_date = models.DateField(default=timezone.now, verbose_name="Ngày vào làm")

    class Meta:
        ordering = ['user__last_name', 'user__first_name']
        verbose_name = verbose_name_plural = "Nhân viên"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role}"