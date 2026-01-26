from django.contrib import admin
from .models import User, CandidateProfile, Application, JobPosting, EmployerProfile, SavedJob, CandidateSkill, Education, Certification, Notification

# Register your models here.
admin.site.register(User)
admin.site.register(CandidateProfile)
admin.site.register(Application)
admin.site.register(JobPosting)
admin.site.register(EmployerProfile)
admin.site.register(SavedJob)
admin.site.register(CandidateSkill)
admin.site.register(Education)
admin.site.register(Certification)
admin.site.register(Notification)

