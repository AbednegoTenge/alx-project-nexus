from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True # Abstract base class (no table)


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        EMPLOYER = 'EMPLOYER', _('Employer')
        CANDIDATE = 'CANDIDATE', _('Candidate')

    username = None
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CANDIDATE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def is_employer(self):
        return self.role == self.Role.EMPLOYER
    
    @property
    def is_candidate(self):
        return self.role == self.Role.CANDIDATE

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN


