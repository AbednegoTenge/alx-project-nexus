from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, CandidateProfile, Application, JobPosting, 
    EmployerProfile, SavedJob, CandidateSkill, Education, 
    Certification, Notification, Address
)
from .forms import UserChangeForm, UserCreationForm

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "first_name", "last_name", "is_active")
    list_filter = ("is_staff", "is_active")

    fieldsets = (
        (None, {"fields": ("email", "first_name", "last_name", "password", "is_active", "role")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "is_active", "password1", "password2", "role"),
        }),
    )

    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(CandidateProfile)
admin.site.register(Application)
admin.site.register(JobPosting)
admin.site.register(EmployerProfile)
admin.site.register(SavedJob)
admin.site.register(CandidateSkill)
admin.site.register(Education)
admin.site.register(Certification)
admin.site.register(Notification)
admin.site.register(Address)

