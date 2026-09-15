# SafeSpace Architecture

## Architecture Goal

SafeSpace provides AI-assisted explanations without allowing the AI model to become the source of legal truth.

The system follows the principle:

Verified Source → Structured Rights Record → Controlled Retrieval → AI Explanation → Source Citation → Next Action

## Full Architecture (Day 4)

```
                  USER (mobile-first)
                        |
                        v
              Next.js Frontend (App Router)
              /journeys, /support, /safety
                        |
              NEXT_PUBLIC_API_BASE_URL
                        |
                        v
              Django API (/api/v1/)
              CORS: restricted to frontend origin
                        |
       +----------------+------------------+-----------+
       |                |                  |           |
       v                v                  v           v
 Rights Layer     Action Layer       Support        Safety Layer
       |                |             Layer               |
       v                v                |               v
RightsRecord       ActionPath      SupportService    RiskRule
LegalSource        (+ source)      (verified         (deterministic
(source             (+ service)     contacts)         pattern match)
 provenance)
       \               |                 /              /
        \              |                /              /
         +-------------+---------------+--------------+
                        |
                        v
                   PostgreSQL

AI layer: Day 5+
```

## Components

### Frontend (Day 4)

Technology: Next.js 16 + TypeScript + Tailwind CSS (App Router)

Pages:
- `/` — landing page, journey cards from API
- `/journeys/[journeySlug]` — topics from API
- `/journeys/[journeySlug]/topics/[topicSlug]` — UNDERSTAND / VERIFY / ACT / PROTECT
- `/support` — support services directory from API
- `/safety` — deterministic safety check

Features:
- API client (`lib/api.ts`) with `NEXT_PUBLIC_API_BASE_URL`
- Quick Exit (navigates away immediately, no history manipulation)
- Loading / empty / error states on all API-driven screens
- Risk badges and Verified badges driven by backend status
- No legal content hard-coded in frontend source
- No user accounts, no personal data collection
- Safety check messages cleared from state after submission, never persisted

### Backend API

Technology: Django 6 + Django REST Framework

Status: Fully operational. 7 endpoints. CORS configured (restricted to frontend origin).

### Knowledge Database

Technology: PostgreSQL

Status: All Day 4 tables live. Seed data loaded.

### Safety Engine

Current: Deterministic RiskRule pattern matching (POST /api/v1/safety/check/).

Future: AI-assisted classification (Day 5+).

### AI Layer

Status: Not yet implemented. Planned for Day 5+.

## API Endpoints (complete)

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/v1/journeys/ | List active journeys |
| GET | /api/v1/journeys/\<slug\>/topics/ | Topics in a journey |
| GET | /api/v1/journeys/\<slug\>/topics/\<slug\>/rights/ | Verified rights records |
| GET | /api/v1/journeys/\<slug\>/topics/\<slug\>/actions/ | Verified action steps |
| GET | /api/v1/rights/\<record_code\>/ | Single rights record |
| GET | /api/v1/support-services/ | Verified support services |
| POST | /api/v1/safety/check/ | Deterministic safety classification |

## CORS Decision

CORS is required because Next.js (port 3000) and Django (port 8000) run on separate origins in development.

`django-cors-headers==4.4.0` is used. Allowed origins are configured via `CORS_ALLOWED_ORIGINS` environment variable — default: `http://localhost:3000,http://127.0.0.1:3000`. `CORS_ALLOW_ALL_ORIGINS` is never used.

## Failure Behaviour

If API unavailable: frontend shows error state — no invented content.

If no verified information: empty state shown, user directed to support services.

If immediate danger detected: IMMEDIATE risk result surfaces verified support contacts immediately.
