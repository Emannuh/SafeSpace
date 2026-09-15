# 08 Build Log

## Day 1

### Completed

- Created the SafeSpace GitHub repository.
- Added initial project documentation.
- Defined the MVP scope and architecture.
- Created the Django backend environment.
- Installed Django and Django REST Framework.
- Configured PostgreSQL environment variables.
- Added environment-based application configuration.
- Created the `core` Django application.
- Added dependency management through `requirements.txt`.
- Verified the initial Django project configuration.

### AI Coding Usage

Kiro was used as an AI coding assistant to:
- scaffold the initial Django backend
- create the Python development environment
- configure project dependencies
- configure environment-based settings
- create the initial Django application structure

AI-generated changes were reviewed before proceeding to the next development stage.

### Current Status

Backend foundation complete.

No SafeSpace business models, API endpoints, AI integration, or frontend functionality have been implemented yet.

---

## Day 1 — continued

### Completed

- Implemented four core knowledge-base models: Journey, Topic, LegalSource, RightsRecord.
- Defined shared TextChoices for RiskLevel, VerificationStatus, and SourceType.
- Added UniqueConstraint for topic slug uniqueness per journey.
- Generated and reviewed migration `core/migrations/0001_initial.py`.
- Diagnosed and resolved PostgreSQL authentication configuration on local development machine.
- Developer reset PostgreSQL superuser credentials, created the `safespace` database, and confirmed connectivity.
- Applied all Django migrations successfully to the `safespace` PostgreSQL database.

### AI Coding Usage

Kiro was used to:
- implement all four knowledge-base models in `core/models.py`
- generate the initial migration file
- diagnose the PostgreSQL authentication failure
- update `pg_hba.conf` auth method to enable the password reset
- revert `pg_hba.conf` after the reset was complete
- update `backend/.env` with the correct database credentials

Developer actions included:
- reviewing the generated models before applying migrations
- executing the PostgreSQL service restart (required Administrator privileges)
- running the `ALTER USER` password reset command
- creating the `safespace` database
- confirming the migration output before proceeding

### Current Status

Database fully migrated. Core knowledge-base schema is live in PostgreSQL.

No API endpoints, AI integration, seed data, superuser, or frontend functionality have been implemented yet.

---

## Day 2

### Objective

Build the first usable SafeSpace trusted knowledge API: register models in the Django admin, create read-only serializers, implement journey-scoped API endpoints with backend trust filtering, write automated tests, and load a small verified demonstration knowledge record.

### Completed

#### Django Admin

- Registered Journey, Topic, LegalSource, and RightsRecord in `core/admin.py`.
- Added `list_display`, `list_filter`, `search_fields`, `ordering`, `prepopulated_fields`, `autocomplete_fields`, `readonly_fields`, `date_hierarchy`, and `fieldsets` to each admin class.
- Admin configured to support the editorial workflow: adding/updating rights records (FR-16), updating verification dates (FR-17), and deactivating outdated content (FR-18).

#### Serializers

- Created `core/serializers.py` with read-only serializers for Journey, Topic, LegalSource (nested), and RightsRecord.
- LegalSource is embedded inline within RightsRecord responses — every rights response carries a full citation.
- Human-readable display values added for source_type, risk_level, and status using `get_*_display` fields.
- Navigation slugs (journey_slug, topic_slug) included in RightsRecord to support frontend breadcrumb rendering.
- No write operations exposed.

#### API Endpoints

- Created `core/urls.py` and updated `safespace_backend/urls.py` to include routes under `/api/v1/`.
- Implemented four read-only endpoints in `core/views.py`:

| Endpoint | Purpose |
|---|---|
| `GET /api/v1/journeys/` | List active journeys |
| `GET /api/v1/journeys/<journey_slug>/topics/` | List active topics within a journey |
| `GET /api/v1/journeys/<journey_slug>/topics/<topic_slug>/rights/` | List verified rights records for a topic within a journey |
| `GET /api/v1/rights/<record_code>/` | Single verified rights record by code |

