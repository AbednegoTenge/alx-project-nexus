from cryptography.hazmat.primitives.ciphers.algorithms import Camellia
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, ValidationError
from django.utils.text import slugify
from .static_backend import PublicMediaStorage, PrivateMediaStorage

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
    phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=20, choices=Gender.choices, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    # Professional info
    headline = models.CharField(max_length=255, blank=True, help_text='e.g Senior Software Engineer')
    about = models.TextField(blank=True, help_text='Tell us about yourself')
    # Social links
    linkedin = models.URLField(blank=True, help_text='Your LinkedIn profile URL')
    github = models.URLField(blank=True, help_text='Your GitHub profile URL')
    twitter = models.URLField(blank=True, help_text='Your Twitter profile URL')
    website = models.URLField(blank=True, help_text='Your website URL')
    # Media links
    profile_picture = models.ImageField(storage=PublicMediaStorage, upload_to='profiles/pictures', blank=True, null=True)
    resume = models.FileField(storage=PrivateMediaStorage, upload_to='profiles/resumes', blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    @property
    def verified(self):
        return self.is_verified

    class Meta:
        verbose_name = _('Candidate Profile')
        verbose_name_plural = _('Candidate Profiles')

    def get_profile_completion_percentage(self):
        """
        Calculate profile completion percentage based on filled fields
        Returns: int (0-100)
        """
        # Define all fields that contribute to profile completion (equal weight)
        profile_fields = [
            ('first_name', self.user.first_name),
            ('last_name', self.user.last_name),
            ('phone', self.phone),
            ('gender', self.gender),
            ('date_of_birth', self.date_of_birth),
            ('headline', self.headline),
            ('about', self.about),
            ('linkedin', self.linkedin),
            ('github', self.github),
            ('twitter', self.twitter),
            ('website', self.website),
            ('profile_picture', self.profile_picture),
            ('resume', self.resume),
        ]
        
        # Count filled fields
        total_fields = len(profile_fields)
        filled_fields = sum(1 for field_name, field_value in profile_fields if field_value)
        
        percentage = (filled_fields / total_fields) * 100
        return round(percentage)

    @property
    def is_profile_complete(self):
        """
        Check if profile completion meets minimum threshold
        Returns: bool
        """

        return self.get_profile_completion_percentage() == 100
    

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.headline}"


class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

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
    field_of_study = models.CharField(max_length=255, blank=True)
    institution = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)


    class Meta:
        verbose_name = _('Education')
        verbose_name_plural = _('Educations')

    def __str__(self):
        return f"{self.level} in {self.field_of_study} - {self.institution}"    


class Skill(BaseModel):
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
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='candidate_skills')

    class Meta:
        verbose_name = _('Candidate Skill')
        verbose_name_plural = _('Candidate Skills')
        unique_together = ('candidate', 'skill')

    def __str__(self):
        return f"{self.candidate.user.get_full_name()} - {self.skill.name}"


class Certification(BaseModel):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    credential_url = models.URLField(blank=True)
    credential_id = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = _('Certification')
        verbose_name_plural = _('Certifications')

    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"


class EmployerProfile(BaseModel):
    class CompanySize(models.TextChoices):
        SMALL = '1-10', _('1-10 employees')
        MEDIUM = '11-50', _('11-50 employees')
        LARGE = '51-200', _('51-200 employees')
        ENTERPRISE = '201-500', _('201-500 employees')
        CORPORATE = '500+', _('500+ employees')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=200)
    company_size = models.CharField(max_length=20, choices=CompanySize.choices, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    founded_year = models.IntegerField(null=True, blank=True) # remove
    
    # Company Info
    description = models.TextField(blank=True)
    website_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    # Media
    logo = models.ImageField(storage=PublicMediaStorage, upload_to='companies/logos/', null=True, blank=True)
    cover_image = models.ImageField(storage=PublicMediaStorage, upload_to='companies/covers/', null=True, blank=True)
    
    # Contact
    headquarters_address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    
    # Verification``
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Employer Profile'
        verbose_name_plural = 'Employer Profiles'

    def verified(self):
        return self.is_verified

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.company_name}"


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='subcategories'
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name


class JobPosting(BaseModel):
    class EmploymentType(models.TextChoices):
        FULL_TIME = 'FULL_TIME', _('Full-time')
        PART_TIME = 'PART_TIME', _('Part-time')
        CONTRACT = 'CONTRACT', _('Contract')
        INTERNSHIP = 'INTERNSHIP', _('Internship')
        FREELANCE = 'FREELANCE', _('Freelance')

    class LocationType(models.TextChoices):
        REMOTE = 'REMOTE', _('Remote')
        ON_SITE = 'ON_SITE', _('On-site')
        HYBRID = 'HYBRID', _('Hybrid')
    
    class ExperienceLevel(models.TextChoices):
        ENTRY = 'ENTRY', _('Entry Level')
        INTERMEDIATE = 'INTERMEDIATE', _('Intermediate')
        SENIOR = 'SENIOR', _('Senior')
        LEAD = 'LEAD', _('Lead')
        EXECUTIVE = 'EXECUTIVE', _('Executive')

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Draft')
        ACTIVE = 'ACTIVE', _('Active')
        CLOSED = 'CLOSED', _('Closed')
        EXPIRED = 'EXPIRED', _('Expired')

    employer = models.ForeignKey(
        EmployerProfile, 
        on_delete=models.CASCADE, 
        related_name='job_postings'
    )
    posted_by = models.ForeignKey(EmployerProfile, on_delete=models.SET_NULL, null=True, related_name='posted_jobs')
    
    # Job Details
    title = models.CharField(max_length=200)
    description = models.TextField()
    responsibilities = models.JSONField(default=list, blank=True)
    requirements = models.JSONField(default=list, blank=True)
    nice_to_have = models.JSONField(default=list, blank=True)
    benefits = models.JSONField(default=list, blank=True)
    
    # Job Type
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices)
    job_type = models.CharField(max_length=20, choices=LocationType.choices)
    experience_level = models.CharField(max_length=20, choices=ExperienceLevel.choices)
    
    # Salary
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField(max_length=3, default='USD')
    is_salary_disclosed = models.BooleanField(default=False)
    
    # Location
    location = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Categories
    categories = models.ManyToManyField(Category, related_name='jobs', blank=True)
    
    # Skills
    required_skills = models.ManyToManyField(
        Skill, 
        through='JobSkill', 
        related_name='required_for_jobs'
    )
    
    # Other Details
    application_deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    
    # Metrics
    applications_count = models.IntegerField(default=0)
    
    # Dates
    posted_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Job Posting'
        verbose_name_plural = 'Job Postings'
        ordering = ['-posted_at']
        indexes = [
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['job_type', 'experience_level']),
            models.Index(fields=['city', 'country']),
        ]


    def clean(self):
        if self.salary_min and self.salary_max:
            if self.salary_max < self.salary_min:
                raise ValidationError("Maximum salary cannot be less than minimum salary.")

    def __str__(self):
        return f"{self.title} - {self.employer.company_name}"

