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

Kiro was used as an AI coding assistant to scaffold the initial Django backend, create the Python development environment, configure project dependencies, configure environment-based settings, and create the initial Django application structure.

AI-generated changes were reviewed before proceeding.

### Current Status at end of Day 1

Backend foundation complete. No business models, API endpoints, AI integration, or frontend functionality.

---

## Day 1 — continued

### Completed

- Implemented four core knowledge-base models: Journey, Topic, LegalSource, RightsRecord.
- Defined shared TextChoices for RiskLevel, VerificationStatus, and SourceType.
- Added UniqueConstraint for topic slug uniqueness per journey.
- Generated and reviewed migration `core/migrations/0001_initial.py`.
- Diagnosed and resolved PostgreSQL authentication configuration on local development machine.
- Developer reset PostgreSQL superuser credentials, created the `safespace` database, and confirmed connectivity.
- Applied all Django migrations successfully.

### AI Coding Usage

Kiro implemented models, generated migration, diagnosed PostgreSQL auth failure, updated pg_hba.conf, and reverted after reset.

Developer actions: reviewed models before applying migrations, executed PostgreSQL service restart (Administrator required), ran ALTER USER password reset, created safespace database.

### Current Status

Database migrated. Core schema live. No API endpoints yet.

---

## Day 2

### Objective

Build the first usable SafeSpace trusted knowledge API.

### Completed

- Registered Journey, Topic, LegalSource, RightsRecord in Django Admin with editorial workflow configuration.
- Created read-only serializers in `core/serializers.py`.
- Implemented four read-only API endpoints.
- Created `core/urls.py`, updated `safespace_backend/urls.py`.
- Written 29 automated tests — all passing.
- Created `core/management/commands/seed_demo.py`.
- Loaded one verified demonstration RightsRecord: CJ-001 (Constitution of Kenya, Article 49).

### Endpoints (Day 2)

| Method | Endpoint |
|---|---|
| GET | /api/v1/journeys/ |
| GET | /api/v1/journeys/<slug>/topics/ |
| GET | /api/v1/journeys/<slug>/topics/<slug>/rights/ |
| GET | /api/v1/rights/<record_code>/ |

### Test results

29/29 tests passing.

### AI Coding Usage

Kiro implemented admin classes, serializers, views, URL routing, 29 tests, seed command, and build log.

Developer decisions: URL design correction (journey-scoped topics), seed content review against docs/03-legal-framework.md, approval of migration, confirming test results.

### Current Status at end of Day 2

Trusted knowledge API operational. VERIFIED filtering enforced server-side. No AI, no frontend.

---

## Day 3

### Objective

Add the first actionability and safety layer: SupportService, ActionPath, RiskRule, action/support APIs, and deterministic safety classification.

### Completed

#### Models

- Added `SupportService` model with service-type choices and verification fields.
- Added `ActionPath` model with step ordering and `unique_step_number_per_topic` constraint.
- Added `RiskRule` model with pattern-based deterministic matching and a `.matches()` method.
- Added supporting TextChoices: `ServiceType`, `ActionType`, `RiskCategory`, `RiskAction`.

#### Migration

- Generated and applied `core/migrations/0002_riskrule_supportservice_actionpath.py`.
- Tables created: `core_riskrule`, `core_supportservice`, `core_actionpath`.
- Constraint added: `unique_step_number_per_topic` on `core_actionpath`.

#### Django Admin

- Registered `SupportService`, `ActionPath`, `RiskRule` with list_display, list_filter, search_fields, autocomplete_fields, date_hierarchy, and fieldsets.

#### Serializers

- Rewrote `core/serializers.py` — added `SupportServiceSerializer` and `ActionPathSerializer`.
- `ActionPathSerializer` nests inline `SupportServiceSerializer` and `LegalSourceSerializer`.

#### API Endpoints (Day 3 additions)

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/v1/support-services/ | Active VERIFIED support services |
| GET | /api/v1/journeys/<slug>/topics/<slug>/actions/ | Verified action steps for a topic |
| POST | /api/v1/safety/check/ | Deterministic risk classification (message not stored) |

#### Safety Classification

- Implemented `safety_check` view: accepts `{"message": "..."}`, evaluates active RiskRules by priority and severity, returns `{risk_level, action, matched_rule}`.
- User message is not persisted anywhere.
- Falls back to `LOW / NORMAL_FLOW` when no rules match.

#### Tests

- Added 27 new tests (ActionPath: 10, SupportService: 7, SafetyCheck: 10).
- Total test suite: 56 tests, all passing.
- Run time: ~1.2 seconds.

#### Demonstration Seed Data

Extended `seed_demo.py` with:
- 4 verified support services from `docs/03-legal-framework.md`: Child Helpline 116, GBV Helpline 1195, National Legal Aid Service, IPOA.
- 3 ActionPath steps for the Arrest Rights topic (grounded in Constitution of Kenya, Article 49).
- 3 RiskRules based on example phrases from `docs/07-safety-and-privacy.md`.

All seed data is sourced from existing project documentation. No contact information was invented.

### Files Created

- `backend/core/migrations/0002_riskrule_supportservice_actionpath.py`

### Files Modified

- `backend/core/models.py` — appended SupportService, ActionPath, RiskRule
- `backend/core/admin.py` — appended SupportService, ActionPath, RiskRule admin classes
- `backend/core/serializers.py` — rewritten to add SupportServiceSerializer, ActionPathSerializer
- `backend/core/views.py` — rewritten to add support_service_list, action_list, safety_check
- `backend/core/urls.py` — rewritten to add 3 new routes
- `backend/core/tests.py` — rewritten with 56 total tests
- `backend/core/management/commands/seed_demo.py` — rewritten with Day 3 data
- `docs/05-architecture.md` — updated with Day 3 architecture
- `docs/06-data-model.md` — updated with SupportService, ActionPath, RiskRule
- `docs/07-safety-and-privacy.md` — updated with deterministic risk classification
- `docs/08-build-log.md` — this file

### Issues Encountered

- `seed_demo --reset` failed on first run because PROTECT prevented Journey deletion while Topics existed. Fixed by deleting children (ActionPaths, RightsRecords, Topics) before parents.

### Architectural Decisions

- SupportService is separate from LegalSource: legal documents and human support contacts serve different purposes and have different verification workflows.
- ActionPath uses `PROTECT` on source FK (nullable) and `SET_NULL` on support_service FK — allows a service to be removed without cascading deletes of action steps.
- Safety endpoint uses deterministic pattern matching — auditable and AI-free. AI-assisted classification is planned for Day 4+.
- User messages are not persisted anywhere — consistent with SafeSpace privacy principle (docs/07-safety-and-privacy.md).

### AI Coding Usage

Kiro implemented: three new models, migration, three admin classes, two new serializers, three new views, updated URL routing, 27 new tests, updated seed command, and all four documentation updates.

Developer decisions included:
- reviewing seed service data against docs/03-legal-framework.md before approving
- confirming risk rule patterns are consistent with docs/07-safety-and-privacy.md examples
- reviewing all 56 test results before proceeding
- deciding which support services had sufficient documentation to include
- approving the architecture decision to keep safety classification deterministic (no AI) at this stage

SafeSpace capstone idea, target users, journeys, and problem scope remain entirely human-originated.

### Current Status at end of Day 3

Actionability and safety layer complete. The backend now has:
- 7 knowledge/support/action models
- 7 read-only API endpoints
- 1 deterministic safety classification endpoint
- 56 passing automated tests
- Verified demonstration data for all Day 3 features

No AI, no frontend, no user authentication, no personal data collection.
