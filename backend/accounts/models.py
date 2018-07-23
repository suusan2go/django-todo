from django.contrib.auth.models import AbstractUser
from django import forms
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    email = models.CharField(
        max_length=150,
        unique=True,
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            '同じメールアドレスが既に登録済みです。'
        )
