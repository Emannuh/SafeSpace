# SafeSpace Architecture

## Architecture Goal

SafeSpace should provide AI-assisted explanations without allowing the AI model to become the source of legal truth.

The system follows the principle:

Verified Source
↓
Structured Rights Record
↓
Controlled Retrieval
↓
AI Explanation
↓
Source Citation
↓
Next Action

## High-Level Components

### Frontend

Responsibilities:

- mobile-first user interface
- journey selection
- question submission
- display of rights information
- display of sources
- display of support services
- language selection
- Quick Exit

Proposed technology:

Next.js and Tailwind CSS

### Backend API

Responsibilities:

- expose journey and topic data
- retrieve rights records
- manage support services
- process user questions
- perform safety routing
- prepare grounded AI context
- return structured responses

Proposed technology:

Django and Django REST Framework

### Knowledge Database

Responsibilities:

- store journeys
- store legal topics
- store verified sources
- store rights records
- store support services
- store action pathways
- store translations
- store risk rules

Proposed technology:

PostgreSQL

### Safety Engine

Responsibilities:

- classify risk
- identify immediate danger
- bypass ordinary AI flows when necessary
- expose emergency support pathways

Proposed MVP approach:

deterministic safety rules plus AI-assisted classification

### Retrieval Layer

Responsibilities:

- map user questions to relevant topics
- retrieve the best matching verified records
- return only validated content to the AI layer

Initial approach:

structured database filtering

Future enhancement:

semantic search using pgvector

### AI Layer

Responsibilities:

- simplify complex legal language
- explain verified rights information
- classify intent where appropriate
- support multilingual explanation

The AI layer must not:

- invent laws
- invent legal procedures
- invent support institutions
- determine guilt or innocence

## Failure Behaviour

If AI is unavailable:

SafeSpace should still display structured legal content.

If no verified information exists:

SafeSpace should clearly state that it does not currently have verified information for the request.

If immediate danger is detected:

SafeSpace should prioritise safety and support information before normal legal explanation.