# Job Portal API Documentation (Complete)

## Base URL
```
http://localhost:8000/api
```

## Authentication
This API uses JWT (JSON Web Token) authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## Table of Contents
1. [Authentication Endpoints](#authentication-endpoints)
2. [Profile Management](#profile-management)
3. [Job Management](#job-management)
4. [Application Management](#application-management)
5. [Education & Certifications](#education--certifications)
6. [Skills Management](#skills-management)
7. [Job Categories](#job-categories)
8. [Saved Jobs & Job Alerts](#saved-jobs--job-alerts)
9. [Company Reviews](#company-reviews)
10. [Notifications](#notifications)
11. [Address Management](#address-management)

---

## Authentication Endpoints

### 1. Register User
**Endpoint:** `POST /api/auth/register/`  
**Authentication:** Not required

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "password2": "securePassword123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "CANDIDATE"
}
```

**Success Response (201):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "CANDIDATE",
    "is_active": true,
    "is_employer": false,
    "is_candidate": true,
    "is_admin": false
  }
}
```

---

### 2. Login
**Endpoint:** `POST /api/auth/login/`  
**Authentication:** Not required

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Success Response (200):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "CANDIDATE"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 3. Refresh Token
**Endpoint:** `POST /api/auth/refresh/`  
**Authentication:** Not required

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 4. Get Current User
**Endpoint:** `GET /api/auth/me/`  
**Authentication:** Required

---

## Profile Management

### 5. Get User Profile
**Endpoint:** `GET /api/auth/profile/`  
**Authentication:** Required  
**Note:** Returns different structure based on user role (Candidate/Employer)

**Candidate Response:**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "email": "candidate@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "CANDIDATE"
  },
  "phone": "+1234567890",
  "gender": "MALE",
  "date_of_birth": "1990-01-15",
  "headline": "Senior Software Engineer",
  "about": "Experienced software engineer...",
  "linkedin": "https://linkedin.com/in/johndoe",
  "github": "https://github.com/johndoe",
  "twitter": "https://twitter.com/johndoe",
  "website": "https://johndoe.com",
  "profile_picture": "http://localhost:8000/media/profiles/pictures/photo.jpg",
  "resume": "http://localhost:8000/media/profiles/resumes/resume.pdf",
  "is_verified": false,
  "verified": false,
  "profile_completion": 85,
  "is_profile_complete": false,
  "candidate_skills": [...],
  "education": [...],
  "certifications": [...],
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-20T15:30:00Z"
}
```

---

### 6. Update Profile
**Endpoint:** `PATCH /api/auth/update_profile/` or `PUT /api/auth/update_profile/`  
**Authentication:** Required  
**Content-Type:** `multipart/form-data`

---

## Education & Certifications

### 7. List Education
**Endpoint:** `GET /api/profile/education/`  
**Authentication:** Required (Candidate only)

**Success Response (200):**
```json
[
  {
    "id": 1,
    "level": "BACHELOR",
    "field_of_study": "Computer Science",
    "institution": "MIT",
    "start_date": "2010-09-01",
    "end_date": "2014-06-01",
    "description": "Bachelor's degree in Computer Science",
    "created_at": "2024-01-01T10:00:00Z",
    "is_active": true
  }
]
```

---

### 8. Create Education
**Endpoint:** `POST /api/profile/education/`  
**Authentication:** Required (Candidate only)

**Request Body:**
```json
{
  "level": "BACHELOR",
  "field_of_study": "Computer Science",
  "institution": "MIT",
  "start_date": "2010-09-01",
  "end_date": "2014-06-01",
  "description": "Bachelor's degree with focus on algorithms and data structures"
}
```

---

### 9. Update Education
**Endpoint:** `PATCH /api/profile/education/{id}/` or `PUT /api/profile/education/{id}/`  
**Authentication:** Required (Candidate only)

---

### 10. Delete Education
**Endpoint:** `DELETE /api/profile/education/{id}/`  
**Authentication:** Required (Candidate only)

---

### 11. List Certifications
**Endpoint:** `GET /api/profile/certifications/`  
**Authentication:** Required (Candidate only)

**Success Response (200):**
```json
[
  {
    "id": 1,
    "name": "AWS Solutions Architect",
    "issuing_organization": "Amazon Web Services",
    "issue_date": "2020-05-01",
    "expiry_date": "2023-05-01",
    "credential_url": "https://aws.amazon.com/...",
    "credential_id": "AWS-123456",
    "created_at": "2024-01-01T10:00:00Z"
  }
]
```

---

### 12. Create Certification
**Endpoint:** `POST /api/profile/certifications/`  
**Authentication:** Required (Candidate only)

**Request Body:**
```json
{
  "name": "AWS Solutions Architect",
  "issuing_organization": "Amazon Web Services",
  "issue_date": "2020-05-01",
  "expiry_date": "2023-05-01",
  "credential_url": "https://aws.amazon.com/verify/12345",
  "credential_id": "AWS-123456"
}
```

---

### 13. Update Certification
**Endpoint:** `PATCH /api/profile/certifications/{id}/` or `PUT /api/profile/certifications/{id}/`  
**Authentication:** Required (Candidate only)

---

### 14. Delete Certification
**Endpoint:** `DELETE /api/profile/certifications/{id}/`  
**Authentication:** Required (Candidate only)

---

## Skills Management

### 15. List All Skills
**Endpoint:** `GET /api/skills/`  
**Authentication:** Not required

**Success Response (200):**
```json
[
  {
    "id": 1,
    "name": "Python",
    "category": "Programming Language",
    "description": "High-level programming language",
    "created_at": "2024-01-01T10:00:00Z"
  }
]
```

---

### 16. Create Skill (Admin only)
**Endpoint:** `POST /api/skills/`  
**Authentication:** Required (Admin only)

**Request Body:**
```json
{
  "name": "Python",
  "category": "Programming Language",
  "description": "High-level programming language"
}
```

---

### 17. List Candidate Skills
**Endpoint:** `GET /api/profile/skills/`  
**Authentication:** Required (Candidate only)

**Success Response (200):**
```json
[
  {
    "id": 1,
    "skill": {
      "id": 1,
      "name": "Python",
      "category": "Programming Language"
    },
    "created_at": "2024-01-05T10:00:00Z"
  }
]
```

---

### 18. Add Skill to Profile
**Endpoint:** `POST /api/profile/skills/`  
**Authentication:** Required (Candidate only)

**Request Body:**
```json
{
  "skill_id": 1
}
```

---

### 19. Remove Skill from Profile
**Endpoint:** `DELETE /api/profile/skills/{id}/`  
**Authentication:** Required (Candidate only)

---

## Job Categories

### 20. List Categories
**Endpoint:** `GET /api/categories/`  
**Authentication:** Not required

**Success Response (200):**
```json
[
  {
    "id": 1,
    "name": "Software Development",
    "slug": "software-development",
    "description": "Jobs related to software development",
    "parent": null,
    "subcategories": [
      {
        "id": 2,
        "name": "Backend Development",
        "slug": "backend-development"
      }
    ],
    "icon": "💻",
    "created_at": "2024-01-01T10:00:00Z"
  }
]
```

---

### 21. Create Category (Admin only)
**Endpoint:** `POST /api/categories/`  
**Authentication:** Required (Admin only)

**Request Body:**
```json
{
  "name": "Software Development",
  "description": "Jobs related to software development",
  "parent": null,
  "icon": "💻"
}
```

---

### 22. Update Category (Admin only)
**Endpoint:** `PATCH /api/categories/{id}/` or `PUT /categories/{id}/`  
**Authentication:** Required (Admin only)

---

### 23. Delete Category (Admin only)
**Endpoint:** `DELETE /api/categories/{id}/`  
**Authentication:** Required (Admin only)

---

## Job Management

### 24. List All Active Jobs
**Endpoint:** `GET /api/jobs/`  
**Authentication:** Not required

**Query Parameters:**
- `employment_type` (optional): FULL_TIME, PART_TIME, CONTRACT, INTERNSHIP, FREELANCE
- `job_type` (optional): REMOTE, ON_SITE, HYBRID
- `experience_level` (optional): ENTRY, INTERMEDIATE, SENIOR, LEAD, EXECUTIVE
- `city` (optional): Filter by city
- `category` (optional): Filter by category ID

**Success Response (200):**
```json
[
  {
    "id": 1,
    "title": "Senior Backend Developer",
    "employer": {
      "id": 2,
      "company_name": "Tech Corp",
      "logo": "http://localhost:8000/media/companies/logos/logo.png"
    },
    "employment_type": "FULL_TIME",
    "job_type": "REMOTE",
    "experience_level": "SENIOR",
    "location": "San Francisco, CA",
    "city": "San Francisco",
    "state": "California",
    "country": "USA",
    "salary_min": 100000.00,
    "salary_max": 150000.00,
    "currency": "USD",
    "is_salary_disclosed": true,
    "status": "ACTIVE",
    "posted_at": "2024-01-15T10:00:00Z",
    "application_deadline": "2024-02-15",
    "applications_count": 25
  }
]
```

---

### 25. Get Job Details
**Endpoint:** `GET /api/jobs/{id}/`  
**Authentication:** Not required

**Success Response (200):**
```json
{
  "id": 1,
  "employer": {
    "id": 2,
    "company_name": "Tech Corp",
    "logo": "http://localhost:8000/media/companies/logos/logo.png",
    "industry": "Technology",
    "company_size": "51-200",
    "website_url": "https://techcorp.com",
    "is_verified": true
  },
  "posted_by": {
    "id": 2,
    "company_name": "Tech Corp"
  },
  "title": "Senior Backend Developer",
  "description": "We are looking for an experienced backend developer to join our growing team. You will be responsible for designing, developing, and maintaining scalable backend services that power our platform.",
  "responsibilities": [
    "Design and develop scalable backend services",
    "Collaborate with frontend team to integrate APIs",
    "Write clean, maintainable, and well-documented code",
    "Code review and mentoring junior developers",
    "Participate in architectural decisions"
  ],
  "requirements": [
    "5+ years of Python/Django experience",
    "Strong understanding of REST APIs and microservices",
    "Experience with PostgreSQL or similar relational databases",
    "Excellent problem-solving skills",
    "Bachelor's degree in Computer Science or related field"
  ],
  "nice_to_have": [
    "Experience with Docker and Kubernetes",
    "Frontend development skills (React, Vue)",
    "AWS or cloud platform experience",
    "Open source contributions"
  ],
  "benefits": [
    "Competitive salary and equity",
    "Health, dental, and vision insurance",
    "401k matching up to 6%",
    "Remote work options",
    "Professional development budget of $5000/year",
    "Flexible working hours",
    "25 days PTO plus holidays"
  ],
  "employment_type": "FULL_TIME",
  "job_type": "REMOTE",
  "experience_level": "SENIOR",
  "salary_min": 100000.00,
  "salary_max": 150000.00,
  "currency": "USD",
  "is_salary_disclosed": true,
  "location": "San Francisco, CA (Remote)",
  "city": "San Francisco",
  "state": "California",
  "country": "USA",
  "categories": [
    {
      "id": 1,
      "name": "Software Development",
      "slug": "software-development",
      "description": "Jobs related to software development"
    },
    {
      "id": 2,
      "name": "Backend Development",
      "slug": "backend-development",
      "parent": 1
    }
  ],
  "required_skills": [
    {
      "id": 1,
      "skill": {
        "id": 1,
        "name": "Python",
        "category": "Programming Language",
        "description": "High-level programming language"
      },
      "is_required": true,
      "minimum_years": 5
    },
    {
      "id": 2,
      "skill": {
        "id": 2,
        "name": "Django",
        "category": "Web Framework"
      },
      "is_required": true,
      "minimum_years": 3
    }
  ],
  "application_deadline": "2024-02-15",
  "status": "ACTIVE",
  "applications_count": 25,
  "posted_at": "2024-01-15T10:00:00Z",
  "expires_at": "2024-02-15T23:59:59Z",
  "created_at": "2024-01-10T09:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z",
  "is_active": true
}
```

**Response Fields Explained:**
- `employer`: Main employer profile (ForeignKey to EmployerProfile)
- `posted_by`: Could be same as employer or different (ForeignKey, nullable)
- `title`: Job title (max 200 chars)
- `description`: Full job description (text field)
- `responsibilities`: JSON array of responsibility strings
- `requirements`: JSON array of requirement strings
- `nice_to_have`: JSON array of optional qualification strings
- `benefits`: JSON array of benefit strings
- `employment_type`: Type of employment (FULL_TIME, PART_TIME, CONTRACT, INTERNSHIP, FREELANCE)
- `job_type`: Work location type (REMOTE, ON_SITE, HYBRID) - based on LocationType choices
- `experience_level`: Required experience (ENTRY, INTERMEDIATE, SENIOR, LEAD, EXECUTIVE)
- `salary_min`/`salary_max`: Salary range (decimal, nullable)
- `currency`: 3-letter currency code (default: USD)
- `is_salary_disclosed`: Whether salary is shown publicly (boolean)
- `location`: Full location string (max 200 chars)
- `city`, `state`, `country`: Structured location fields (max 100 chars each)
- `categories`: ManyToMany relation to Category model
- `required_skills`: ManyToMany through JobSkill model with additional fields
- `application_deadline`: Last date to apply (date field, nullable)
- `status`: Current status (DRAFT, ACTIVE, CLOSED, EXPIRED)
- `applications_count`: Number of applications received (integer, default: 0)
- `posted_at`: When job was posted (datetime, nullable)
- `expires_at`: When job posting expires (datetime, nullable)
- `created_at`: When record was created (auto_now_add from BaseModel)
- `updated_at`: When record was last updated (auto_now from BaseModel)
- `is_active`: Soft delete flag (boolean from BaseModel, default: true)

---

### 26. Create Job Posting
**Endpoint:** `POST /api/jobs/`  
**Authentication:** Required (Employer only)

**Request Body:**
```json
{
  "title": "Senior Backend Developer",
  "description": "We are looking for an experienced backend developer to join our team...",
  "responsibilities": [
    "Design and develop scalable backend services",
    "Lead code reviews and mentor junior developers",
    "Collaborate with cross-functional teams"
  ],
  "requirements": [
    "5+ years of Python/Django experience",
    "Strong understanding of REST APIs",
    "Experience with PostgreSQL or similar databases"
  ],
  "nice_to_have": [
    "Experience with Docker and Kubernetes",
    "Frontend development skills",
    "AWS or cloud platform experience"
  ],
  "benefits": [
    "Competitive salary",
    "Health insurance",
    "Remote work options",
    "Professional development budget"
  ],
  "employment_type": "FULL_TIME",
  "job_type": "REMOTE",
  "experience_level": "SENIOR",
  "salary_min": 100000.00,
  "salary_max": 150000.00,
  "currency": "USD",
  "is_salary_disclosed": true,
  "location": "San Francisco, CA",
  "city": "San Francisco",
  "state": "California",
  "country": "USA",
  "application_deadline": "2024-03-15",
  "status": "DRAFT"
}
```

**Field Descriptions:**
- `title` (string, required, max 200 chars): Job title
- `description` (string, required): Detailed job description
- `responsibilities` (array of strings, optional): List of job responsibilities
- `requirements` (array of strings, optional): List of job requirements
- `nice_to_have` (array of strings, optional): Optional qualifications
- `benefits` (array of strings, optional): List of benefits offered
- `employment_type` (string, required): FULL_TIME | PART_TIME | CONTRACT | INTERNSHIP | FREELANCE
- `job_type` (string, required): REMOTE | ON_SITE | HYBRID
- `experience_level` (string, required): ENTRY | INTERMEDIATE | SENIOR | LEAD | EXECUTIVE
- `salary_min` (decimal, optional): Minimum salary
- `salary_max` (decimal, optional): Maximum salary
- `currency` (string, optional, default: "USD", max 3 chars): Currency code
- `is_salary_disclosed` (boolean, optional, default: false): Whether to show salary publicly
- `location` (string, optional, max 200 chars): Full location description
- `city` (string, optional, max 100 chars): City name
- `state` (string, optional, max 100 chars): State/Province
- `country` (string, optional, max 100 chars): Country name
- `application_deadline` (date, optional): Deadline for applications (YYYY-MM-DD)
- `status` (string, optional, default: "DRAFT"): DRAFT | ACTIVE | CLOSED | EXPIRED

**Note:** Categories and skills are managed separately via many-to-many relationships:
- Add categories: Include `categories` array with category IDs
- Add skills: Use the `/jobs/{id}/skills/` endpoint after creation

---

### 27. Update Job
**Endpoint:** `PATCH /api/jobs/{id}/` or `PUT /api/jobs/{id}/`  
**Authentication:** Required (Employer only, must own the job)

---

### 28. Delete Job
**Endpoint:** `DELETE /api/jobs/{id}/`  
**Authentication:** Required (Employer only, must own the job)

---

### 29. Apply for Job
**Endpoint:** `POST /api/jobs/{id}/apply/`  
**Authentication:** Required (Candidate only)  
**Content-Type:** `multipart/form-data`

**Request Body:**
```
cover_letter: I am very interested in this position...
resume: <file> (optional)
expected_salary: 120000.00
available_from: 2024-03-01
```

**Success Response (201):**
```json
{
  "message": "Application submitted successfully",
  "application_id": 1,
  "status": "PENDING"
}
```

---

### 30. Add Skills to Job (Employer)
**Endpoint:** `POST /api/jobs/{id}/skills/`  
**Authentication:** Required (Employer only)

**Request Body:**
```json
{
  "skill_id": 1,
  "is_required": true,
  "minimum_years": 5
}
```

---

## Application Management

### 31. Get User Applications
**Endpoint:** `GET /api/auth/applications/`  
**Authentication:** Required

Returns candidate's applications or employer's received applications based on user role.

---

### 32. Get Application Details
**Endpoint:** `GET /api/applications/{id}/`  
**Authentication:** Required (Candidate who applied or Employer who owns the job)

**Success Response (200):**
```json
{
  "id": 1,
  "job": {
    "id": 5,
    "title": "Senior Backend Developer",
    "company": "Tech Corp"
  },
  "candidate": {
    "id": 3,
    "user": {
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe"
    },
    "headline": "Software Engineer",
    "profile_picture": "..."
  },
  "cover_letter": "I am very interested...",
  "resume": "http://localhost:8000/media/applications/resumes/resume.pdf",
  "expected_salary": 120000.00,
  "available_from": "2024-03-01",
  "status": "PENDING",
  "is_withdrawn": false,
  "applied_at": "2024-01-20T14:30:00Z",
  "reviewed_at": null,
  "created_at": "2024-01-20T14:30:00Z"
}
```

---

### 33. Update Application Status (Employer)
**Endpoint:** `PATCH /api/applications/{id}/`  
**Authentication:** Required (Employer who owns the job)

**Request Body:**
```json
{
  "status": "REVIEWED",
  "notes": "Good candidate, schedule interview"
}
```

**Available Status Values:**
- PENDING
- REVIEWED
- SHORTLISTED
- INTERVIEW
- REJECTED
- ACCEPTED
- WITHDRAWN

---

### 34. Withdraw Application (Candidate)
**Endpoint:** `POST /api/applications/{id}/withdraw/`  
**Authentication:** Required (Candidate who applied)

**Success Response (200):**
```json
{
  "message": "Application withdrawn successfully",
  "status": "WITHDRAWN"
}
```

---

### 35. Get Application Status History
**Endpoint:** `GET /api/applications/{id}/history/`  
**Authentication:** Required (Candidate who applied or Employer who owns the job)

**Success Response (200):**
```json
[
  {
    "id": 1,
    "old_status": "PENDING",
    "new_status": "REVIEWED",
    "changed_by": {
      "id": 2,
      "email": "employer@techcorp.com",
      "first_name": "Jane"
    },
    "notes": "Reviewed application, moving to next stage",
    "created_at": "2024-01-21T10:00:00Z"
  }
]
```

---

## Saved Jobs & Job Alerts

### 36. Get Saved Jobs
**Endpoint:** `GET /api/auth/saved_jobs/`  
**Authentication:** Required (Candidate only)

**Success Response (200):**
```json
[
  {
    "id": 1,
    "job": {
      "id": 5,
      "title": "Senior Backend Developer",
      "company": "Tech Corp",
      "location": "San Francisco, CA",
      "salary_min": 100000.00,
      "salary_max": 150000.00
    },
    "notes": "Interesting position, apply by end of month",
    "created_at": "2024-01-18T12:00:00Z"
  }
]
```

---

### 37. Save Job
**Endpoint:** `POST /api/saved-jobs/`  
**Authentication:** Required (Candidate only)

**Request Body:**
```json
{
  "job_id": 5,
  "notes": "Interesting position, matches my skills"
}
```

---

### 38. Update Saved Job Notes
**Endpoint:** `PATCH /api/saved-jobs/{id}/`  
**Authentication:** Required (Candidate only)

**Request Body:**
```json
{
  "notes": "Updated notes about this job"
}
```

---

### 39. Remove Saved Job
**Endpoint:** `DELETE /api/saved-jobs/{id}/`  
**Authentication:** Required (Candidate only)

---

### 40. List Job Alerts
**Endpoint:** `GET /api/job-alerts/`  
**Authentication:** Required (Candidate only)

**Success Response (200):**
```json
[
  {
    "id": 1,
    "alert_name": "Senior Backend Jobs",
    "keywords": "python, django, backend",
    "location": "San Francisco",
    "job_type": "REMOTE",
    "experience_level": "SENIOR",
    "salary_min": 100000.00,
    "is_remote": true,
    "frequency": "DAILY",
    "is_active": true,
    "created_at": "2024-01-15T10:00:00Z"
  }
]
```

---

### 41. Create Job Alert
**Endpoint:** `POST /api/job-alerts/`  
**Authentication:** Required (Candidate only)

**Request Body:**
```json
{
  "alert_name": "Senior Backend Jobs",
  "keywords": "python, django, backend",
  "location": "San Francisco",
  "job_type": "REMOTE",
  "experience_level": "SENIOR",
  "salary_min": 100000.00,
  "is_remote": true,
  "frequency": "DAILY"
}
```

**Frequency Options:**
- INSTANT
- DAILY
- WEEKLY

---

### 42. Update Job Alert
**Endpoint:** `PATCH /api/job-alerts/{id}/` or `PUT /job-alerts/{id}/`  
**Authentication:** Required (Candidate only)

---

### 43. Delete Job Alert
**Endpoint:** `DELETE /api/job-alerts/{id}/`  
**Authentication:** Required (Candidate only)

---

## Company Reviews

### 44. Get User Reviews
**Endpoint:** `GET /api/auth/reviews/`  
**Authentication:** Required

---

### 45. List Company Reviews
**Endpoint:** `GET /api/companies/{id}/reviews/`  
**Authentication:** Not required

**Success Response (200):**
```json
[
  {
    "id": 1,
    "reviewer": {
      "first_name": "John",
      "last_name": "D."
    },
    "rating": 5,
    "review_text": "Great company to work for! Excellent culture and benefits.",
    "created_at": "2024-01-15T10:00:00Z"
  }
]
```

---

### 46. Create Company Review
**Endpoint:** `POST /api/companies/{id}/reviews/`  
**Authentication:** Required

**Request Body:**
```json
{
  "rating": 5,
  "review_text": "Great company to work for! The team is supportive and the work is challenging."
}
```

**Rating:** Integer between 1-5

---

### 47. Update Review
**Endpoint:** `PATCH /api/reviews/{id}/` or `PUT /api/reviews/{id}/`  
**Authentication:** Required (Must be the review author)

---

### 48. Delete Review
**Endpoint:** `DELETE /api/reviews/{id}/`  
**Authentication:** Required (Must be the review author)

---

## Notifications

### 49. Get User Notifications
**Endpoint:** `GET /api/auth/notifications/`  
**Authentication:** Required

**Success Response (200):**
```json
[
  {
    "id": 1,
    "notification_type": "APPLICATION_STATUS",
    "title": "Application Status Updated",
    "content": "Your application for Senior Backend Developer has been reviewed",
    "reference_id": 5,
    "reference_type": "application",
    "is_read": false,
    "read_at": null,
    "created_at": "2024-01-20T15:00:00Z"
  }
]
```

**Notification Types:**
- APPLICATION_STATUS
- NEW_MESSAGE
- JOB_ALERT
- INTERVIEW
- SYSTEM
- APPLICATION

---

### 50. Mark Notification as Read
**Endpoint:** `POST /api/notifications/{id}/mark-read/`  
**Authentication:** Required

**Success Response (200):**
```json
{
  "message": "Notification marked as read",
  "is_read": true,
  "read_at": "2024-01-20T16:00:00Z"
}
```

---

### 51. Mark All Notifications as Read
**Endpoint:** `POST /api/notifications/mark-all-read/`  
**Authentication:** Required

**Success Response (200):**
```json
{
  "message": "All notifications marked as read",
  "count": 10
}
```

---

### 52. Delete Notification
**Endpoint:** `DELETE /api/notifications/{id}/`  
**Authentication:** Required

---

## Address Management

### 53. Get User Address
**Endpoint:** `GET /api/profile/address/`  
**Authentication:** Required

**Success Response (200):**
```json
{
  "id": 1,
  "street": "123 Main Street",
  "city": "San Francisco",
  "state": "California",
  "country": "USA",
  "postal_code": "94102",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-15T14:00:00Z"
}
```

---

### 54. Create/Update Address
**Endpoint:** `POST /api/profile/address/` or `PATCH /api/profile/address/`  
**Authentication:** Required

**Request Body:**
```json
{
  "street": "123 Main Street, Apt 4B",
  "city": "San Francisco",
  "state": "California",
  "country": "USA",
  "postal_code": "94102"
}
```

---

### 55. Delete Address
**Endpoint:** `DELETE /api/profile/address/`  
**Authentication:** Required

---

## Error Responses

All endpoints return standard error responses:

**400 Bad Request:**
```json
{
  "field_name": ["Error message"],
  "another_field": ["Another error message"]
}
```

**401 Unauthorized:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden:**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**404 Not Found:**
```json
{
  "detail": "Not found."
}
```

---

## Enumerations

### User Roles
- `ADMIN` - Administrator
- `EMPLOYER` - Employer/Company
- `CANDIDATE` - Job Seeker

### Gender
- `MALE`
- `FEMALE`
- `OTHER`

### Education Levels
- `HIGH_SCHOOL`
- `ASSOCIATE`
- `BACHELOR`
- `MASTER`
- `PHD`
- `CERTIFICATE`
- `DIPLOMA`

### Employment Types
- `FULL_TIME`
- `PART_TIME`
- `CONTRACT`
- `INTERNSHIP`
- `FREELANCE`

### Location Types (Job Type)
- `REMOTE`
- `ON_SITE`
- `HYBRID`

### Experience Levels
- `ENTRY`
- `INTERMEDIATE`
- `SENIOR`
- `LEAD`
- `EXECUTIVE`

### Job Status
- `DRAFT`
- `ACTIVE`
- `CLOSED`
- `EXPIRED`

### Application Status
- `PENDING`
- `REVIEWED`
- `SHORTLISTED`
- `INTERVIEW`
- `REJECTED`
- `ACCEPTED`
- `WITHDRAWN`

### Company Sizes
- `1-10`
- `11-50`
- `51-200`
- `201-500`
- `500+`

### Job Alert Frequency
- `INSTANT`
- `DAILY`
- `WEEKLY`

### Notification Types
- `APPLICATION_STATUS`
- `NEW_MESSAGE`
- `JOB_ALERT`
- `INTERVIEW`
- `SYSTEM`
- `APPLICATION`

---

## Notes

1. **Model Issues Found:**
   - EmployerProfile.verified() should be @property not a method
   - CandidateProfile uses related_name='candidate' (not 'candidate_profile')
   - JobPosting has redundant employer and posted_by fields
   
2. **Profile Completion:**
   - Candidate profiles calculate completion percentage automatically
   - 100% completion requires all fields filled
   
3. **File Uploads:**
   - Use `multipart/form-data` for profile pictures, resumes, logos
   - Maximum file size should be configured in Django settings
   
4. **Datetime Format:**
   - All datetime fields use ISO 8601 format
   
5. **Soft Deletes:**
   - Most models use `is_active` field for soft deletion
   - Set `is_active=false` instead of hard deleting

6. **Missing Endpoints:**
   - The views.py file doesn't implement endpoints for: Education, Certifications, Skills, Categories, SavedJobs, JobAlerts, Reviews, Notifications, Address
   - These need to be implemented as separate ViewSets

7. **Related Name Inconsistency:**
   - Views access `user.candidate_profile` but model defines `related_name='candidate'`
   - Should be consistent throughout the codebase