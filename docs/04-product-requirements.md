# Product Requirements

## Functional Requirements

FR-01
Users can select one of the three SafeSpace journeys.

FR-02
Users can browse predefined rights questions.

FR-03
Users can submit a natural-language question.

FR-04
The system classifies the question into a known topic.

FR-05
The system retrieves relevant verified rights records.

FR-06
The system provides a plain-language explanation.

FR-07
Every legal answer displays its source.

FR-08
The system displays the last verification date.

FR-09
Users receive practical next-step guidance.

FR-10
Users can view appropriate verified support services.

FR-11
The system performs risk classification.

FR-12
Immediate-risk questions trigger the safety journey.

FR-13
Core content is available without creating an account.

FR-14
Selected content can be viewed in English and Kiswahili.

FR-15
A Quick Exit feature is available.

FR-16
Administrators can add or update rights records.

FR-17
Administrators can update source verification dates.

FR-18
Administrators can deactivate outdated content.

FR-19
AI-generated explanations must be grounded in retrieved SafeSpace records.

FR-20
If no verified record exists, the system must not invent an answer.

## Non-Functional Requirements

### Privacy

The system should minimise collection of sensitive or identifying information.

### Security

Production communication should use HTTPS.

API credentials and secret keys must not be stored in source code.

### Accessibility

The interface should use readable typography, clear navigation, large interaction targets, and semantic markup.

### Performance

The core experience should remain useful on low-bandwidth mobile connections.

### Reliability

Static rights content should remain available even when the AI service is unavailable.

### Traceability

Every legal answer must be linked to a verified source.

### Maintainability

Legal information should be editable through the content-management layer without requiring application code changes.

### Scalability

Jurisdiction, language, support services, and legal sources should be data-driven.

### Safety

High-risk requests should take priority over normal informational responses.

### Transparency

Users should be informed when AI is used to simplify verified information.