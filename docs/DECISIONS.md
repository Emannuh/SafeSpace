# Architecture Decision Records

## ADR-001: Anonymous Access

Status:
Accepted

Decision:

SafeSpace will not require account registration for core MVP functionality.

Reason:

The platform may be used by minors and vulnerable users. Collecting identity information creates additional privacy and security risk without being necessary for the core service.

---

## ADR-002: Verified Sources Before AI

Status:
Accepted

Decision:

The SafeSpace knowledge base will be built before the AI response layer.

Reason:

The project is designed around trusted information. AI should explain verified information, not become the source of legal truth.

---

## ADR-003: Structured Rights Records

Status:
Accepted

Decision:

Legal information will be stored as structured rights records rather than relying only on entire PDF documents.

Reason:

Structured records improve traceability, retrieval, verification, translation, and update management.

---

## ADR-004: Django Backend

Status:
Proposed

Decision:

Use Django and Django REST Framework for the MVP backend.

Reason:

Django provides strong database modelling, API support, security features, and a built-in administration interface that can serve as the SafeSpace knowledge management console.

---

## ADR-005: PostgreSQL

Status:
Proposed

Decision:

Use PostgreSQL as the primary database.

Reason:

PostgreSQL provides reliable relational storage and allows future use of pgvector for semantic retrieval without introducing a separate vector database.

---

## ADR-006: AI as Explanation Layer

Status:
Accepted

Decision:

AI will be used primarily for explanation, classification, and multilingual support.

Reason:

This preserves a clear separation between authoritative information and generated language.

---

## ADR-007: Low-Bandwidth First

Status:
Accepted

Decision:

The MVP interface should be text-first and mobile-first.

Reason:

The hackathon requires consideration of limited connectivity, basic devices, and restricted mobile data.

---

## ADR-009: CORS Configuration

Status: Accepted

Decision:

Use `django-cors-headers` with `CORS_ALLOWED_ORIGINS` restricted to the frontend origin. Never use `CORS_ALLOW_ALL_ORIGINS = True`.

Reason:

Next.js (port 3000) and Django (port 8000) run on separate origins in development. CORS is required for the browser to allow the API call. Restricting to known origins is a security baseline.

---

## ADR-010: Quick Exit Implementation

Status: Accepted

Decision:

Quick Exit uses `window.location.replace()` to navigate away immediately. No browser history manipulation (e.g. `history.pushState` tricks) is attempted.

Reason:

History manipulation is unreliable and can create a false sense of security. Clear disclosure is provided: "Quick Exit leaves SafeSpace immediately but does not erase your browser history."

---

## ADR-011: Safety Message Privacy

Status: Accepted

Decision:

The safety check message is held only in React component state and cleared after submission. It is never written to localStorage, sessionStorage, cookies, or analytics.

Reason:

Consistent with SafeSpace's privacy principle (collect less, protect more) and the sensitive nature of the safety check content.

Status:
Accepted

Decision:

Immediate-risk messages will bypass the normal informational response flow.

Reason:

A long legal explanation should not take priority over immediate safety and support information.

## ADR-008: Safety Overrides Normal Flow

Status: Accepted

Decision:

Immediate-risk messages will bypass the normal informational response flow.

Reason:

A long legal explanation should not take priority over immediate safety and support information.
