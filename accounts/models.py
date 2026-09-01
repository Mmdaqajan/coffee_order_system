from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ("admin", "مدیر"),
        ("barista", "باریستا"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="کاربر",
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="barista",
        verbose_name="نقش",
    )

    class Meta:
        verbose_name = "پروفایل کاربر"
        verbose_name_plural = "پروفایل‌های کاربران"

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"