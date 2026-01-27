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
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "candidate" // or "employer"
}
```

**Response:** `201 CREATED`
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "candidate"
  }
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
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "candidate"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "dashboard": {
    // Dashboard data from DashboardService
  }
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
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "candidate"
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
    "description": "We are looking for...",
    "status": "ACTIVE",
    "responsibilities": [
      "Design and develop web applications",
      "Write clean code",
      "Collaborate with team"
    ],
    "requirements": [
      "3+ years Python experience",
      "Django knowledge"
    ],
    "nice_to_have": [
      "React experience"
    ],
    "benefits": [
      "Health insurance",
      "Remote work"
    ],
    "created_at": "2026-01-27T10:00:00Z",
    "updated_at": "2026-01-27T10:00:00Z"
    // ... all other fields from GetJobSerializer
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
  "description": "We are looking for...",
  "status": "ACTIVE",
  "responsibilities": [
    "Design and develop web applications"
  ],
  "requirements": [
    "3+ years Python experience"
  ],
  "nice_to_have": [
    "React experience"
  ],
  "benefits": [
    "Health insurance"
  ],
  "created_at": "2026-01-27T10:00:00Z",
  "updated_at": "2026-01-27T10:00:00Z"
  // ... all other fields
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
  "employment_type": "FULL_TIME",
  "experience_level": "SENIOR",
  "location": "Remote",
  "salary_min": 80000,
  "salary_max": 120000,
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
  // ... all fields
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
  "status": "CLOSED",
  "description": "Updated description",
  // ... all other fields
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
expected_salary: 100000
available_from: "2026-02-01"
```

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
  "non_field_errors": ["This job is no more accepting applications"]
}
```

- `400 BAD REQUEST` - If already applied
```json
{
  "non_field_errors": ["You have already applied for this job"]
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

1. **Browse Jobs:** `GET /api/jobs/` or `GET /api/jobs/get_jobs/`
2. **View Job Details:** `GET /api/jobs/{id}/`
3. **Login/Register:** If not authenticated
4. **Apply:** `POST /api/jobs/{id}/apply/` with cover letter and resume

---

## Notes

- All timestamps are in ISO 8601 format (UTC)
- File uploads use `multipart/form-data` encoding
- JSON fields (responsibilities, requirements, etc.) accept arrays
- Job status options: `ACTIVE`, `CLOSED`, `DRAFT`, `ARCHIVED`
- User types: `candidate`, `employer`
- Application status: `PENDING`, `REVIEWED`, `SHORTLISTED`, `INTERVIEW`, `REJECTED`, `ACCEPTED`, `WITHDRAWN`