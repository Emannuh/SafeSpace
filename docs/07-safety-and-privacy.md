# Safety and Privacy

## Safety Principle

SafeSpace may be used by young people in sensitive or unsafe situations.

Safety is part of the architecture, not an additional feature.

## Data Minimisation

The MVP does not require:
- full name, national ID, phone number, email address, exact address, account creation.

Users can access core rights information anonymously.

## Sensitive Conversations

SafeSpace does not store raw user messages or conversations.

The safety classification endpoint (POST /api/v1/safety/check/) accepts a message, classifies it, and returns a result — without persisting the message.

**Frontend privacy rules (Day 4):**
- The safety-check message is held only in React component state.
- It is NEVER written to localStorage, sessionStorage, or cookies.
- It is NEVER sent to analytics.
- After submission, the message is cleared from component state.
- The textarea uses `autoComplete="off"` and `autoSave="off"` to discourage browser caching.

## Risk Classification

### Risk Levels

LOW — normal informational journey

MEDIUM — information plus relevant support services

HIGH — prominently surface verified support options

IMMEDIATE — prioritise immediate safety and support pathways before legal information

### Deterministic Safety Classification

SafeSpace uses deterministic RiskRule pattern matching as the first line of safety classification.

Rules are stored in the database, not hard-coded. Priority ordering ensures the most severe matching rule wins.

If no rules match, the default is LOW / NORMAL_FLOW.

### Immediate Risk Examples (from docs/07 spec)

"I am not safe" → IMMEDIATE

"He is here" → IMMEDIATE

"They are hurting me now" → IMMEDIATE

### Frontend Safety UX (Day 4)

IMMEDIATE result: "Your safety comes first" — calm tone, direct link to support services.

HIGH result: "You may need support right now" — support services prominently shown.

MEDIUM result: "Support is available" — support services visible.

LOW result: "Here to help" — normal navigation.

All results include: "This is a structured safety guide — not a definitive assessment."

Emergency services contact (999 / 112) always mentioned for IMMEDIATE.

## Quick Exit (Day 4)

Quick Exit is available throughout SafeSpace via the persistent header button.

Behaviour:
- One click navigates to an external neutral site immediately (google.com).
- No confirmation dialog.
- No history manipulation is attempted.

Disclaimer shown to users:
"Quick Exit leaves SafeSpace immediately but does not erase your browser history or device activity."

## AI Safety

SafeSpace must never allow the AI model (Day 5+) to:
- determine whether a specific person is guilty
- tell a user how to evade law enforcement
- fabricate legal rights, institutions, or emergency contacts

AI output must be grounded in SafeSpace records.

## Unsupported Questions

If no verified information exists:
"SafeSpace does not currently have verified information for this question. Please use one of the listed support services or seek qualified legal assistance."

## Privacy Philosophy

SafeSpace follows the principle: **Collect less. Protect more.**
