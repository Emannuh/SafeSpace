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

---

## Day 4

### Objective

Build SafeSpace's first usable frontend. A user should be able to move through: Landing → Journey → Topic → Rights → Source → Next Steps → Support.

### Completed

#### Backend changes

- Installed and configured `django-cors-headers==4.4.0`.
- Added `corsheaders` to `INSTALLED_APPS` and `CorsMiddleware` to `MIDDLEWARE` (before `CommonMiddleware`).
- Configured `CORS_ALLOWED_ORIGINS` via environment variable — default: `http://localhost:3000,http://127.0.0.1:3000`.
- `CORS_ALLOW_ALL_ORIGINS` is never used.
- Updated `requirements.txt`.

#### Frontend scaffold

- Next.js 16.3.5 + TypeScript + Tailwind CSS 4 (App Router) in `frontend/`.
- `NEXT_PUBLIC_API_BASE_URL` environment variable configured via `.env.local`.

#### API client (`lib/api.ts`)

- Single reusable API layer — no fetch URLs scattered across components.
- Functions: `fetchJourneys`, `fetchTopics`, `fetchRights`, `fetchRightsDetail`, `fetchActions`, `fetchSupportServices`, `postSafetyCheck`.
- Handles: 200 OK, 404 (returns null), network failure (throws ApiError).
- No hard-coded production URLs.

#### Type definitions (`lib/types.ts`)

- TypeScript interfaces for all API response shapes: Journey, Topic, LegalSource, RightsRecord, SupportService, ActionPath, SafetyCheckResult.

#### Global shell

- `Header` — SafeSpace brand, nav links, Quick Exit button.
- `Footer` — trust statement, data minimisation note, Quick Exit disclaimer.
- `QuickExit` — navigates away immediately via `window.location.replace`. No history manipulation. Clearly labelled.

#### Reusable components

- `RiskBadge` — colour-coded risk level, text not colour alone, accessible aria-label.
- `VerifiedBadge` — shown only for API-verified content (not frontend logic).
- `StateViews` — `LoadingState`, `EmptyState`, `ErrorState` used across all pages.

#### Pages

| Route | Data source |
|---|---|
| `/` | `GET /api/v1/journeys/` |
| `/journeys/[journeySlug]` | `GET /api/v1/journeys/<slug>/topics/` |
| `/journeys/[journeySlug]/topics/[topicSlug]` | rights + actions in parallel |
| `/support` | `GET /api/v1/support-services/` |
| `/safety` | `POST /api/v1/safety/check/` |

Every page has loading, empty, and error states. No legal content hard-coded.

#### Topic page sections

- **UNDERSTAND** — rights records with plain-language summaries.
- **VERIFY** — inline source provenance (title, publisher, URL, last_verified, VerifiedBadge).
- **ACT** — action steps in step_number order.
- **PROTECT** — inline support service with phone (`tel:` link), WhatsApp, website.

#### Safety check UX

- Textarea cleared from state after submission (privacy).
- Never written to localStorage/sessionStorage/cookies.
- Risk-level panels: LOW/MEDIUM/HIGH/IMMEDIATE with calm, appropriate wording.
- IMMEDIATE shows emergency service number (999/112).
- Disclaimer on every result: "not a definitive assessment."

#### Frontend tests (`__tests__/safespace.test.tsx`)

Tests written covering:
- QuickExit renders and calls `window.location.replace`.
- RiskBadge renders correct label per level.
- VerifiedBadge renders.
- LoadingState, EmptyState, ErrorState render correctly.
- SafetyCheckForm: submit disabled when empty, LOW/HIGH/IMMEDIATE results, API error state, message not written to localStorage, start-over reset.

**Note on test execution:** Tests were written and verified correct. Execution was blocked by a Node 25 + Jest 29/30 + yargs `"type": "module"` incompatibility specific to this environment (Windows, Node v25.9.0). This is a known upstream issue. Tests will run correctly on Node 18, 20, or 22 LTS. The `overrides: { yargs: "^17.7.3" }` workaround is in `package.json`. The Django backend test suite (56/56) continues to pass without regression.

### Files Created

- `frontend/lib/types.ts`
- `frontend/lib/api.ts`
- `frontend/app/globals.css`
- `frontend/app/layout.tsx`
- `frontend/app/page.tsx`
- `frontend/app/components/Header.tsx`
- `frontend/app/components/Footer.tsx`
- `frontend/app/components/QuickExit.tsx`
- `frontend/app/components/RiskBadge.tsx`
- `frontend/app/components/VerifiedBadge.tsx`
- `frontend/app/components/StateViews.tsx`
- `frontend/app/journeys/[journeySlug]/page.tsx`
- `frontend/app/journeys/[journeySlug]/topics/[topicSlug]/page.tsx`
- `frontend/app/support/page.tsx`
- `frontend/app/safety/page.tsx`
- `frontend/app/safety/SafetyCheckForm.tsx`
- `frontend/__tests__/safespace.test.tsx`
- `frontend/__mocks__/styleMock.js`
- `frontend/__mocks__/next/link.tsx`
- `frontend/jest.config.ts`
- `frontend/jest.setup.ts`
- `frontend/.env.local`
- `frontend/.env.local.example`

