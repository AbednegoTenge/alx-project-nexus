# Job Portal API Documentation

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

## Endpoints Overview

### Authentication Endpoints
- `POST /auth/login/` - User login
- `POST /auth/register/` - User registration
- `POST /auth/refresh/` - Refresh access token
- `GET /auth/me/` - Get current user info
- `GET /auth/profile/` - Get current user's profile
- `PATCH /auth/update_profile/` - Update current user's profile
- `PUT /auth/update_profile/` - Replace current user's profile
- `GET /auth/applications/` - Get user's applications
- `GET /auth/notifications/` - Get user's notifications
- `GET /auth/reviews/` - Get user's reviews
- `GET /auth/saved_jobs/` - Get user's saved jobs

### Job Endpoints
- `GET /jobs/` - List all active jobs
- `GET /jobs/{id}/` - Get job details
- `POST /jobs/` - Create a new job (Employer only)
- `PUT /jobs/{id}/` - Update job (Employer only)
- `PATCH /jobs/{id}/` - Partial update job (Employer only)
- `DELETE /jobs/{id}/` - Delete job (Employer only)
- `POST /jobs/{id}/apply/` - Apply for a job

---

## Detailed Endpoint Documentation

### 1. User Registration

**Endpoint:** `POST /auth/register/`

**Description:** Register a new user account (Candidate or Employer)

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

**Request Fields:**
- `email` (string, required): User's email address
- `password` (string, required): User's password
- `password2` (string, required): Password confirmation
- `first_name` (string, optional): User's first name
- `last_name` (string, optional): User's last name
- `role` (string, required): User role - `CANDIDATE`, `EMPLOYER`, or `ADMIN`

**Success Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "CANDIDATE",
    "is_active": true
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "email": ["User with this email already exists."],
  "password": ["Passwords do not match."]
}
```

---

### 2. User Login

**Endpoint:** `POST /auth/login/`

**Description:** Authenticate user and receive JWT tokens

**Authentication:** Not required

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Request Fields:**
- `email` (string, required): User's email address
- `password` (string, required): User's password

**Success Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "CANDIDATE",
    "is_active": true
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Invalid email or password"
}
```

---

### 3. Refresh Token

**Endpoint:** `POST /auth/refresh/`

**Description:** Get a new access token using refresh token

**Authentication:** Not required

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Success Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 4. Get Current User

**Endpoint:** `GET /auth/me/`

**Description:** Get current authenticated user's information

**Authentication:** Required

**Success Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "CANDIDATE",
    "is_active": true
  }
}
```

---

### 5. Get User Profile

**Endpoint:** `GET /auth/profile/`

**Description:** Get detailed profile of current user (Candidate or Employer)

**Authentication:** Required

**Success Response for Candidate (200 OK):**
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
  "about": "Experienced software engineer with 5+ years...",
  "linkedin": "https://linkedin.com/in/johndoe",
  "github": "https://github.com/johndoe",
  "twitter": "https://twitter.com/johndoe",
  "website": "https://johndoe.com",
  "profile_picture": "http://localhost:8000/media/profiles/pictures/photo.jpg",
  "resume": "http://localhost:8000/media/profiles/resumes/resume.pdf",
  "is_verified": false,
  "profile_completion": 85,
  "candidate_skills": [
    {
      "id": 1,
      "skill": {
        "id": 1,
        "name": "Python",
        "category": "Programming"
      }
    }
  ],
  "education": [
    {
      "id": 1,
      "level": "BACHELOR",
      "field_of_study": "Computer Science",
      "institution": "MIT",
      "start_date": "2010-09-01",
      "end_date": "2014-06-01",
      "description": "Bachelor's degree in Computer Science"
    }
  ],
  "certifications": [
    {
      "id": 1,
      "name": "AWS Solutions Architect",
      "issuing_organization": "Amazon Web Services",
      "issue_date": "2020-05-01",
      "expiry_date": "2023-05-01",
      "credential_url": "https://aws.amazon.com/...",
      "credential_id": "AWS-123456"
    }
  ]
}
```

**Success Response for Employer (200 OK):**
```json
{
  "id": 1,
  "user": {
    "id": 2,
    "email": "employer@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "role": "EMPLOYER"
  },
  "company_name": "Tech Corp",
  "company_size": "51-200",
  "industry": "Technology",
  "description": "Leading technology company...",
  "website_url": "https://techcorp.com",
  "linkedin_url": "https://linkedin.com/company/techcorp",
  "logo": "http://localhost:8000/media/companies/logos/logo.png",
  "cover_image": "http://localhost:8000/media/companies/covers/cover.jpg",
  "headquarters_address": "123 Tech Street",
  "city": "San Francisco",
  "state": "California",
  "country": "USA",
  "postal_code": "94102",
  "phone": "+1234567890",
  "contact_email": "contact@techcorp.com",
  "is_verified": true,
  "verified_at": "2024-01-15T10:30:00Z"
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "Candidate profile not found"
}
```

---

### 6. Update User Profile

**Endpoint:** `PATCH /auth/update_profile/` or `PUT /auth/update_profile/`

