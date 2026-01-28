from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CandidateProfile, EmployerProfile, Address, Notification, Application
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


@receiver(post_save, sender=Application)
def send_employer_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.job.employer.user,
            title=f"New Application for {instance.job.title}",
            notification_type=Notification.NotificationType.APPLICATION,
            content=f"{instance.candidate.user.get_full_name()} has applied for the position of {instance.job.title}.",
        )

@receiver(post_save, sender=Application)
def send_candidate_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.candidate.user,
            title=f"Application for {instance.job.title} has been submitted",
            notification_type=Notification.NotificationType.APPLICATION,
            content=f"You have successfully applied for the position of {instance.job.title} at {instance.job.employer.company_name}.",
        )