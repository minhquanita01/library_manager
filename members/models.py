from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import uuid

# Create your models here.
class Member(models.Model):
    MEMBERSHIP_TYPES = (
        ('STANDARD', 'Tiêu chuẩn'),
        ('PREMIUM', 'Cao cấp'),
        ('STUDENT', 'Sinh viên'),
        ('SENIOR', 'Người cao tuổi'),
    )

    GENDER_CHOICES = (
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('O', 'Khác'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="member_profiles", verbose_name="Người dùng")
    membership_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="Mã thành viên")
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_TYPES, default="STANDARD", verbose_name="Loại thành viên")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Ngày sinh")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True, verbose_name="Giới tính")
    address = models.TextField(blank=True, null=True, verbose_name="Địa chỉ")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Số điện thoại")
    profile_picture = models.ImageField(upload_to="members/", blank=True, null=True, verbose_name="Ảnh đại diện")
    registration_date = models.DateField(auto_now_add=True, verbose_name="Ngày đăng ký")
    expiry_date = models.DateField(verbose_name="Ngày hết hạn")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")

    class Meta:
        ordering = ["user__last_name", "user__first_name"]
        verbose_name = verbose_name_plural = "Độc giả"

    def __str__(self):
        return f"{self.membership_id} - {self.user.get_full_name()}"
    
    @property
    def is_expired(self):
        return self.expiry_date < timezone.now().date()
    
    def get_absolute_url(self):
        return reverse("member-detail", args=[str(self.id)])