# Job Board API Documentation

Base URL: `http://localhost:2000/api/`

## Authentication Endpoints

### 1. Register User
**Endpoint:** `POST /api/auth/register/`

**Permission:** Public (AllowAny)

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "confirm_password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "CANDIDATE" // or "EMPLOYER"
}
```

**Response:** `201 CREATED`
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "CANDIDATE"
  }
}
```

**Error Responses:**
- `400 BAD REQUEST` - If passwords don't match
```json
{
  "detail": "Passwords do not match"
}
```

- `400 BAD REQUEST` - If email already exists
```json
{
  "email": ["user with this email already exists."]
}
```

---

### 2. Login
**Endpoint:** `POST /api/auth/login/`

**Permission:** Public (AllowAny)

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "CANDIDATE"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "dashboard": {
    // Dashboard data from DashboardService
  }
}
```

**Error Responses:**
- `400 BAD REQUEST` - If credentials are invalid
```json
{
  "detail": "Invalid credentials"
}
```

- `400 BAD REQUEST` - If user account is inactive
```json
{
  "detail": "User is not active"
}
```

---

### 3. Get Current User
**Endpoint:** `GET /api/auth/me/`

**Permission:** Authenticated

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "CANDIDATE"
  },
  "dashboard": {
    // Dashboard data
  }
}
```

---

### 4. Refresh Token
**Endpoint:** `POST /api/auth/refresh/`

**Permission:** Public (AllowAny)

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## Job Endpoints

### 5. List All Active Jobs
**Endpoint:** `GET /api/jobs/`

**Permission:** Public (AllowAny)

**Query Parameters:** None

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "Senior Software Engineer",
    "status": "ACTIVE",
    "description": "We are looking for...",
    "requirements": [
      "3+ years Python experience",
      "Django knowledge"
    ],
    "responsibilities": [
      "Design and develop web applications",
      "Write clean code",
      "Collaborate with team"
    ],
    "nice_to_have": [
      "React experience"
    ],
    "job_type": "FULL_TIME",
    "experience_level": "SENIOR",
    "salary_min": 80000.00,
    "salary_max": 120000.00,
    "benefits": [
      "Health insurance",
      "Remote work"
    ],
    "is_remote": true,
    "is_hybrid": false,
    "city": "San Francisco",
    "country": "USA",
    "applications_count": 15,
    "application_deadline": "2026-02-28T23:59:59Z",
    "created_at": "2026-01-27T10:00:00Z",
    "updated_at": "2026-01-27T10:00:00Z"
  }
]
```

---

### 6. Get Active Jobs (Alternative)
**Endpoint:** `GET /api/jobs/get_jobs/`

**Permission:** Public (AllowAny)

**Response:** Same as endpoint #5

---

### 7. Get Single Job
**Endpoint:** `GET /api/jobs/{id}/`

**Permission:** Public (AllowAny)

**Example:** `GET /api/jobs/1/`

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Senior Software Engineer",
  "status": "ACTIVE",
  "description": "We are looking for...",
  "requirements": [
    "3+ years Python experience",
    "Django knowledge"
  ],
  "responsibilities": [
    "Design and develop web applications",
    "Write clean code"
  ],
  "nice_to_have": [
    "React experience",
    "AWS knowledge"
  ],
  "job_type": "FULL_TIME",
  "experience_level": "SENIOR",
  "salary_min": 80000.00,
  "salary_max": 120000.00,
  "benefits": [
    "Health insurance",
    "Remote work",
    "401k matching"
  ],
  "is_remote": true,
  "is_hybrid": false,
  "city": "San Francisco",
  "country": "USA",
  "applications_count": 15,
  "application_deadline": "2026-02-28T23:59:59Z",
  "created_at": "2026-01-27T10:00:00Z",
  "updated_at": "2026-01-27T10:00:00Z"
}
```

---

### 8. Create Job Posting
**Endpoint:** `POST /api/jobs/`