class JobSkill(BaseModel):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='job_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    is_required = models.BooleanField(default=True)
    minimum_years = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Job Skill'
        verbose_name_plural = 'Job Skills'
        unique_together = ['job', 'skill']

    def __str__(self):
        req_type = "Required" if self.is_required else "Nice to have"
        return f"{self.job.title} - {self.skill.name} ({req_type})"


# ==================== APPLICATION MODELS ====================

class Application(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        REVIEWED = 'REVIEWED', _('Reviewed')
        SHORTLISTED = 'SHORTLISTED', _('Shortlisted')
        INTERVIEW = 'INTERVIEW', _('Interview Scheduled')
        REJECTED = 'REJECTED', _('Rejected')
        ACCEPTED = 'ACCEPTED', _('Accepted')
        WITHDRAWN = 'WITHDRAWN', _('Withdrawn')

    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications')
    
    # Application Data
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(storage=PrivateMediaStorage, upload_to='applications/resumes/', null=True, blank=True)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available_from = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    is_withdrawn = models.BooleanField(default=False)
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        ordering = ['-applied_at']
        unique_together = ['job', 'candidate']
        indexes = [
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['job', 'status']),
        ]

    def __str__(self):
        return f"{self.candidate.user.get_full_name()} -> {self.job.title}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Update job application count
        if is_new:
            self.job.applications_count = self.job.applications.filter(is_active=True).count()
            self.job.save(update_fields=['applications_count'])


class ApplicationStatusHistory(BaseModel):
    application = models.ForeignKey(
        Application, 
        on_delete=models.CASCADE, 
        related_name='status_history'
    )
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Application Status History'
        verbose_name_plural = 'Application Status Histories'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.application} - {self.old_status} -> {self.new_status}"


class SavedJob(BaseModel):
    candidate = models.ForeignKey(
        CandidateProfile, 
        on_delete=models.CASCADE, 
        related_name='saved_jobs'
    )
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='saved_by')
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Saved Job'
        verbose_name_plural = 'Saved Jobs'
        unique_together = ['candidate', 'job']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.candidate.user.get_full_name()} saved {self.job.title}"


class JobAlert(BaseModel):
    class Frequency(models.TextChoices):
        INSTANT = 'INSTANT', _('Instant')
        DAILY = 'DAILY', _('Daily')
        WEEKLY = 'WEEKLY', _('Weekly')

    candidate = models.ForeignKey(
        CandidateProfile, 
        on_delete=models.CASCADE, 
        related_name='job_alerts'
    )
    alert_name = models.CharField(max_length=200)
    keywords = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    job_type = models.CharField(max_length=20, blank=True)
    experience_level = models.CharField(max_length=20, blank=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_remote = models.BooleanField(default=False)
    frequency = models.CharField(max_length=20, choices=Frequency.choices, default=Frequency.DAILY)

    class Meta:
        verbose_name = 'Job Alert'
        verbose_name_plural = 'Job Alerts'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.candidate.user.get_full_name()} - {self.alert_name}"

class JobNotification(BaseModel):
    """Track which job postings have been sent to which candidates"""
    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name='job_notifications'
    )
    job_posting = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Job Notification'
        verbose_name_plural = 'Job Notifications'
        unique_together = ['candidate', 'job_posting']
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['candidate']),
            models.Index(fields=['job_posting']),
            models.Index(fields=['sent_at']),
        ]
    
    def __str__(self):
        return f"{self.candidate.user.get_full_name()} - {self.job_posting.title}"


class CompanyReview(BaseModel):
    company = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_reviews')
    
    # Review Content
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField()

    class Meta:
        verbose_name = 'Company Review'
        verbose_name_plural = 'Company Reviews'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company.company_name} - {self.rating} stars"


class Notification(BaseModel):
    class NotificationType(models.TextChoices):
        APPLICATION_STATUS = 'APPLICATION_STATUS', _('Application Status Update')
        NEW_MESSAGE = 'NEW_MESSAGE', _('New Message')
        JOB_ALERT = 'JOB_ALERT', _('Job Alert')
        INTERVIEW = 'INTERVIEW', _('Interview Scheduled')
        SYSTEM = 'SYSTEM', _('System Notification')
        APPLICATION = 'APPLICATION', _('Application')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices)
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # Reference to related object
    reference_id = models.IntegerField(null=True, blank=True)
    reference_type = models.CharField(max_length=50, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.title}"

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = models.functions.Now()
            self.save(update_fields=['is_read', 'read_at'])