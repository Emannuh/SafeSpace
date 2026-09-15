# SafeSpace Architecture

## Architecture Goal

SafeSpace provides AI-assisted explanations without allowing the AI model to become the source of legal truth.

The system follows the principle:

Verified Source → Structured Rights Record → Controlled Retrieval → AI Explanation → Source Citation → Next Action

## Updated Architecture (Day 3)

```
                  USER
                    |
                    v
             Future Frontend
                    |
                    v
              Django API (/api/v1/)
                    |
       +------------+-------------+-----------+
       |            |             |           |
       v            v             v           v
 Rights Layer   Action Layer  Support    Safety Layer
       |            |          Layer          |
       v            v             |           v
RightsRecord   ActionPath    SupportService  RiskRule
LegalSource    (optional     (verified       (deterministic
               source)        contacts)       pattern match)
       \            |             /           /
        \           |            /           /
         +----------+-----------+-----------+
                    |
                    v
                PostgreSQL

No AI yet. AI layer is planned for Day 4+.
```

## High-Level Components

### Frontend

Responsibilities: mobile-first UI, journey selection, question submission, display of rights information, sources, support services, safety routing, language selection, Quick Exit.

Proposed technology: Next.js and Tailwind CSS

Status: Not yet implemented.

### Backend API

Responsibilities: expose journey/topic/rights/action/support data, process safety classification, prepare grounded AI context (future), return structured responses.

Proposed technology: Django and Django REST Framework

Status: Read-only API operational. Safety endpoint operational.

### Knowledge Database

Responsibilities: store journeys, topics, legal sources, rights records, support services, action pathways, risk rules, translations (future).

Proposed technology: PostgreSQL

Status: All Day 3 tables live.

### Safety Engine

Responsibilities: classify risk level, identify immediate danger, bypass ordinary AI flows when necessary, expose emergency support pathways.

Current MVP approach: deterministic RiskRule pattern matching.

Future enhancement: AI-assisted classification.

Status: Deterministic safety endpoint operational at POST /api/v1/safety/check/.

### Retrieval Layer

Responsibilities: map user questions to relevant topics, retrieve best matching verified records.

Current approach: structured database filtering.

Future enhancement: semantic search using pgvector.

Status: Structured filtering in place.

### AI Layer (Day 4+)

Responsibilities: simplify complex legal language, explain verified rights information, support multilingual explanation.

The AI layer must not: invent laws, invent procedures, invent support institutions, determine guilt or innocence.

Status: Not yet implemented.

## Failure Behaviour

If AI is unavailable: SafeSpace still displays structured legal content.

If no verified information exists: SafeSpace clearly states it does not have verified information.

If immediate danger is detected: SafeSpace prioritises safety and support information before legal explanation.

## API Endpoints (Day 3)

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/v1/journeys/ | List active journeys |
| GET | /api/v1/journeys/<slug>/topics/ | List active topics in a journey |
| GET | /api/v1/journeys/<slug>/topics/<slug>/rights/ | Verified rights records |
| GET | /api/v1/journeys/<slug>/topics/<slug>/actions/ | Verified action steps |
| GET | /api/v1/rights/<record_code>/ | Single rights record |
| GET | /api/v1/support-services/ | Active verified support services |
| POST | /api/v1/safety/check/ | Deterministic risk classification |