**Description:** Update current user's profile (partial update with PATCH, full update with PUT)

**Authentication:** Required

**Content-Type:** `multipart/form-data` (for file uploads)

**Request Body (Candidate - multipart/form-data):**
```
phone: +1234567890
gender: MALE
date_of_birth: 1990-01-15
headline: Senior Software Engineer
about: Experienced developer...
linkedin: https://linkedin.com/in/johndoe
profile_picture: <file>
resume: <file>
```

**Request Body (Employer - multipart/form-data):**
```
company_name: Tech Corp
company_size: 51-200
industry: Technology
description: Leading tech company...
website_url: https://techcorp.com
logo: <file>
cover_image: <file>
city: San Francisco
state: California
country: USA
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "phone": "+1234567890",
  "headline": "Senior Software Engineer",
  ...
}
```

---

### 7. Get User Applications

**Endpoint:** `GET /auth/applications/`

**Description:** Get all applications for the current user (candidate's applications or employer's received applications)

**Authentication:** Required

**Success Response for Candidate (200 OK):**
```json
[
  {
    "id": 1,
    "job": {
      "id": 5,
      "title": "Senior Backend Developer",
      "company": "Tech Corp",
      "location": "San Francisco, CA"
    },
    "status": "PENDING",
    "cover_letter": "I am very interested...",
    "expected_salary": 120000.00,
    "applied_at": "2024-01-20T14:30:00Z"
  }
]
```

**Success Response for Employer (200 OK):**
```json
[
  {
    "id": 1,
    "job": {
      "id": 5,
      "title": "Senior Backend Developer"
    },
    "candidate": {
      "id": 3,
      "name": "John Doe",
      "email": "john@example.com",
      "headline": "Software Engineer"
    },
    "status": "PENDING",
    "applied_at": "2024-01-20T14:30:00Z"
  }
]
```

---

### 8. Get User Notifications

**Endpoint:** `GET /auth/notifications/`

**Description:** Get all notifications for the current user

**Authentication:** Required

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "notification_type": "APPLICATION_STATUS",
    "title": "Application Status Updated",
    "content": "Your application for Senior Backend Developer has been reviewed",
    "is_read": false,
    "created_at": "2024-01-20T15:00:00Z"
  }
]
```

---

### 9. Get User Reviews

**Endpoint:** `GET /auth/reviews/`

**Description:** Get all reviews written by or about the current user

**Authentication:** Required

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "company": {
      "id": 2,
      "company_name": "Tech Corp"
    },
    "rating": 5,
    "review_text": "Great company to work for!",
    "created_at": "2024-01-15T10:00:00Z"
  }
]
```

---

### 10. Get Saved Jobs

**Endpoint:** `GET /auth/saved_jobs/`

**Description:** Get all jobs saved by the current user

