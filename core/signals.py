from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    CandidateProfile, EmployerProfile, Address, 
    Notification, Application, JobPosting, JobNotification
)
from django.contrib.auth import get_user_model
from .utils import send_email
import logging

logger = logging.getLogger(__name__)

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


@receiver(post_save, sender=JobPosting)
def send_automatic_job_notifications(sender, instance, created, **kwargs):
    """
    Automatically send job notifications to matching candidates when a new job is posted.
    Matches candidates based on their skills (skill-based matching).
    """
    if not created:
        return  # Only send notifications for new job postings
    
    # Only send notifications for active jobs
    if instance.status != JobPosting.Status.ACTIVE:
        logger.info(f"Job {instance.title} is not active, skipping automatic notifications")
        return
    
    # Get all required skills for this job
    required_skill_ids = instance.job_skills.filter(
        is_required=True
    ).values_list('skill_id', flat=True)
    
    if not required_skill_ids:
        logger.info(f"No required skills for job {instance.title}, skipping skill-based matching")
        return
    
    # Find candidates who have at least one of the required skills
    matching_candidates = CandidateProfile.objects.filter(
        candidate_skills__skill_id__in=required_skill_ids,
        user__is_active=True  # Only send to active users
    ).distinct()
    
    logger.info(f"Found {matching_candidates.count()} skill-matching candidates for {instance.title}")
    
    for candidate in matching_candidates:
        # Create job notification record
        notification, notification_created = JobNotification.objects.get_or_create(
            candidate=candidate,
            job_posting=instance,
            defaults={'source': 'SKILL_MATCH'}
        )
        
        if not notification_created:
            logger.info(f"Notification already exists for {candidate.user.email}")
            continue
        
        # Get matching skills for personalization
        candidate_skill_ids = candidate.candidate_skills.values_list('skill_id', flat=True)
        matching_skills = instance.job_skills.filter(
            skill_id__in=candidate_skill_ids
        ).select_related('skill')
        
        matching_skill_names = [js.skill.name for js in matching_skills]
        
        # Prepare email content
        subject = f"New Job Match: {instance.title}"
        
        body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .skills {{ background-color: #e8f5e9; padding: 10px; margin: 10px 0; border-radius: 5px; }}
                .button {{ 
                    display: inline-block; 
                    padding: 12px 24px; 
                    background-color: #4CAF50; 
                    color: white; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    margin-top: 15px;
                }}
                .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>New Job Match!</h1>
                </div>
                <div class="content">
                    <h2>{instance.title}</h2>
                    <p><strong>Company:</strong> {instance.company.name if hasattr(instance, 'company') else 'N/A'}</p>
                    <p><strong>Location:</strong> {instance.location if hasattr(instance, 'location') else 'N/A'}</p>
                    
                    <div class="skills">
                        <strong>Your Matching Skills:</strong>
                        <ul>
                            {"".join([f"<li>{skill}</li>" for skill in matching_skill_names])}
                        </ul>
                    </div>
                    
                    <p>{instance.description[:200] if hasattr(instance, 'description') else ''}...</p>
                    
                    <a href="{instance.get_absolute_url()}" class="button">View Job Details</a>
                </div>
                <div class="footer">
                    <p>You're receiving this because your skills match this job.</p>
                    <p>To stop receiving alerts, update your preferences.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Send email
        email_sent = send_email(
            email_address=candidate.user.email,
            subject=subject,
            body=body,
            html=True
        )
        
        if email_sent:
            logger.info(f"Alert sent to {candidate.user.email} for job {instance.title}")
        else:
            logger.error(f"Failed to send alert to {candidate.user.email} for job {instance.title}")

