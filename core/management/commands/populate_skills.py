# management/commands/populate_skills.py
from django.core.management.base import BaseCommand
from core.models import Skill

class Command(BaseCommand):
    help = 'Populate the Skill model with common skills'

    def handle(self, *args, **kwargs):
        skills = [
            # Programming Languages
            ('Python', 'Programming Language'),
            ('JavaScript', 'Programming Language'),
            ('Java', 'Programming Language'),
            ('C++', 'Programming Language'),
            ('TypeScript', 'Programming Language'),
            ('PHP', 'Programming Language'),
            ('Ruby', 'Programming Language'),
            ('Go', 'Programming Language'),
            ('Swift', 'Programming Language'),
            ('Kotlin', 'Programming Language'),
            
            # Frameworks
            ('Django', 'Web Framework'),
            ('React', 'Frontend Framework'),
            ('Node.js', 'Backend Framework'),
            ('Angular', 'Frontend Framework'),
            ('Vue.js', 'Frontend Framework'),
            ('Flask', 'Web Framework'),
            ('Spring Boot', 'Web Framework'),
            ('Laravel', 'Web Framework'),
            
            # Databases
            ('PostgreSQL', 'Database'),
            ('MySQL', 'Database'),
            ('MongoDB', 'Database'),
            ('Redis', 'Database'),
            ('SQL Server', 'Database'),
            ('Oracle', 'Database'),
            ('SQLite', 'Database'),
            
            # DevOps/Tools
            ('Docker', 'DevOps'),
            ('Kubernetes', 'DevOps'),
            ('AWS', 'Cloud Platform'),
            ('Azure', 'Cloud Platform'),
            ('Google Cloud', 'Cloud Platform'),
            ('Git', 'Version Control'),
            ('Jenkins', 'CI/CD'),
            ('GitHub Actions', 'CI/CD'),
            ('Terraform', 'Infrastructure as Code'),
            
            # Administrative Skills - Office Management
            ('Microsoft Office Suite', 'Administrative'),
            ('Microsoft Excel', 'Administrative'),
            ('Microsoft Word', 'Administrative'),
            ('Microsoft PowerPoint', 'Administrative'),
            ('Google Workspace', 'Administrative'),
            ('Data Entry', 'Administrative'),
            ('File Management', 'Administrative'),
            ('Document Preparation', 'Administrative'),
            ('Records Management', 'Administrative'),
            ('Office Administration', 'Administrative'),
            
            # Administrative Skills - Communication
            ('Email Management', 'Administrative'),
            ('Business Correspondence', 'Administrative'),
            ('Customer Service', 'Administrative'),
            ('Client Relations', 'Administrative'),
            
            # Administrative Skills - Scheduling & Organization
            ('Calendar Management', 'Administrative'),
            ('Appointment Scheduling', 'Administrative'),
            ('Travel Arrangements', 'Administrative'),
            ('Event Planning', 'Administrative'),
            ('Meeting Coordination', 'Administrative'),
            ('Time Management', 'Administrative'),
            ('Multitasking', 'Administrative'),
            ('Priority Management', 'Administrative'),

            
            # Administrative Skills - Specialized
            ('Typing', 'Administrative'),
            ('Transcription', 'Administrative'),
            ('Proofreading', 'Administrative'),
            ('Report Writing', 'Administrative'),
            ('Presentation Skills', 'Administrative'),
            ('Database Management', 'Administrative'),
            ('CRM Software', 'Administrative'),
            ('Salesforce', 'Administrative'),
            ('SharePoint', 'Administrative'),
            ('Slack', 'Administrative'),
            ('Zoom', 'Administrative'),
            ('Microsoft Teams', 'Administrative'),
            
            # Administrative Skills - HR Related
            ('Onboarding', 'Administrative'),
            ('Employee Records Management', 'Administrative'),
            ('Recruitment Support', 'Administrative'),
            ('Policy Documentation', 'Administrative'),
            
            # Soft Skills
            ('Team Leadership', 'Soft Skill'),
            ('Communication', 'Soft Skill'),
            ('Problem Solving', 'Soft Skill'),
            ('Project Management', 'Soft Skill'),
            ('Critical Thinking', 'Soft Skill'),
            ('Attention to Detail', 'Soft Skill'),
            ('Teamwork', 'Soft Skill'),
            ('Adaptability', 'Soft Skill'),
            ('Conflict Resolution', 'Soft Skill'),
            ('Decision Making', 'Soft Skill'),
            ('Organizational Skills', 'Soft Skill'),
            ('Interpersonal Skills', 'Soft Skill'),
            
            # Marketing & Sales
            ('Digital Marketing', 'Marketing'),
            ('SEO', 'Marketing'),
            ('Content Marketing', 'Marketing'),
            ('Social Media Marketing', 'Marketing'),
            ('Email Marketing', 'Marketing'),
            ('Sales', 'Sales'),
            
            # Design
            ('Adobe Photoshop', 'Design'),
            ('Adobe Illustrator', 'Design'),
            ('Figma', 'Design'),
            ('UI/UX Design', 'Design'),
            ('Graphic Design', 'Design'),
            
            # Data & Analytics
            ('Data Analysis', 'Data & Analytics'),
            ('Excel Advanced', 'Data & Analytics'),
            ('Power BI', 'Data & Analytics'),
            ('Tableau', 'Data & Analytics'),
            ('SQL', 'Data & Analytics'),
            ('Statistics', 'Data & Analytics'),
        ]

        created_count = 0
        existing_count = 0

        for skill_name, category in skills:
            skill, created = Skill.objects.get_or_create(
                name=skill_name,
                defaults={'category': category}
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created skill: {skill_name} ({category})')
                )
            else:
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(f'○ Already exists: {skill_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n{"="*50}\n'
                f'Summary:\n'
                f'  Created: {created_count} new skills\n'
                f'  Existing: {existing_count} skills\n'
                f'  Total: {created_count + existing_count} skills\n'
                f'{"="*50}'
            )
        )