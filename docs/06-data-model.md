# Data Model

## Journey

Represents one of the main SafeSpace journeys.

Fields:

id

name

slug

description

risk_default

active

## Topic

Represents a specific information topic within a journey.

Fields:

id

journey_id

title

slug

description

default_risk_level

sort_order

active

## LegalSource

Represents an authoritative legal, policy, or institutional source.

Fields:

id

title

source_type

publisher

jurisdiction

url

publication_date

last_verified

status

## RightsRecord

Represents a small, verifiable rights proposition.

Fields:

id

journey_id

topic_id

jurisdiction

title

plain_language_summary

legal_reference

section_reference

source_id

risk_level

next_step_text

limitations

last_verified

status

active

## RightsTranslation

Stores translated SafeSpace content.

Fields:

id

rights_record_id

language_code

title

plain_language_summary

next_step_text

## SupportService

Represents a verified support or referral service.

Fields:

id

name

service_type

country

phone

whatsapp

website

description

available_24_7

last_verified

status

## ActionPath

Represents structured next-step guidance.

Fields:

id

topic_id

step_number

instruction

action_type

active

## RiskRule

Represents deterministic safety classification rules.

Fields:

id

category

pattern

risk_level

action

active

## Optional Interaction Record

SafeSpace may store privacy-preserving analytics.

Possible fields:

id

anonymous_session_id

journey_id

topic_id

risk_level

created_at

The MVP should avoid storing raw user questions unless there is a clear safety and privacy justification.