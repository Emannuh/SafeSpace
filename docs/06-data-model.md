# Data Model

## Journey

Represents one of the main SafeSpace journeys.

Fields:

id, name, slug, description, risk_default, active, created_at, updated_at

## Topic

Represents a specific information topic within a journey.

Fields:

id, journey_id, title, slug, description, default_risk_level, sort_order, active, created_at, updated_at

Constraint: slug is unique within a Journey (not globally).

## LegalSource

Represents an authoritative legal, policy, or institutional source document.

Fields:

id, title, source_type, publisher, jurisdiction, url, publication_date, last_verified, status, created_at, updated_at

## RightsRecord

Represents a small, verifiable rights proposition.

Fields:

id, record_code, journey_id, topic_id, jurisdiction, title, plain_language_summary, legal_reference, section_reference, source_id, risk_level, next_step_text, limitations, last_verified, status, active, created_at, updated_at

## SupportService

Represents a verified support organisation, helpline, or official support pathway.

Purpose: store verified human support contacts that a user can contact — distinct from LegalSource which stores authoritative legal documents.

Fields:

id, name, slug, service_type, description, jurisdiction, phone, whatsapp, website, available_24_7, source_url, last_verified, status, active, created_at, updated_at

Service types: CHILD_PROTECTION, GBV_SUPPORT, LEGAL_AID, POLICE_OVERSIGHT, HEALTH_SUPPORT, GENERAL_SUPPORT

## ActionPath

Represents structured next-step guidance associated with a SafeSpace topic.

Purpose: provide verified, source-traceable next steps — not AI-generated suggestions.

Fields:

id, topic_id, title, step_number, instruction, action_type, support_service_id (nullable), source_id (nullable), last_verified, status, active, created_at, updated_at

Action types: RIGHTS_GUIDANCE, SUPPORT_REFERRAL, LEGAL_ASSISTANCE, REPORTING_OPTION, SAFETY_ACTION

Constraint: step_number is unique within a Topic.

## RiskRule

Represents a deterministic safety classification rule.

Purpose: provide first-line risk classification without AI. Rules use simple pattern matching on incoming messages.

Fields:

id, name, category, pattern (comma-separated keywords), risk_level, action, priority, active, created_at, updated_at

Categories: GENERAL, ABUSE, IMMEDIATE_DANGER, LAW_ENFORCEMENT

Actions: NORMAL_FLOW, SHOW_SUPPORT, SHOW_HIGH_RISK_SUPPORT, SHOW_IMMEDIATE_SAFETY

## RightsTranslation (planned — Day 4+)

Stores translated SafeSpace content.

Fields (planned): id, rights_record_id, language_code, title, plain_language_summary, next_step_text

## Optional Interaction Record (planned)

SafeSpace may store privacy-preserving analytics.

The MVP does not store raw user questions or personal data.
