from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CandidateProfile, EmployerProfile, Address
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_candidate_or_employer_profile(sender, instance, created, **kwargs):
    if created and instance.is_candidate:
        CandidateProfile.objects.get_or_create(user=instance)
        Address.objects.get_or_create(user=instance)
    elif created and instance.is_employer:
        EmployerProfile.objects.get_or_create(user=instance)
        Address.objects.get_or_create(user=instance)