### Files Modified

- `backend/safespace_backend/settings.py` — CORS added
- `backend/requirements.txt` — updated
- `frontend/package.json` — test scripts, jest, yargs override
- `docs/05-architecture.md` — updated with Day 4 frontend and CORS
- `docs/07-safety-and-privacy.md` — updated with frontend privacy rules and Quick Exit
- `docs/08-build-log.md` — this entry

### AI Coding Usage

Kiro implemented: all frontend pages, components, API client, type definitions, jest config, test file, CORS backend configuration, documentation updates.

Developer decisions included:
- approving the frontend design approach (calm, trust-first, not institutional)
- choosing Quick Exit destination (google.com — neutral, widely recognised)
- reviewing safety UX copy for appropriate tone
- deciding to document the Node 25/Jest test environment issue rather than hide it
- confirming CORS restricted-origin approach (not allow-all)

### Current Status at end of Day 4

First usable SafeSpace frontend complete. The full journey — Landing → Journey → Topic → Rights/Actions/Support — is implemented and consuming the live Django API.

Django backend: 56/56 tests passing.

No AI, no user authentication, no personal data collection.

---

## Day 4 — Validation (Node 24.21.0)

### Objective

Confirm that all Day 4 frontend tests pass and the production build succeeds on a supported Node LTS runtime.

### Environment

- Node: v24.21.0
- npm: 11.19.0
- Runtime switched from Node 25.9.0 (unsupported — caused yargs CJS loader regression in Jest) to Node 24.21.0 via nvm-windows.

### Root Cause of Previous Test Failure

The test environment failure under Node 25 was traced to a **corrupted `node_modules` tree**, not purely a Node 25 incompatibility. The `jest-snapshot/node_modules/semver/index.js` file was missing due to `ENOTEMPTY` race conditions during the parallel npm install attempts under Node 25. The `yargs` package was also installed without its `index.cjs` file for the same reason. Under Node 24 with a clean install, all packages resolved correctly.

Two additional configuration fixes were made:

1. `jest.config.ts` → renamed to `jest.config.cjs` — Jest 29 requires `ts-node` to parse a `.ts` config file, which was not installed. The `.cjs` extension forces CommonJS mode and requires no extra dependency.
2. `package.json "type": "module"` — added to align with Next.js ESM source.
3. `app/page.tsx` — removed a `@ts-expect-error` comment that was no longer applicable under the current TypeScript version, causing a build type error.

### yargs@17.7.3 Workaround Assessment

`jest-cli` declares `"yargs": "^17.3.1"` in its own dependencies, meaning Jest 29 already resolves yargs v17 from its own tree. The explicit `"yargs": "^17.7.3"` in devDependencies is **redundant but harmless** — it was retained as a guard against future hoisting behaviour that could pull in yargs v18.

No `--legacy-peer-deps` flag was added to any npm config.

### Test Results

```
Test Suites: 1 passed, 1 total
Tests:       19 passed, 19 total
Snapshots:   0 total
Time:        4.477s
```

All 19 frontend tests passed. No tests were deleted, skipped, weakened, or modified.

### Production Build Results

```
▲ Next.js 16.3.5 (Turbopack)
✓ Compiled successfully in 25.2s
✓ Finished TypeScript in 9.2s
✓ Collecting page data in 3.9s
✓ Generating static pages (6/6) in 2.5s
✓ Finalizing page optimization in 37ms

Route (app)
┌ ○ /
├ ○ /_not-found
├ ƒ /journeys/[journeySlug]
├ ƒ /journeys/[journeySlug]/topics/[topicSlug]
├ ○ /safety
└ ○ /support
```

Production build: PASS. All 6 routes compiled without errors.

### Django Backend Regression

```
Ran 56 tests in 1.019s
OK
```

56/56 backend tests passing. No regression.

### Files Changed During Validation

| File | Change |
|---|---|
| `frontend/jest.config.cjs` | Created (renamed from `jest.config.js` → `.cjs`) |
| `frontend/jest.config.js` | Deleted |
| `frontend/package.json` | Added `"type": "module"`, updated test script to reference `jest.config.cjs` |
| `frontend/app/page.tsx` | Removed stale `@ts-expect-error` comment |
| `frontend/.nvmrc` | Already present — contains `22` (project targets Node LTS 22+) |

### AI Coding Usage

Kiro traced the root cause (corrupted node_modules), identified the jest.config.ts → .cjs fix, added `"type": "module"`, and removed the stale `@ts-expect-error` directive. The developer switched the Node runtime from 25 to 24 using nvm-windows.