**Permission:** Authenticated

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Senior Software Engineer",
  "description": "We are looking for a talented developer...",
  "status": "ACTIVE",
  "job_type": "FULL_TIME",
  "experience_level": "SENIOR",
  "salary_min": 80000,
  "salary_max": 120000,
  "is_remote": true,
  "is_hybrid": false,
  "city": "San Francisco",
  "country": "USA",
  "application_deadline": "2026-02-28T23:59:59Z",
  "responsibilities": [
    "Design and develop web applications",
    "Write clean, maintainable code"
  ],
  "requirements": [
    "3+ years Python experience",
    "Strong Django knowledge"
  ],
  "nice_to_have": [
    "React experience",
    "AWS knowledge"
  ],
  "benefits": [
    "Health insurance",
    "Remote work",
    "401k matching"
  ]
}
```

**Response:** `201 CREATED`
```json
{
  "id": 1,
  "title": "Senior Software Engineer",
  "description": "We are looking for a talented developer...",
  "status": "ACTIVE",
  "created_at": "2026-01-27T10:00:00Z",
  "updated_at": "2026-01-27T10:00:00Z"
}
```

**Error Response:**
- `400 BAD REQUEST` - If user is not an employer
```json
{
  "non_field_errors": ["Only employers can create job postings"]
}
```

---

### 9. Update Job Posting (Partial)
**Endpoint:** `PATCH /api/jobs/{id}/`

**Permission:** Authenticated

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Example:** `PATCH /api/jobs/1/`

**Request Body:** (only include fields you want to update)
```json
{
  "status": "CLOSED",
  "description": "Updated description"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Senior Software Engineer",
  "description": "Updated description",
  "status": "CLOSED",
  "created_at": "2026-01-27T10:00:00Z",
  "updated_at": "2026-01-27T12:00:00Z"
}
```

---

### 10. Update Job Posting (Full)
**Endpoint:** `PUT /api/jobs/{id}/`

**Permission:** Authenticated

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:** (must include all required fields)
```json
{
  "title": "Senior Software Engineer",
  "description": "Updated full description",
  "status": "ACTIVE",
  // ... all required fields
}
```

**Response:** `200 OK`

---

### 11. Delete Job Posting
**Endpoint:** `DELETE /api/jobs/{id}/`

**Permission:** Authenticated

**Headers:**
```
Authorization: Bearer <access_token>
```

**Example:** `DELETE /api/jobs/1/`

**Response:** `204 NO CONTENT`

---

### 12. Apply to Job
**Endpoint:** `POST /api/jobs/{id}/apply/`

**Permission:** Authenticated (Candidate only)

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Example:** `POST /api/jobs/1/apply/`

**Request Body:** (multipart/form-data)
```
cover_letter: "I am very interested in this position..."
resume: <file>
```

**Note:** The `job` and `candidate` fields are automatically set from context, not from request data.

**Response:** `201 CREATED`
```json
{
  "message": "Application submitted successfully",
  "application_id": 1,
  "status": "PENDING"
}
```

**Error Responses:**
- `400 BAD REQUEST` - If user is not a candidate
```json
{
  "non_field_errors": ["Only candidates can apply for job"]
}
```

- `400 BAD REQUEST` - If job is not accepting applications
```json
{
  "non_field_errors": ["This job is no more acepting applications"]
}
```

- `400 BAD REQUEST` - If already applied
```json
{
  "non_field_errors": ["You have already applied for this job"]
}
```

- `400 BAD REQUEST` - If not authenticated or not a candidate
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## Complete API Endpoints Summary

### Authentication
| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| POST | `/api/auth/register/` | Public | Register new user |
| POST | `/api/auth/login/` | Public | Login user |
| GET | `/api/auth/me/` | Authenticated | Get current user |
| POST | `/api/auth/refresh/` | Public | Refresh access token |

### Jobs
| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| GET | `/api/jobs/` | Public | List all active jobs |
| POST | `/api/jobs/` | Authenticated | Create new job |
| GET | `/api/jobs/{id}/` | Public | Get single job |
| PUT | `/api/jobs/{id}/` | Authenticated | Full update job |
| PATCH | `/api/jobs/{id}/` | Authenticated | Partial update job |
| DELETE | `/api/jobs/{id}/` | Authenticated | Delete job |
| GET | `/api/jobs/get_jobs/` | Public | List active jobs (alt) |
| POST | `/api/jobs/{id}/apply/` | Authenticated | Apply to job |

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error."
}
```

---

## Authentication Flow

1. **Register:** `POST /api/auth/register/`
2. **Login:** `POST /api/auth/login/` → Get access & refresh tokens
3. **Use Access Token:** Include in header: `Authorization: Bearer <access_token>`
4. **Refresh Token:** When access expires, `POST /api/auth/refresh/` with refresh token
5. **Get User Info:** `GET /api/auth/me/`

---

## Job Application Flow

1. **Browse Jobs:** `GET /api/jobs/`
2. **View Job Details:** `GET /api/jobs/{id}/`
3. **Login/Register:** If not authenticated
4. **Apply:** `POST /api/jobs/{id}/apply/` with cover letter and resume

---

## Notes

- All timestamps are in ISO 8601 format (UTC)
- File uploads use `multipart/form-data` encoding
- JSON fields (responsibilities, requirements, nice_to_have, benefits) accept arrays of strings
- Job status options: `ACTIVE`, `CLOSED`, `DRAFT`, etc. (check JobPosting.Status enum)
- Job type options: `FULL_TIME`, `PART_TIME`, `CONTRACT`, `INTERNSHIP`
- Experience level options: `ENTRY`, `JUNIOR`, `SENIOR`, `LEAD`, `MANAGER`
- User roles: `CANDIDATE`, `EMPLOYER`
- Application status: `PENDING`, `REVIEWED`, `SHORTLISTED`, `INTERVIEW`, `REJECTED`, `ACCEPTED`, `WITHDRAWN`
- Password validation: Passwords must match in registration
- Only employers can create job postings
- Only candidates can apply to jobs
- Users cannot apply to the same job twice
