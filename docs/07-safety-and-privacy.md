# Safety and Privacy

## Safety Principle

SafeSpace may be used by young people in sensitive or unsafe situations.

Safety therefore needs to be part of the architecture rather than an additional feature.

## Data Minimisation

The MVP should not require:

- full name
- national ID
- phone number
- email address
- exact home address
- account creation

Users should be able to access core rights information anonymously.

## Sensitive Conversations

SafeSpace should avoid storing raw conversations by default.

If interaction analytics are required, the system should prefer storing:

- topic
- risk classification
- anonymous session identifier
- timestamp

rather than detailed personal disclosures.

## Risk Classification

Suggested levels:

LOW

MEDIUM

HIGH

IMMEDIATE

## Immediate Risk

Examples of messages that may indicate immediate risk include:

"I am not safe"

"He is here"

"They are hurting me now"

"I cannot leave"

Immediate-risk responses should prioritise verified support channels.

The system should not delay the response while generating a long AI explanation.

## Quick Exit

SafeSpace should include a Quick Exit feature.

The purpose is to allow users to leave sensitive content quickly.

The interface should also clearly communicate that a Quick Exit feature cannot guarantee that browser history, network logs, or device activity have been removed.

## AI Safety

SafeSpace should never allow the AI model to:

- determine whether a specific person is guilty
- tell a user how to evade law enforcement
- fabricate legal rights
- fabricate legal institutions
- fabricate emergency contacts

AI output should be grounded in SafeSpace records.

## Unsupported Questions

If no verified information exists:

SafeSpace should say so.

Example:

"SafeSpace does not currently have verified information for this question. Please use one of the listed support services or seek qualified legal assistance."

## Privacy Philosophy

SafeSpace follows the principle:

Collect less. Protect more.