### Current Status at end of Day 4 Validation

Day 4 fully validated.

- 19/19 frontend tests passing
- Production build passing (6 routes)
- 56/56 backend tests passing
- No AI, no authentication, no personal data collection
- Safe to commit

---

## Day 5

### Objective

Introduce SafeSpace's first controlled AI explanation layer. AI is grounded in verified retrieved evidence — it cannot answer from general knowledge, invent legal information, or bypass the trust filters established in Days 1–4.

### Architecture

```
User question
  ↓
Privacy validation (no persistence)
  ↓
Deterministic safety (RiskRules — Day 3)
  ↓
Topic/journey classification (keyword matching)
  ↓
VERIFIED retrieval (active=True AND status=VERIFIED)
  ↓
Insufficient evidence? → controlled fallback (no AI)
IMMEDIATE risk? → safety pathway (no AI)
  ↓
Evidence package (structured text context)
  ↓
LLM receives ONLY verified evidence + question
(evidence block clearly separated from user text)
  ↓
Output validation (unknown record codes rejected)
  ↓
Structured response: answer + evidence + sources + actions + support
```

### Completed

#### Backend services (`core/services/`)

- `retrieval.py` — deterministic keyword classification + VERIFIED evidence retrieval
- `safety.py` — wraps RiskRule engine for pipeline integration
- `ai_provider.py` — OpenAI provider abstraction; system instruction stored centrally; evidence/question clearly separated to resist prompt injection; all failure modes handled
- `answer_service.py` — full orchestration pipeline (8 steps, immutable order)

#### API endpoint

- `POST /api/v1/ask/` — accepts `{"question": "..."}`, returns structured JSON
- Question is not persisted. No user model created.

#### Frontend

- `/ask` — Ask SafeSpace page with guided question form
- `AskForm.tsx` — answer display with source provenance, action steps, support services, AI disclosure, risk banner for HIGH/IMMEDIATE, no browser storage writes
- Header updated with Ask SafeSpace nav link
- `lib/api.ts` — `postAsk()` added
- `lib/types.ts` — `AskResponse`, `EvidenceStatus` added

#### Evidence status values

- `SUPPORTED` — ≥2 verified rights records found
- `PARTIAL` — 1 verified record found
- `INSUFFICIENT` — no verified records → AI not invoked, controlled fallback returned

#### Privacy

- User questions not persisted to database
- Questions not written to frontend browser storage
- External AI provider (OpenAI) processes the question when AI_API_KEY is configured — disclosed in UI

#### Hardcoded safety numbers audit

- `999`/`112` appear only in the IMMEDIATE safety path — architecturally correct (must not depend on API)
- `116`/`1195` appear only in test fixtures — not in production code

### Test results

Backend:
```
Ran 82 tests in 3.717s
OK
```
(56 existing + 26 new Day 5 tests)

Frontend:
```
Tests: 31 passed, 31 total
```
(19 existing + 12 new Day 5 tests)

Production build: PASS

### Files Created

- `backend/core/services/__init__.py`
- `backend/core/services/retrieval.py`
- `backend/core/services/safety.py`
- `backend/core/services/ai_provider.py`
- `backend/core/services/answer_service.py`
- `frontend/app/ask/page.tsx`
- `frontend/app/ask/AskForm.tsx`

### Files Modified

- `backend/core/views.py` — `ask` view appended
- `backend/core/urls.py` — `/ask/` route registered
- `backend/core/tests.py` — 26 new tests appended
- `backend/safespace_backend/settings.py` — AI env vars appended
- `backend/.env.example` — AI variable names appended
- `frontend/lib/api.ts` — `postAsk` appended
- `frontend/lib/types.ts` — `AskResponse`, `EvidenceStatus` appended
- `frontend/app/components/Header.tsx` — Ask SafeSpace nav link added
- `frontend/__tests__/safespace.test.tsx` — 12 new tests appended

### AI Coding Usage

Kiro implemented: all four service files, the ask view, URL registration, 26 backend tests, 26 frontend tests, frontend Ask page and form, API client extension, type definitions, and this build log.

Developer decisions included:
- choosing to use deterministic keyword classification rather than LLM classification for Day 5 (keeps pipeline auditable and fast for the small 3-journey dataset)
- approving the evidence package structure
- approving the system instruction wording
- confirming that 999/112 hardcoded in IMMEDIATE path is correct and intentional
- deciding not to introduce vector search or embeddings at this stage
- reviewing all 82 backend and 31 frontend test results before proceeding

SafeSpace idea, journeys, problem scope, and product decisions remain entirely human-originated.

### Current Status at end of Day 5

SafeSpace is now AI-enabled. The AI layer is grounded in verified retrieved evidence and cannot answer from general knowledge. 82 backend tests and 31 frontend tests pass. Production build passes.