**Authentication:** Required

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "job": {
      "id": 5,
      "title": "Senior Backend Developer",
      "company": "Tech Corp",
      "location": "San Francisco, CA",
      "employment_type": "FULL_TIME",
      "salary_min": 100000.00,
      "salary_max": 150000.00
    },
    "notes": "Interesting position, apply by end of month",
    "created_at": "2024-01-18T12:00:00Z"
  }
]
```

---

### 11. List Jobs

**Endpoint:** `GET /jobs/`

**Description:** Get list of all active job postings

**Authentication:** Not required

**Query Parameters:**
- None (returns all active jobs)

**Success Response (200 OK):**
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

### 12. Get Job Details

**Endpoint:** `GET /jobs/{id}/`

**Description:** Get detailed information about a specific job

**Authentication:** Not required

**Success Response (200 OK):**
```json
{
  "id": 1,
  "title": "Senior Backend Developer",
  "description": "We are looking for an experienced backend developer...",
  "responsibilities": [
    "Design and develop scalable backend services",
    "Collaborate with frontend team",
    "Code review and mentoring"
  ],
  "requirements": [
    "5+ years of Python/Django experience",
    "Strong understanding of REST APIs",
    "Experience with PostgreSQL"
  ],
  "nice_to_have": [
    "Experience with Docker and Kubernetes",
    "Frontend development skills"
  ],
  "benefits": [
    "Health insurance",
    "401k matching",
    "Remote work options",
    "Professional development budget"
  ],
  "employer": {
    "id": 2,
    "company_name": "Tech Corp",
    "logo": "http://localhost:8000/media/companies/logos/logo.png",
    "industry": "Technology",
    "company_size": "51-200",
    "website_url": "https://techcorp.com"
  },
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
  "categories": [
    {
      "id": 1,
      "name": "Software Development",
      "slug": "software-development"
    }
  ],
  "required_skills": [
    {
      "id": 1,
      "skill": {
        "id": 1,
        "name": "Python",
        "category": "Programming"
      },
      "is_required": true,
      "minimum_years": 5
    },
    {
      "id": 2,
      "skill": {
        "id": 2,
        "name": "Django",
        "category": "Framework"
      },
      "is_required": true,
      "minimum_years": 3
    }
  ],
  "status": "ACTIVE",
  "applications_count": 25,
  "posted_at": "2024-01-15T10:00:00Z",
  "application_deadline": "2024-02-15",
  "expires_at": "2024-02-15T23:59:59Z"
}
```

---

### 13. Create Job Posting

**Endpoint:** `POST /jobs/`

**Description:** Create a new job posting (Employer only)

**Authentication:** Required (Employer role)

**Request Body:**
```json
{
  "title": "Senior Backend Developer",
  "description": "We are looking for an experienced backend developer...",
  "responsibilities": [
    "Design and develop scalable backend services",
    "Collaborate with frontend team"
  ],
  "requirements": [
    "5+ years of Python/Django experience",
    "Strong understanding of REST APIs"
  ],
  "nice_to_have": [
    "Experience with Docker and Kubernetes"
  ],
  "benefits": [
    "Health insurance",
    "401k matching"
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
  "application_deadline": "2024-02-15",
  "status": "DRAFT"
}
```

**Success Response (201 Created):**
```json
{
  "id": 1,
  "title": "Senior Backend Developer",
  "status": "DRAFT",
  ...
}
```

---

### 14. Update Job Posting

**Endpoint:** `PUT /jobs/{id}/` or `PATCH /jobs/{id}/`

**Description:** Update job posting (Employer only, must own the job)

**Authentication:** Required (Employer role)

**Request Body (same as Create Job):**

**Success Response (200 OK):**
```json
{
  "id": 1,
  "title": "Senior Backend Developer",
  ...
}
```

---

### 15. Delete Job Posting

**Endpoint:** `DELETE /jobs/{id}/`

**Description:** Delete job posting (Employer only, must own the job)

**Authentication:** Required (Employer role)

**Success Response (204 No Content):**
No response body

---

### 16. Apply for Job

**Endpoint:** `POST /jobs/{id}/apply/`

**Description:** Submit an application for a job posting

**Authentication:** Required (Candidate role)

**Content-Type:** `multipart/form-data`

**Request Body (multipart/form-data):**
```
cover_letter: I am very interested in this position...
resume: <file> (optional if already uploaded to profile)
expected_salary: 120000.00
available_from: 2024-03-01
```

**Request Fields:**
- `cover_letter` (string, optional): Cover letter text
- `resume` (file, optional): Resume file upload
- `expected_salary` (decimal, optional): Expected salary
- `available_from` (date, optional): Availability start date

**Success Response (201 Created):**
```json
{
  "message": "Application submitted successfully",
  "application_id": 1,
  "status": "PENDING"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "You have already applied for this job"
}
```

---

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Resource deleted successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required or failed
- `403 Forbidden` - User doesn't have permission
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Enumerations

### User Roles
- `ADMIN` - Administrator
- `EMPLOYER` - Employer/Company
- `CANDIDATE` - Job Seeker

### Employment Types
- `FULL_TIME` - Full-time
- `PART_TIME` - Part-time
- `CONTRACT` - Contract
- `INTERNSHIP` - Internship
- `FREELANCE` - Freelance

### Location Types (Job Type)
- `REMOTE` - Remote
- `ON_SITE` - On-site
- `HYBRID` - Hybrid

### Experience Levels
- `ENTRY` - Entry Level
- `INTERMEDIATE` - Intermediate
- `SENIOR` - Senior
- `LEAD` - Lead
- `EXECUTIVE` - Executive

### Job Status
- `DRAFT` - Draft
- `ACTIVE` - Active
- `CLOSED` - Closed
- `EXPIRED` - Expired

### Application Status
- `PENDING` - Pending
- `REVIEWED` - Reviewed
- `SHORTLISTED` - Shortlisted
- `INTERVIEW` - Interview Scheduled
- `REJECTED` - Rejected
- `ACCEPTED` - Accepted
- `WITHDRAWN` - Withdrawn

### Gender
- `MALE` - Male
- `FEMALE` - Female
- `OTHER` - Other

### Education Level
- `HIGH_SCHOOL` - High School
- `ASSOCIATE` - Associate Degree
- `BACHELOR` - Bachelor's Degree
- `MASTER` - Master's Degree
- `PHD` - PhD
- `CERTIFICATE` - Certificate
- `DIPLOMA` - Diploma

### Company Size
- `1-10` - 1-10 employees
- `11-50` - 11-50 employees
- `51-200` - 51-200 employees
- `201-500` - 201-500 employees
- `500+` - 500+ employees

---

## Error Handling

All error responses follow this format:

```json
{
  "field_name": ["Error message"],
  "another_field": ["Another error message"]
}
```

Or for general errors:

```json
{
  "detail": "Error message"
}
```

---

## Notes

1. All datetime fields are in ISO 8601 format (e.g., `2024-01-20T14:30:00Z`)
2. All file uploads should use `multipart/form-data` content type
3. JWT tokens expire after a certain period (configured in Django settings)
4. Refresh tokens can be used to obtain new access tokens
5. Profile completion percentage is automatically calculated for candidates
6. Job application count is automatically updated when applications are submitted