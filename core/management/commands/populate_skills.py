# management/commands/populate_skills.py
from django.core.management.base import BaseCommand
from core.models import Skill

class Command(BaseCommand):
    help = 'Populate the Skill model with common skills'

    def handle(self, *args, **kwargs):
        # Format: (name, category, description)
        skills = [
            # Programming Languages
            ('Python', 'Programming Language', 'General-purpose programming language popular for web, data science, and automation'),
            ('JavaScript', 'Programming Language', 'Essential language for web development and interactive websites'),
            ('Java', 'Programming Language', 'Object-oriented language used for enterprise applications and Android development'),
            ('C++', 'Programming Language', 'High-performance language for system programming and game development'),
            ('C#', 'Programming Language', 'Microsoft\'s object-oriented language for .NET development'),
            ('TypeScript', 'Programming Language', 'Typed superset of JavaScript for large-scale applications'),
            ('PHP', 'Programming Language', 'Server-side scripting language for web development'),
            ('Ruby', 'Programming Language', 'Dynamic language known for developer productivity'),
            ('Go', 'Programming Language', 'Google\'s language designed for concurrent and cloud applications'),
            ('Swift', 'Programming Language', 'Apple\'s language for iOS and macOS development'),
            ('Kotlin', 'Programming Language', 'Modern language for Android and cross-platform development'),
            ('Rust', 'Programming Language', 'Systems programming language focused on safety and performance'),
            ('Scala', 'Programming Language', 'Functional programming language running on the JVM'),
            ('R', 'Programming Language', 'Statistical programming language for data analysis'),
            
            # Backend Frameworks
            ('Django', 'Backend Framework', 'High-level Python web framework for rapid development'),
            ('Flask', 'Backend Framework', 'Lightweight Python web framework'),
            ('FastAPI', 'Backend Framework', 'Modern Python framework for building APIs'),
            ('Spring Boot', 'Backend Framework', 'Java framework for building enterprise applications'),
            ('Laravel', 'Backend Framework', 'PHP framework for elegant web applications'),
            ('Ruby on Rails', 'Backend Framework', 'Full-stack Ruby framework following MVC pattern'),
            ('ASP.NET Core', 'Backend Framework', 'Microsoft\'s cross-platform framework for web apps'),
            ('Express.js', 'Backend Framework', 'Minimalist Node.js web framework'),
            
            # Frontend Frameworks & Libraries
            ('React', 'Frontend Framework', 'JavaScript library for building user interfaces'),
            ('Angular', 'Frontend Framework', 'TypeScript-based framework by Google'),
            ('Vue.js', 'Frontend Framework', 'Progressive JavaScript framework'),
            ('Next.js', 'Frontend Framework', 'React framework for production applications'),
            ('Svelte', 'Frontend Framework', 'Compiler-based frontend framework'),
            ('jQuery', 'Frontend Framework', 'JavaScript library for DOM manipulation'),
            ('Bootstrap', 'Frontend Framework', 'CSS framework for responsive design'),
            ('Tailwind CSS', 'Frontend Framework', 'Utility-first CSS framework'),
            
            # Backend Runtime
            ('Node.js', 'Backend Framework', 'JavaScript runtime for server-side development'),
            
            # Mobile Development
            ('React Native', 'Mobile Development', 'Framework for building native mobile apps with React'),
            ('Flutter', 'Mobile Development', 'Google\'s UI toolkit for cross-platform mobile apps'),
            ('Android Development', 'Mobile Development', 'Native Android app development'),
            ('iOS Development', 'Mobile Development', 'Native iOS app development with Swift/Objective-C'),
            ('Xamarin', 'Mobile Development', 'Microsoft\'s cross-platform mobile development framework'),
            
            # Databases - Relational
            ('PostgreSQL', 'Database', 'Advanced open-source relational database'),
            ('MySQL', 'Database', 'Popular open-source relational database'),
            ('SQL Server', 'Database', 'Microsoft\'s enterprise relational database'),
            ('Oracle Database', 'Database', 'Enterprise-grade relational database system'),
            ('SQLite', 'Database', 'Lightweight embedded database'),
            ('MariaDB', 'Database', 'MySQL fork with additional features'),
            
            # Databases - NoSQL
            ('MongoDB', 'Database', 'Document-oriented NoSQL database'),
            ('Redis', 'Database', 'In-memory data structure store and cache'),
            ('Cassandra', 'Database', 'Distributed NoSQL database for big data'),
            ('DynamoDB', 'Database', 'Amazon\'s managed NoSQL database'),
            ('Elasticsearch', 'Database', 'Search and analytics engine'),
            ('CouchDB', 'Database', 'Document-oriented NoSQL database'),
            
            # Database Skills
            ('SQL', 'Data & Analytics', 'Structured Query Language for database management'),
            ('Database Design', 'Database', 'Designing efficient database schemas and relationships'),
            ('Database Administration', 'Database', 'Managing and maintaining database systems'),
            ('Query Optimization', 'Database', 'Improving database query performance'),
            
            # Cloud Platforms
            ('AWS', 'Cloud Platform', 'Amazon Web Services cloud platform'),
            ('Azure', 'Cloud Platform', 'Microsoft\'s cloud computing platform'),
            ('Google Cloud', 'Cloud Platform', 'Google\'s cloud infrastructure platform'),
            ('DigitalOcean', 'Cloud Platform', 'Cloud infrastructure for developers'),
            ('Heroku', 'Cloud Platform', 'Platform as a Service for app deployment'),
            
            # DevOps & CI/CD
            ('Docker', 'DevOps', 'Containerization platform for applications'),
            ('Kubernetes', 'DevOps', 'Container orchestration platform'),
            ('Jenkins', 'CI/CD', 'Automation server for CI/CD pipelines'),
            ('GitHub Actions', 'CI/CD', 'Workflow automation and CI/CD in GitHub'),
            ('GitLab CI', 'CI/CD', 'GitLab\'s built-in CI/CD solution'),
            ('CircleCI', 'CI/CD', 'Cloud-based CI/CD platform'),
            ('Travis CI', 'CI/CD', 'Continuous integration service'),
            
            # Infrastructure & Configuration
            ('Terraform', 'Infrastructure as Code', 'Infrastructure provisioning and management'),
            ('Ansible', 'Infrastructure as Code', 'Automation and configuration management'),
            ('Puppet', 'Infrastructure as Code', 'Configuration management tool'),
            ('Chef', 'Infrastructure as Code', 'Infrastructure automation framework'),
            
            # Version Control
            ('Git', 'Version Control', 'Distributed version control system'),
            ('GitHub', 'Version Control', 'Git repository hosting and collaboration'),
            ('GitLab', 'Version Control', 'DevOps platform with Git repository management'),
            ('Bitbucket', 'Version Control', 'Git repository management by Atlassian'),
            ('SVN', 'Version Control', 'Subversion version control system'),
            
            # Testing
            ('Jest', 'Testing', 'JavaScript testing framework'),
            ('Pytest', 'Testing', 'Python testing framework'),
            ('JUnit', 'Testing', 'Java testing framework'),
            ('Selenium', 'Testing', 'Browser automation for testing'),
            ('Cypress', 'Testing', 'End-to-end testing for web applications'),
            ('Postman', 'Testing', 'API development and testing tool'),
            
            # Administrative Skills - Office Software
            ('Microsoft Office Suite', 'Administrative', 'Word, Excel, PowerPoint, and Outlook proficiency'),
            ('Microsoft Excel', 'Administrative', 'Spreadsheet creation, formulas, and data analysis'),
            ('Microsoft Word', 'Administrative', 'Document creation and formatting'),
            ('Microsoft PowerPoint', 'Administrative', 'Presentation design and delivery'),
            ('Microsoft Outlook', 'Administrative', 'Email and calendar management'),
            ('Google Workspace', 'Administrative', 'Google Docs, Sheets, Slides, and Gmail'),
            ('Google Sheets', 'Administrative', 'Cloud-based spreadsheet management'),
            ('Google Docs', 'Administrative', 'Cloud-based document creation'),
            ('LibreOffice', 'Administrative', 'Open-source office suite'),
            
            # Administrative Skills - Communication & Customer Service
            ('Email Management', 'Administrative', 'Managing and organizing email communications'),
            ('Business Correspondence', 'Administrative', 'Professional written communication'),
            ('Customer Service', 'Administrative', 'Assisting and supporting customers'),
            ('Client Relations', 'Administrative', 'Building and maintaining client relationships'),
            ('Phone Etiquette', 'Administrative', 'Professional telephone communication'),
            ('Live Chat Support', 'Administrative', 'Real-time customer assistance'),
            
            # Administrative Skills - Scheduling & Organization
            ('Calendar Management', 'Administrative', 'Scheduling and coordinating appointments'),
            ('Appointment Scheduling', 'Administrative', 'Booking and managing appointments'),
            ('Travel Arrangements', 'Administrative', 'Planning and booking business travel'),
            ('Event Planning', 'Administrative', 'Organizing and coordinating events'),
            ('Meeting Coordination', 'Administrative', 'Scheduling and facilitating meetings'),
            ('Time Management', 'Administrative', 'Efficiently managing time and priorities'),
            ('Multitasking', 'Administrative', 'Handling multiple tasks simultaneously'),
            ('Priority Management', 'Administrative', 'Organizing tasks by importance and urgency'),
            ('Project Coordination', 'Administrative', 'Supporting project management activities'),
            
            # Administrative Skills - Data & Records
            ('Data Entry', 'Administrative', 'Accurate input of information into systems'),
            ('File Management', 'Administrative', 'Organizing and maintaining files'),
            ('Document Preparation', 'Administrative', 'Creating and formatting documents'),
            ('Records Management', 'Administrative', 'Maintaining organized record systems'),
            ('Archive Management', 'Administrative', 'Managing historical records and documents'),
            ('Document Control', 'Administrative', 'Version control and document tracking'),
            
            # Administrative Skills - Office Management
            ('Office Administration', 'Administrative', 'General office operations and management'),
            ('Reception', 'Administrative', 'Front desk and visitor management'),
            ('Inventory Management', 'Administrative', 'Tracking and managing office supplies'),
            ('Vendor Management', 'Administrative', 'Coordinating with suppliers and vendors'),
            ('Facilities Management', 'Administrative', 'Overseeing office space and amenities'),
            
            # Administrative Skills - Specialized Software
            ('Typing', 'Administrative', 'Fast and accurate keyboard skills'),
            ('Transcription', 'Administrative', 'Converting audio/video to written text'),
            ('Proofreading', 'Administrative', 'Reviewing and correcting written content'),
            ('Report Writing', 'Administrative', 'Creating detailed business reports'),
            ('Presentation Skills', 'Administrative', 'Delivering effective presentations'),
            ('Database Management', 'Administrative', 'Maintaining organizational databases'),
            ('CRM Software', 'Administrative', 'Customer relationship management systems'),
            ('Salesforce', 'Administrative', 'Salesforce CRM platform proficiency'),
            ('HubSpot', 'Administrative', 'HubSpot CRM and marketing platform'),
            ('SharePoint', 'Administrative', 'Microsoft SharePoint collaboration platform'),
            ('Slack', 'Administrative', 'Team communication and collaboration'),
            ('Zoom', 'Administrative', 'Video conferencing and virtual meetings'),
            ('Microsoft Teams', 'Administrative', 'Team collaboration and communication'),
            ('Asana', 'Administrative', 'Project and task management'),
            ('Trello', 'Administrative', 'Visual project management boards'),
            ('Monday.com', 'Administrative', 'Work operating system and project management'),
            ('Notion', 'Administrative', 'All-in-one workspace and documentation'),
            
            # Administrative Skills - HR & Recruiting
            ('Onboarding', 'Administrative', 'New employee integration processes'),
            ('Employee Records Management', 'Administrative', 'Maintaining employee information'),
            ('Recruitment Support', 'Administrative', 'Assisting with hiring processes'),
            ('Policy Documentation', 'Administrative', 'Creating and maintaining policy documents'),
            ('Benefits Administration', 'Administrative', 'Managing employee benefits programs'),
            ('Payroll Processing', 'Administrative', 'Processing employee compensation'),
            
            # Administrative Skills - Financial
            ('Bookkeeping', 'Administrative', 'Recording financial transactions'),
            ('Expense Tracking', 'Administrative', 'Managing and reporting expenses'),
            ('Invoice Processing', 'Administrative', 'Handling invoices and billing'),
            ('Purchase Orders', 'Administrative', 'Creating and managing purchase orders'),
            ('Budget Tracking', 'Administrative', 'Monitoring budget and spending'),
            ('QuickBooks', 'Administrative', 'QuickBooks accounting software'),
            ('Xero', 'Administrative', 'Xero accounting platform'),
            
            # Soft Skills - Leadership & Management
            ('Team Leadership', 'Soft Skill', 'Leading and motivating teams'),
            ('Project Management', 'Soft Skill', 'Planning and executing projects'),
            ('People Management', 'Soft Skill', 'Managing and developing team members'),
            ('Strategic Planning', 'Soft Skill', 'Long-term planning and strategy'),
            ('Decision Making', 'Soft Skill', 'Making effective and timely decisions'),
            ('Delegation', 'Soft Skill', 'Assigning tasks appropriately'),
            ('Coaching & Mentoring', 'Soft Skill', 'Developing others\' skills and abilities'),
            
            # Soft Skills - Communication
            ('Communication', 'Soft Skill', 'Effective verbal and written communication'),
            ('Public Speaking', 'Soft Skill', 'Presenting to audiences confidently'),
            ('Active Listening', 'Soft Skill', 'Fully concentrating and understanding others'),
            ('Negotiation', 'Soft Skill', 'Reaching mutually beneficial agreements'),
            ('Persuasion', 'Soft Skill', 'Influencing others effectively'),
            ('Interpersonal Skills', 'Soft Skill', 'Building positive relationships'),
            ('Conflict Resolution', 'Soft Skill', 'Resolving disagreements constructively'),
            
            # Soft Skills - Problem Solving & Thinking
            ('Problem Solving', 'Soft Skill', 'Identifying and resolving issues'),
            ('Critical Thinking', 'Soft Skill', 'Analytical and logical reasoning'),
            ('Creative Thinking', 'Soft Skill', 'Generating innovative ideas and solutions'),
            ('Analytical Skills', 'Soft Skill', 'Breaking down complex information'),
            ('Research Skills', 'Soft Skill', 'Finding and evaluating information'),
            ('Attention to Detail', 'Soft Skill', 'Thoroughness and accuracy in work'),
            
            # Soft Skills - Personal Effectiveness
            ('Teamwork', 'Soft Skill', 'Collaborating effectively with others'),
            ('Adaptability', 'Soft Skill', 'Adjusting to change and new situations'),
            ('Flexibility', 'Soft Skill', 'Being open to different approaches'),
            ('Self-Motivation', 'Soft Skill', 'Driving oneself without external push'),
            ('Work Ethic', 'Soft Skill', 'Commitment to quality and productivity'),
            ('Reliability', 'Soft Skill', 'Consistent and dependable performance'),
            ('Organizational Skills', 'Soft Skill', 'Keeping work structured and efficient'),
            ('Stress Management', 'Soft Skill', 'Handling pressure effectively'),
            ('Emotional Intelligence', 'Soft Skill', 'Understanding and managing emotions'),
            
            # Marketing - Digital Marketing
            ('Digital Marketing', 'Marketing', 'Online marketing strategies and campaigns'),
            ('SEO', 'Marketing', 'Search engine optimization techniques'),
            ('SEM', 'Marketing', 'Search engine marketing and paid ads'),
            ('Content Marketing', 'Marketing', 'Creating valuable content to attract customers'),
            ('Social Media Marketing', 'Marketing', 'Marketing through social media platforms'),
            ('Email Marketing', 'Marketing', 'Email campaigns and automation'),
            ('Affiliate Marketing', 'Marketing', 'Partner-based marketing programs'),
            ('Influencer Marketing', 'Marketing', 'Collaborating with influencers for promotion'),
            ('Marketing Automation', 'Marketing', 'Automated marketing workflows'),
            
            # Marketing - Platforms & Tools
            ('Google Analytics', 'Marketing', 'Web analytics and reporting'),
            ('Google Ads', 'Marketing', 'Google advertising platform'),
            ('Facebook Ads', 'Marketing', 'Facebook advertising and campaigns'),
            ('LinkedIn Marketing', 'Marketing', 'LinkedIn content and advertising'),
            ('Instagram Marketing', 'Marketing', 'Instagram content and promotion'),
            ('Twitter Marketing', 'Marketing', 'Twitter engagement and advertising'),
            ('TikTok Marketing', 'Marketing', 'TikTok content and advertising'),
            ('Mailchimp', 'Marketing', 'Email marketing platform'),
            ('HubSpot Marketing', 'Marketing', 'HubSpot marketing automation'),
            ('Hootsuite', 'Marketing', 'Social media management platform'),
            ('Buffer', 'Marketing', 'Social media scheduling and analytics'),
            
            # Marketing - Strategy & Analysis
            ('Marketing Strategy', 'Marketing', 'Planning and executing marketing plans'),
            ('Brand Management', 'Marketing', 'Building and maintaining brand identity'),
            ('Market Research', 'Marketing', 'Analyzing market trends and customer needs'),
            ('Competitor Analysis', 'Marketing', 'Researching and analyzing competitors'),
            ('Campaign Management', 'Marketing', 'Planning and executing marketing campaigns'),
            ('Conversion Optimization', 'Marketing', 'Improving conversion rates'),
            ('A/B Testing', 'Marketing', 'Testing variations to optimize performance'),
            ('Marketing Analytics', 'Marketing', 'Analyzing marketing data and metrics'),
            
            # Marketing - Content
            ('Content Creation', 'Marketing', 'Creating engaging marketing content'),
            ('Copywriting', 'Marketing', 'Writing persuasive marketing copy'),
            ('Video Marketing', 'Marketing', 'Creating and promoting video content'),
            ('Blogging', 'Marketing', 'Writing and maintaining blog content'),
            
            # Sales
            ('Sales', 'Sales', 'Selling products and services'),
            ('B2B Sales', 'Sales', 'Business-to-business sales'),
            ('B2C Sales', 'Sales', 'Business-to-consumer sales'),
            ('Inside Sales', 'Sales', 'Remote sales via phone and email'),
            ('Outside Sales', 'Sales', 'Field sales with in-person meetings'),
            ('Account Management', 'Sales', 'Managing client accounts and relationships'),
            ('Business Development', 'Sales', 'Identifying and creating business opportunities'),
            ('Lead Generation', 'Sales', 'Finding and qualifying potential customers'),
            ('Sales Forecasting', 'Sales', 'Predicting future sales performance'),
            ('Negotiation Skills', 'Sales', 'Negotiating deals and contracts'),
            ('Cold Calling', 'Sales', 'Reaching out to potential customers'),
            ('CRM Management', 'Sales', 'Managing customer data in CRM systems'),
            
            # Design - Graphic & Visual Design
            ('Graphic Design', 'Design', 'Creating visual content and graphics'),
            ('Adobe Photoshop', 'Design', 'Image editing and manipulation software'),
            ('Adobe Illustrator', 'Design', 'Vector graphics and illustration software'),
            ('Adobe InDesign', 'Design', 'Page layout and publishing software'),
            ('Canva', 'Design', 'Online graphic design tool'),
            ('Sketch', 'Design', 'Digital design tool for Mac'),
            ('Figma', 'Design', 'Collaborative interface design tool'),
            ('Adobe XD', 'Design', 'UI/UX design and prototyping tool'),
            
            # Design - UI/UX & Product
            ('UI/UX Design', 'Design', 'User interface and experience design'),
            ('User Research', 'Design', 'Understanding user needs and behaviors'),
            ('Wireframing', 'Design', 'Creating website/app structural layouts'),
            ('Prototyping', 'Design', 'Building interactive design prototypes'),
            ('Responsive Design', 'Design', 'Designing for multiple screen sizes'),
            ('Mobile App Design', 'Design', 'Designing mobile applications'),
            ('Web Design', 'Design', 'Designing websites and web applications'),
            ('Interaction Design', 'Design', 'Designing interactive elements'),
            
            # Design - Specialized
            ('Logo Design', 'Design', 'Creating brand logos and identities'),
            ('Brand Identity', 'Design', 'Developing cohesive brand visuals'),
            ('Print Design', 'Design', 'Designing for print materials'),
            ('Packaging Design', 'Design', 'Designing product packaging'),
            ('Typography', 'Design', 'Art and technique of arranging type'),
            ('Color Theory', 'Design', 'Understanding and applying color principles'),
            ('3D Design', 'Design', '3D modeling and rendering'),
            ('Animation', 'Design', 'Creating animated graphics and videos'),
            ('Motion Graphics', 'Design', 'Animated graphic design'),
            ('Video Editing', 'Design', 'Editing and producing videos'),
            ('Adobe After Effects', 'Design', 'Motion graphics and visual effects'),
            ('Adobe Premiere Pro', 'Design', 'Video editing software'),
            ('Final Cut Pro', 'Design', 'Professional video editing for Mac'),
            
            # Data & Analytics
            ('Data Analysis', 'Data & Analytics', 'Analyzing and interpreting data'),
            ('Data Visualization', 'Data & Analytics', 'Creating visual representations of data'),
            ('Statistical Analysis', 'Data & Analytics', 'Statistical methods and techniques'),
            ('Excel Advanced', 'Data & Analytics', 'Advanced Excel functions and analysis'),
            ('Power BI', 'Data & Analytics', 'Microsoft business intelligence platform'),
            ('Tableau', 'Data & Analytics', 'Data visualization and analytics platform'),
            ('Looker', 'Data & Analytics', 'Business intelligence and analytics'),
            ('Google Data Studio', 'Data & Analytics', 'Google\'s data visualization tool'),
            ('Statistics', 'Data & Analytics', 'Statistical theory and application'),
            ('Data Mining', 'Data & Analytics', 'Extracting patterns from large datasets'),
            ('Big Data', 'Data & Analytics', 'Processing and analyzing large datasets'),
            ('ETL', 'Data & Analytics', 'Extract, Transform, Load data processes'),
            
            # Data Science & AI
            ('Machine Learning', 'Data Science', 'Building predictive models and algorithms'),
            ('Deep Learning', 'Data Science', 'Neural networks and advanced ML'),
            ('Artificial Intelligence', 'Data Science', 'AI systems and applications'),
            ('Natural Language Processing', 'Data Science', 'Processing and analyzing text data'),
            ('Computer Vision', 'Data Science', 'Image and video analysis'),
            ('TensorFlow', 'Data Science', 'Machine learning framework'),
            ('PyTorch', 'Data Science', 'Deep learning framework'),
            ('scikit-learn', 'Data Science', 'Machine learning library for Python'),
            ('Pandas', 'Data Science', 'Data manipulation library for Python'),
            ('NumPy', 'Data Science', 'Numerical computing library for Python'),
            ('Jupyter Notebook', 'Data Science', 'Interactive computing environment'),
            
            # Business & Finance
            ('Financial Modeling', 'Finance', 'Building financial projections and models'),
            ('Financial Analysis', 'Finance', 'Analyzing financial data and statements'),
            ('Accounting', 'Finance', 'Recording and reporting financial transactions'),
            ('Budgeting', 'Finance', 'Planning and managing budgets'),
            ('Forecasting', 'Finance', 'Predicting future financial performance'),
            ('Risk Management', 'Finance', 'Identifying and mitigating risks'),
            ('Investment Analysis', 'Finance', 'Evaluating investment opportunities'),
            ('Corporate Finance', 'Finance', 'Managing company finances'),
            ('Tax Preparation', 'Finance', 'Preparing tax returns and planning'),
            ('Audit', 'Finance', 'Financial auditing and compliance'),
            
            # Project & Product Management
            ('Agile Methodology', 'Project Management', 'Agile project management approach'),
            ('Scrum', 'Project Management', 'Scrum framework for agile teams'),
            ('Kanban', 'Project Management', 'Visual workflow management method'),
            ('Waterfall', 'Project Management', 'Sequential project management approach'),
            ('JIRA', 'Project Management', 'Project tracking and agile management'),
            ('Product Roadmapping', 'Product Management', 'Planning product development timeline'),
            ('User Stories', 'Product Management', 'Defining product features from user perspective'),
            ('Product Strategy', 'Product Management', 'Long-term product planning'),
            ('Stakeholder Management', 'Project Management', 'Managing project stakeholders'),
            ('Risk Assessment', 'Project Management', 'Identifying and evaluating project risks'),
            
            # Other Professional Skills
            ('Technical Writing', 'Writing', 'Creating technical documentation'),
            ('Business Writing', 'Writing', 'Professional business communications'),
            ('Content Writing', 'Writing', 'Writing articles, blogs, and web content'),
            ('Editing', 'Writing', 'Reviewing and improving written content'),
            ('Translation', 'Languages', 'Translating between languages'),
            ('Spanish', 'Languages', 'Spanish language proficiency'),
            ('French', 'Languages', 'French language proficiency'),
            ('German', 'Languages', 'German language proficiency'),
            ('Mandarin', 'Languages', 'Mandarin Chinese language proficiency'),
            ('Arabic', 'Languages', 'Arabic language proficiency'),
        ]

        created_count = 0
        existing_count = 0
        updated_count = 0

        self.stdout.write(self.style.MIGRATE_HEADING('\nPopulating Skills Database...\n'))

        for skill_name, category, description in skills:
            skill, created = Skill.objects.get_or_create(
                name=skill_name,
                defaults={
                    'category': category,
                    'description': description
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {skill_name} ({category})')
                )
            else:
                # Update description if it's empty
                if not skill.description and description:
                    skill.description = description
                    skill.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'Updated: {skill_name} (added description)')
                    )
                else:
                    existing_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'Already exists: {skill_name}')
                    )

        # Category summary
        categories_count = Skill.objects.values('category').distinct().count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n{"="*60}\n'
                f'Summary:\n'
                f'  Created: {created_count} new skills\n'
                f'  Updated: {updated_count} skills (added descriptions)\n'
                f'  Existing: {existing_count} skills\n'
                f'  Total: {created_count + existing_count + updated_count} skills\n'
                f'  Categories: {categories_count} unique categories\n'
                f'{"="*60}'
            )
        )