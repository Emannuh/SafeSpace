# Safety and Privacy

## Safety Principle

SafeSpace may be used by young people in sensitive or unsafe situations.

Safety is part of the architecture rather than an additional feature.

## Data Minimisation

The MVP does not require:

- full name
- national ID
- phone number
- email address
- exact home address
- account creation

Users can access core rights information anonymously.

## Sensitive Conversations

SafeSpace does not store raw user messages or conversations.

The safety classification endpoint (POST /api/v1/safety/check/) accepts a message, classifies it, and returns a result — without persisting the message.

If interaction analytics are required in the future, the system should prefer storing:

- topic
- risk classification
- anonymous session identifier
- timestamp

rather than detailed personal disclosures.

## Risk Classification

### Risk Levels

LOW — normal informational journey

MEDIUM — information plus relevant support services

HIGH — prominently surface verified support options

IMMEDIATE — prioritise immediate safety and support pathways before legal information

### Deterministic Safety Classification (Day 3)

SafeSpace uses deterministic RiskRule pattern matching as the first line of safety classification.

How it works:

1. The user message is compared against all active RiskRule records ordered by priority.
2. Each rule contains a comma-separated list of keywords or phrases.
3. A message matches a rule if it contains any of the listed terms (case-insensitive).
4. When multiple rules match, the rule with the highest risk severity is selected.
5. If no rules match, the default result is LOW / NORMAL_FLOW.

This approach is auditable, verifiable, and does not require AI.

AI-assisted classification is planned for a future milestone.

### Example Risk Rules

immediate-danger: "i am not safe, he is here, they are hurting me, i cannot leave"
→ IMMEDIATE / SHOW_IMMEDIATE_SAFETY

abuse-high-risk: "hurting me, beating me, abusing me, sexual abuse, assault"
→ HIGH / SHOW_HIGH_RISK_SUPPORT

general-concern: "scared, afraid, worried, unsafe, danger, threatened"
→ MEDIUM / SHOW_SUPPORT

### Immediate Risk Examples

"I am not safe" → IMMEDIATE

"He is here" → IMMEDIATE

"They are hurting me now" → IMMEDIATE

"I cannot leave" → IMMEDIATE

Immediate-risk responses prioritise verified support channels before legal explanation.

## Quick Exit

SafeSpace should include a Quick Exit feature (frontend — Day 4+).

The interface should communicate that Quick Exit cannot guarantee browser history, network logs, or device activity have been removed.

## AI Safety

SafeSpace must never allow the AI model to:

- determine whether a specific person is guilty
- tell a user how to evade law enforcement
- fabricate legal rights
- fabricate legal institutions
- fabricate emergency contacts

AI output must be grounded in SafeSpace records.

## Unsupported Questions

If no verified information exists:

"SafeSpace does not currently have verified information for this question. Please use one of the listed support services or seek qualified legal assistance."

## Privacy Philosophy

SafeSpace follows the principle:

Collect less. Protect more.