- Topic rights use the journey-scoped URL to resolve topic slugs unambiguously (consistent with the `unique_topic_slug_per_journey` constraint).

#### Trust Filtering

Backend enforces:
- Journeys: `active=True` only.
- Topics: `active=True`, scoped to the requested active journey.
- RightsRecords: `active=True AND status=VERIFIED` only.
- ARCHIVED, EXPIRED, REVIEW_REQUIRED and inactive records return 404 at both list and detail endpoints.

#### Automated Tests

- 29 automated tests written in `core/tests.py`.
- All 29 tests pass.
- Test run time: ~0.9 seconds.
- Tests cover: active/inactive journey filtering, inactive topic exclusion, journey-scoped duplicate slug handling, VERIFIED/ARCHIVED/EXPIRED/REVIEW_REQUIRED/inactive filtering, cross-journey record leak prevention, source provenance in responses, 404 behaviour.

#### Demonstration Seed Data

- Created `core/management/commands/seed_demo.py` — idempotent Django management command.
- Loaded one verified demonstration knowledge record grounded in `docs/03-legal-framework.md`:
  - Journey: Child Justice
  - Topic: Arrest Rights
  - LegalSource: Constitution of Kenya (Kenya Law)
  - RightsRecord [CJ-001]: Right to be informed of the reason for arrest (Article 49)
- A management command was chosen over a Django fixture because it is self-documenting, allows data integrity validation at load time, and is easier to review than a JSON fixture.
- Seed data is verified by the API at: `GET /api/v1/journeys/child-justice/topics/arrest-rights/rights/`

### Files Created

- `backend/core/serializers.py`
- `backend/core/urls.py`
- `backend/core/management/__init__.py`
- `backend/core/management/commands/__init__.py`
- `backend/core/management/commands/seed_demo.py`

### Files Modified

- `backend/core/admin.py` — rewritten from stub to full admin configuration
- `backend/core/views.py` — rewritten from stub to four read-only API views
- `backend/core/tests.py` — rewritten from stub to 29 automated tests
- `backend/safespace_backend/urls.py` — updated to include `api/v1/` routes
- `docs/08-build-log.md` — this file

### Test Results

```
Ran 29 tests in 0.928s
OK
```

Django system check: 0 issues.

### Issues Encountered

- The previous iteration of the rights-list endpoint used `topics/<slug>/rights/` without journey context. This was corrected to `journeys/<journey_slug>/topics/<topic_slug>/rights/` to properly enforce the data model's journey-scoped topic slug uniqueness.

### Architectural Decisions

- Topic rights URL uses full journey + topic path to match the database constraint (ADR-003).
- `on_delete=PROTECT` retained on all ForeignKeys — prevents accidental cascade deletion of knowledge base content.
- Trust filtering enforced in Django views/QuerySets, not in serializers or frontend — consistent with ADR-002.
- Seed data loaded via management command, not migration, to keep schema migrations separate from business content.

### AI Coding Usage

Kiro was used to:
- implement admin classes with editorial workflow features
- write serializers with nested source provenance
- implement journey-scoped API views with trust filtering
- write 29 automated tests covering trust model enforcement
- create the seed management command structure
- update this build log

Developer actions and judgements included:
- identifying the URL design gap (topic slug ambiguity without journey context)
- reviewing seed content against `docs/03-legal-framework.md` before approving
- confirming test results and seed output before proceeding
- deciding which seed record to include (human product decision)
- deciding the SafeSpace capstone idea, journeys, and problem scope (entirely human-originated)

### Current Status

Day 2 complete. The SafeSpace trusted knowledge API is operational with:
- 4 read-only endpoints
- backend trust filtering enforced
- 29 passing automated tests
- 1 verified demonstration knowledge record in the live database

No AI integration, user authentication, CORS, frontend, or Day 3 features have been implemented.
