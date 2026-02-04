# management/commands/populate_categories.py
from django.core.management.base import BaseCommand
from core.models import Category

class Command(BaseCommand):
    help = 'Populate the Category model with parent and child categories'

    def handle(self, *args, **kwargs):
        # Define parent categories with their metadata
        parent_categories = [
            ('Technology & IT', 'Jobs related to software development, IT infrastructure, and technology'),
            ('Design & Creative', 'Creative roles in design, media, and visual arts'),
            ('Marketing & Sales', 'Marketing, advertising, sales, and business development roles'),
            ('Administrative & Office', 'Office administration, clerical, and support roles'),
            ('Human Resources', 'HR, recruitment, training, and employee management'),
            ('Finance & Accounting', 'Financial services, accounting, and bookkeeping'),
            ('Customer Service', 'Customer support and client relations'),
            ('Healthcare', 'Medical, nursing, and healthcare services'),
            ('Education & Training', 'Teaching, training, and educational services'),
            ('Engineering', 'Engineering disciplines and technical roles'),
            ('Legal', 'Legal services and compliance'),
            ('Operations & Logistics', 'Operations management, supply chain, and logistics'),
            ('Management', 'Leadership and management positions'),
            ('Writing & Content', 'Writing, editing, and content creation'),
            ('Consulting', 'Business and professional consulting services'),
            ('Real Estate', 'Real estate and property management'),
            ('Hospitality & Tourism', 'Hotels, events, and tourism services'),
            ('Research & Science', 'Scientific research and laboratory work'),
            ('Trades & Services', 'Skilled trades and technical services'),
            ('Non-Profit & Social Services', 'Social work and community services'),
        ]
        
        # Define subcategories: (child_name, parent_name, description)
        subcategories = [
            # Technology & IT subcategories
            ('Software Development', 'Technology & IT', 'Software engineering and application development'),
            ('Web Development', 'Technology & IT', 'Frontend, backend, and full-stack web development'),
            ('Mobile Development', 'Technology & IT', 'iOS, Android, and cross-platform mobile apps'),
            ('DevOps & Cloud', 'Technology & IT', 'Cloud infrastructure, CI/CD, and DevOps practices'),
            ('Data Science & Analytics', 'Technology & IT', 'Data analysis, machine learning, and AI'),
            ('Database Administration', 'Technology & IT', 'Database management and optimization'),
            ('Network Engineering', 'Technology & IT', 'Network infrastructure and administration'),
            ('Cybersecurity', 'Technology & IT', 'Information security and cybersecurity'),
            ('IT Support', 'Technology & IT', 'Technical support and help desk services'),
            ('Systems Administration', 'Technology & IT', 'Server and systems management'),
            ('Quality Assurance', 'Technology & IT', 'Software testing and quality control'),
            ('Technical Writing', 'Technology & IT', 'Documentation and technical communication'),
            
            # Design & Creative subcategories
            ('Graphic Design', 'Design & Creative', 'Visual design and graphics'),
            ('UI/UX Design', 'Design & Creative', 'User interface and experience design'),
            ('Web Design', 'Design & Creative', 'Website design and layout'),
            ('Product Design', 'Design & Creative', 'Product and industrial design'),
            ('Video Editing', 'Design & Creative', 'Video production and editing'),
            ('Animation', 'Design & Creative', '2D/3D animation and motion graphics'),
            ('Photography', 'Design & Creative', 'Professional photography services'),
            ('Illustration', 'Design & Creative', 'Digital and traditional illustration'),
            ('Brand Design', 'Design & Creative', 'Brand identity and visual branding'),
            ('Content Creation', 'Design & Creative', 'Digital content and multimedia creation'),
            
            # Marketing & Sales subcategories
            ('Digital Marketing', 'Marketing & Sales', 'Online marketing and digital campaigns'),
            ('Content Marketing', 'Marketing & Sales', 'Content strategy and marketing'),
            ('Social Media Marketing', 'Marketing & Sales', 'Social media management and marketing'),
            ('SEO/SEM', 'Marketing & Sales', 'Search engine optimization and marketing'),
            ('Email Marketing', 'Marketing & Sales', 'Email campaigns and automation'),
            ('Marketing Strategy', 'Marketing & Sales', 'Marketing planning and strategy'),
            ('Sales', 'Marketing & Sales', 'Sales representatives and account executives'),
            ('Business Development', 'Marketing & Sales', 'Business growth and partnerships'),
            ('Account Management', 'Marketing & Sales', 'Client and account relationship management'),
            ('Marketing Analytics', 'Marketing & Sales', 'Marketing data analysis and insights'),
            ('Brand Management', 'Marketing & Sales', 'Brand strategy and management'),
            ('Public Relations', 'Marketing & Sales', 'PR and communications'),
            
            # Administrative & Office subcategories
            ('Administrative Assistant', 'Administrative & Office', 'General administrative support'),
            ('Executive Assistant', 'Administrative & Office', 'Executive-level administrative support'),
            ('Office Manager', 'Administrative & Office', 'Office operations and management'),
            ('Data Entry', 'Administrative & Office', 'Data entry and database management'),
            ('Receptionist', 'Administrative & Office', 'Front desk and reception services'),
            ('Secretary', 'Administrative & Office', 'Secretarial and clerical work'),
            ('Virtual Assistant', 'Administrative & Office', 'Remote administrative support'),
            ('Document Control', 'Administrative & Office', 'Document management and organization'),
            
            # Human Resources subcategories
            ('Recruitment', 'Human Resources', 'Talent acquisition and recruiting'),
            ('HR Management', 'Human Resources', 'HR operations and management'),
            ('Compensation & Benefits', 'Human Resources', 'Employee compensation and benefits'),
            ('Training & Development', 'Human Resources', 'Employee training and development'),
            ('Employee Relations', 'Human Resources', 'Employee relations and engagement'),
            ('Payroll', 'Human Resources', 'Payroll processing and management'),
            
            # Finance & Accounting subcategories
            ('Accounting', 'Finance & Accounting', 'General accounting and bookkeeping'),
            ('Financial Analysis', 'Finance & Accounting', 'Financial analysis and planning'),
            ('Auditing', 'Finance & Accounting', 'Internal and external auditing'),
            ('Tax', 'Finance & Accounting', 'Tax preparation and planning'),
            ('Corporate Finance', 'Finance & Accounting', 'Corporate financial management'),
            ('Investment Management', 'Finance & Accounting', 'Investment analysis and portfolio management'),
            
            # Customer Service subcategories
            ('Customer Support', 'Customer Service', 'Customer service and support'),
            ('Technical Support', 'Customer Service', 'Technical customer support'),
            ('Call Center', 'Customer Service', 'Call center operations'),
            ('Customer Success', 'Customer Service', 'Customer success and retention'),
            ('Client Services', 'Customer Service', 'Client relationship management'),
            
            # Healthcare subcategories
            ('Nursing', 'Healthcare', 'Registered nurses and nursing roles'),
            ('Medical Assistant', 'Healthcare', 'Medical assistance and clinical support'),
            ('Pharmacy', 'Healthcare', 'Pharmacy and pharmaceutical services'),
            ('Therapy', 'Healthcare', 'Physical, occupational, and speech therapy'),
            ('Medical Billing', 'Healthcare', 'Medical billing and coding'),
            ('Healthcare Administration', 'Healthcare', 'Healthcare management and administration'),
            ('Clinical Research', 'Healthcare', 'Clinical trials and medical research'),
            ('Laboratory', 'Healthcare', 'Medical laboratory services'),
            
            # Education & Training subcategories
            ('Teaching', 'Education & Training', 'Primary, secondary, and higher education'),
            ('Tutoring', 'Education & Training', 'Private tutoring and instruction'),
            ('Instructional Design', 'Education & Training', 'Course design and development'),
            ('Corporate Training', 'Education & Training', 'Professional training and development'),
            ('Education Administration', 'Education & Training', 'Educational administration and management'),
            ('Curriculum Development', 'Education & Training', 'Curriculum planning and design'),
            
            # Engineering subcategories
            ('Mechanical Engineering', 'Engineering', 'Mechanical systems and design'),
            ('Electrical Engineering', 'Engineering', 'Electrical systems and electronics'),
            ('Civil Engineering', 'Engineering', 'Infrastructure and construction engineering'),
            ('Chemical Engineering', 'Engineering', 'Chemical processes and manufacturing'),
            ('Industrial Engineering', 'Engineering', 'Process optimization and efficiency'),
            ('Quality Engineering', 'Engineering', 'Quality assurance and control'),
            
            # Legal subcategories
            ('Paralegal', 'Legal', 'Legal assistance and paralegal work'),
            ('Contract Management', 'Legal', 'Contract administration and management'),
            ('Compliance', 'Legal', 'Regulatory compliance and governance'),
            ('Legal Research', 'Legal', 'Legal research and analysis'),
            
            # Operations & Logistics subcategories
            ('Operations Management', 'Operations & Logistics', 'Operations planning and management'),
            ('Supply Chain', 'Operations & Logistics', 'Supply chain management'),
            ('Logistics', 'Operations & Logistics', 'Logistics and distribution'),
            ('Warehouse Management', 'Operations & Logistics', 'Warehouse operations'),
            ('Inventory Control', 'Operations & Logistics', 'Inventory management'),
            ('Procurement', 'Operations & Logistics', 'Purchasing and procurement'),
            
            # Management subcategories
            ('Project Management', 'Management', 'Project planning and execution'),
            ('Product Management', 'Management', 'Product strategy and development'),
            ('Program Management', 'Management', 'Program coordination and management'),
            ('Team Leadership', 'Management', 'Team management and leadership'),
            ('General Management', 'Management', 'General business management'),
            
            # Writing & Content subcategories
            ('Content Writing', 'Writing & Content', 'Article and blog writing'),
            ('Copywriting', 'Writing & Content', 'Marketing and advertising copy'),
            ('Editing', 'Writing & Content', 'Content editing and proofreading'),
            ('Grant Writing', 'Writing & Content', 'Grant proposals and fundraising'),
            ('Journalism', 'Writing & Content', 'News and feature writing'),
            
            # Consulting subcategories
            ('Business Consulting', 'Consulting', 'Business strategy and consulting'),
            ('Management Consulting', 'Consulting', 'Management advisory services'),
            ('IT Consulting', 'Consulting', 'Technology consulting'),
            ('Strategy Consulting', 'Consulting', 'Strategic planning and consulting'),
            
            # Real Estate subcategories
            ('Real Estate Sales', 'Real Estate', 'Real estate sales and brokerage'),
            ('Property Management', 'Real Estate', 'Property management services'),
            ('Real Estate Analysis', 'Real Estate', 'Real estate market analysis'),
            
            # Hospitality & Tourism subcategories
            ('Hotel Management', 'Hospitality & Tourism', 'Hotel operations and management'),
            ('Event Planning', 'Hospitality & Tourism', 'Event coordination and planning'),
            ('Travel Services', 'Hospitality & Tourism', 'Travel planning and coordination'),
            ('Restaurant Management', 'Hospitality & Tourism', 'Restaurant operations'),
            
            # Research & Science subcategories
            ('Research', 'Research & Science', 'Scientific research and analysis'),
            ('Laboratory Services', 'Research & Science', 'Laboratory testing and analysis'),
            ('Data Science', 'Research & Science', 'Data science and analytics'),
            
            # Trades & Services subcategories
            ('Electrical', 'Trades & Services', 'Electrical services and installation'),
            ('Plumbing', 'Trades & Services', 'Plumbing services and repair'),
            ('HVAC', 'Trades & Services', 'Heating, ventilation, and air conditioning'),
            ('Carpentry', 'Trades & Services', 'Carpentry and woodworking'),
            ('Automotive', 'Trades & Services', 'Automotive repair and maintenance'),
            ('Maintenance', 'Trades & Services', 'General maintenance and repair'),
            
            # Non-Profit & Social Services subcategories
            ('Social Work', 'Non-Profit & Social Services', 'Social work and counseling'),
            ('Program Coordination', 'Non-Profit & Social Services', 'Non-profit program management'),
            ('Grant Management', 'Non-Profit & Social Services', 'Grant administration'),
            ('Community Outreach', 'Non-Profit & Social Services', 'Community engagement and outreach'),
            ('Fundraising', 'Non-Profit & Social Services', 'Fundraising and development'),
        ]

        created_count = 0
        existing_count = 0
        parent_cache = {}

        # First, create all parent categories
        self.stdout.write(self.style.MIGRATE_HEADING('\nCreating Parent Categories...'))
        for name, description in parent_categories:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={
                    'description': description,
                    'parent': None
                }
            )
            parent_cache[name] = category
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created parent: {name}')
                )
            else:
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(f'○ Already exists: {name}')
                )

        # Then, create all subcategories
        self.stdout.write(self.style.MIGRATE_HEADING('\nCreating Subcategories...'))
        for child_name, parent_name, description in subcategories:
            parent = parent_cache.get(parent_name)
            if not parent:
                self.stdout.write(
                    self.style.ERROR(f'✗ Parent not found for: {child_name} (parent: {parent_name})')
                )
                continue
                
            category, created = Category.objects.get_or_create(
                name=child_name,
                defaults={
                    'description': description,
                    'parent': parent
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ Created: {child_name} → {parent_name}')
                )
            else:
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(f'  ○ Already exists: {child_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n{"="*60}\n'
                f'Summary:\n'
                f'  Created: {created_count} new categories\n'
                f'  Existing: {existing_count} categories\n'
                f'  Total: {created_count + existing_count} categories\n'
                f'  Parents: {len(parent_categories)}\n'
                f'  Children: {len(subcategories)}\n'
                f'{"="*60}'
            )
        )