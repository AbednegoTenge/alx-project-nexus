from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


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

    objects = UserManager()

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


class CandidateProfile(BaseModel):
    class Gender(models.TextChoices):
        MALE = 'MALE', _('Male')
        FEMALE = 'FEMALE', _('Female')
        OTHER = 'OTHER', _('Other')
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate')
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=20, choices=Gender.choices, blank=True)
    date_of_birth = models.DateField()
    # Professional info
    headline = models.CharField(max_length=255, blank=True, help_text='e.g Senior Software Engineer')
    about = models.TextField(blank=True, help_text='Tell us about yourself')
    # Social links
    linkedin = models.URLField(blank=True, help_text='Your LinkedIn profile URL')
    github = models.URLField(blank=True, help_text='Your GitHub profile URL')
    twitter = models.URLField(blank=True, help_text='Your Twitter profile URL')
    website = models.URLField(blank=True, help_text='Your website URL')
    # Media links
    profile_picture = models.ImageField(upload_to='profiles/pictures', blank=True, null=True)
    resume = models.FileField(upload_to='profiles/resumes', blank=True, null=True)     

    class Meta:
        verbose_name = _('Candidate Profile')
        verbose_name_plural = _('Candidate Profiles')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.headline}"


class Address(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.city}, {self.state}, {self.country}"


class Education(BaseModel):
    class Level(models.TextChoices):
        HIGH_SCHOOL = 'HIGH_SCHOOL', _('High School')
        ASSOCIATE = 'ASSOCIATE', _('Associate Degree')
        BACHELOR = 'BACHELOR', _('Bachelor\'s Degree')
        MASTER = 'MASTER', _('Master\'s Degree')
        PHD = 'PHD', _('PhD')
        CERTIFICATE = 'CERTIFICATE', _('Certificate')
        DIPLOMA = 'DIPLOMA', _('Diploma')
    
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='education')
    level = models.CharField(max_length=20, choices=Level.choices, default=Level.HIGH_SCHOOL)
    field_of_study = models.CharField(max_length=255)
    institution = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)


    class Meta:
        verbose_name = _('Education')
        verbose_name_plural = _('Educations')

    def __str__(self):
        return f"{self.level} in {self.field_of_study} - {self.institution}"    


class Skills(BaseModel):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')

    def __str__(self):
        return self.name    


class CandidateSkill(BaseModel):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='candidate_skills')
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE, related_name='candidate_skills')

    class Meta:
        verbose_name = _('Candidate Skill')
        verbose_name_plural = _('Candidate Skills')

    def __str__(self):
        return f"{self.candidate.user.get_full_name()} - {self.skill.name}"


class Certification(BaseModel):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_url = models.URLField(blank=True)
    credential_id = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = _('Certification')
        verbose_name_plural = _('Certifications')

    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"