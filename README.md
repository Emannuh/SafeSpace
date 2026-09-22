# SafeSpace

**Trusted rights information for young people in Kenya.**

SafeSpace gives young people clear, verified information about their legal rights and protections — and practical steps they can take. No account required.

---

## Problem

Young people in Kenya may encounter situations involving teenage pregnancy, sexual exploitation, abuse, or contact with the justice system without knowing the rights and protections available to them.

Legal information exists — but it is often fragmented across legislation, government agencies, policies, and institutions, and is difficult to understand during a difficult or urgent moment.

SafeSpace provides simple, traceable, and actionable rights information grounded in authoritative Kenyan sources.

---

## MVP Journeys

SafeSpace currently supports three journeys:

**Teenage Pregnancy** — education rights during and after pregnancy, including the right to stay in school, school re-entry, national examinations, and appropriate support.

**Sexual Exploitation and Abuse** — legal protections against sexual exploitation and abuse, safe reporting options, and pathways to support and protection.

**Child Justice** — rights when a young person is involved in a police or justice process: arrest rights, legal representation, parental involvement, detention protections, and diversion.

---

## How SafeSpace Works

```
User question
      ↓
Deterministic safety classification (RiskRules)
      ↓
Journey and topic classification (keyword matching)
      ↓
VERIFIED evidence retrieval (active=True AND status=VERIFIED only)
      ↓
Sufficient evidence? → grounded AI explanation
No evidence?        → "SafeSpace does not yet have enough verified information"
IMMEDIATE risk?     → safety pathway, no AI explanation
      ↓
Structured response:
  answer + verified sources + action steps + support services
```

**UNDERSTAND** → What are my rights?
**VERIFY** → Where does this come from? (source + last verified date)
**ACT** → What can I do next?
**PROTECT** → Where can I get help?

---

## Trust Model

- Every rights record is linked to an authoritative Kenyan legal source.
- Only records marked **VERIFIED** and **active** are returned by the API.
- The AI layer explains verified evidence — it does not generate legal claims.
- If no verified evidence exists, SafeSpace says so. AI is not called.
- Immediate-risk situations bypass the AI explanation entirely.
- Policy and government guidance are labelled differently from legislation.
- Every response includes source title, publisher, and last verification date.
- Human legal review governs which records are marked VERIFIED.

---

## Privacy

- No account required for any core functionality.
- SafeSpace minimises personal data collection.
- User questions submitted to the Ask feature are not intentionally stored.
- Questions are not written to browser localStorage, sessionStorage, or cookies.
- The Safety Check and Ask features do not create user records.
- **Quick Exit** leaves SafeSpace immediately but does not erase browser history or device activity.
- When AI is enabled, the user's question is processed by the configured AI provider (OpenAI). This is disclosed in the UI.
- Hosting infrastructure may produce ordinary technical server logs outside SafeSpace's control.

---

## Technology

**Backend:** Django 6 · Django REST Framework · PostgreSQL · WhiteNoise · Gunicorn

**Frontend:** Next.js 16 · TypeScript · Tailwind CSS

**AI:** OpenAI API (optional) — evidence-grounded explanation only. SafeSpace operates in deterministic-only mode if `AI_API_KEY` is not set.

---

## Live Demo

- **Frontend:** https://safe-space-gmat5au2u-one-term.vercel.app
- **Backend API:** https://safespace-backend-qmvn.onrender.com/api/v1/
- **Health check:** https://safespace-backend-qmvn.onrender.com/api/v1/health/

> Note: The backend runs on Render's free tier and may take ~30 seconds to wake up after inactivity. Load the health check URL first if the app feels slow on first open.

---

## Local Development

### Prerequisites
- Python 3.11+
- Node.js 22 LTS
- PostgreSQL 14+

### Backend setup

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env with your PostgreSQL credentials and a strong SECRET_KEY

python manage.py migrate
python manage.py seed_demo       # Load demo knowledge data
python manage.py runserver
```

### Frontend setup

```bash
cd frontend
npm install

cp .env.local.example .env.local
# Edit .env.local — set NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1

npm run dev
```

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes | Strong random Django secret key |
| `DEBUG` | No | `True` for development only. Default: `False` |
| `ALLOWED_HOSTS` | No | Comma-separated hostnames. Default: `127.0.0.1,localhost` |
| `HTTPS` | No | Set `True` in production to enable secure cookies and HSTS |
| `DATABASE_URL` | No | PostgreSQL URL (Railway style). Takes priority over individual vars |
| `DB_NAME` | No | Database name. Default: `safespace` |
| `DB_USER` | No | Database user. Default: `postgres` |
| `DB_PASSWORD` | No | Database password |
| `DB_HOST` | No | Database host. Default: `localhost` |
| `DB_PORT` | No | Database port. Default: `5432` |
| `CORS_ALLOWED_ORIGINS` | No | Frontend origins. Default: localhost:3000 |
| `CSRF_TRUSTED_ORIGINS` | No | Frontend origins for CSRF. Default: localhost:3000 |
| `AI_PROVIDER` | No | AI provider. Default: `openai` |
| `AI_API_KEY` | No | AI API key. Empty = deterministic-only mode |
| `AI_MODEL` | No | AI model. Default: `gpt-4o-mini` |

### Frontend (`frontend/.env.local`)

| Variable | Required | Description |
|---|---|---|
| `NEXT_PUBLIC_API_BASE_URL` | Yes | Django API base URL, e.g. `http://localhost:8000/api/v1` |

---

## Testing

```bash
# Backend (from backend/)
python manage.py test core --verbosity=1

# Frontend (from frontend/)
npm test

# Production build check (from frontend/)
npm run build
```

**Current test counts:** 120 backend · 31 frontend

---

## Database Initialisation

For a fresh deployment, run in this order:

```bash
python manage.py migrate
python manage.py seed_demo
```

`seed_demo` is idempotent — safe to run multiple times. Do **not** use `--reset` in production unless you intend to wipe all knowledge data.

---

## Deployment

### Backend (Railway)

The backend includes `railway.json` and `Procfile` for Railway deployment.

Set these environment variables in your Railway service:
- `SECRET_KEY` — generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- `DATABASE_URL` — provided automatically by Railway PostgreSQL plugin
- `ALLOWED_HOSTS` — your Railway domain
- `CORS_ALLOWED_ORIGINS` — your frontend domain
- `CSRF_TRUSTED_ORIGINS` — your frontend domain
- `HTTPS=True`
- `AI_API_KEY` — your OpenAI API key (optional)
- `DEBUG` — leave unset (defaults to `False`)

Railway deploy sequence (handled automatically by `railway.json`):
```
pip install -r requirements.txt
python manage.py migrate --no-input
python manage.py collectstatic --no-input
gunicorn safespace_backend.wsgi
```

Run seed data once after first deploy:
```bash
railway run python manage.py seed_demo
```

### Frontend (Vercel / Railway)

Set `NEXT_PUBLIC_API_BASE_URL` to your deployed backend URL, then:

```bash
npm run build
npm run start
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/health/` | Health check |
| GET | `/api/v1/journeys/` | Active journeys |
| GET | `/api/v1/journeys/<slug>/topics/` | Topics in a journey |
| GET | `/api/v1/journeys/<slug>/topics/<slug>/rights/` | Verified rights records |
| GET | `/api/v1/journeys/<slug>/topics/<slug>/actions/` | Verified action steps |
| GET | `/api/v1/rights/<record_code>/` | Single rights record |
| GET | `/api/v1/support-services/` | Verified support services |
| POST | `/api/v1/safety/check/` | Deterministic risk classification |
| POST | `/api/v1/ask/` | AI-grounded question answering |

---

## Limitations

- SafeSpace provides **information**, not legal advice. It is not a substitute for qualified legal representation.
- The knowledge base covers Kenya MVP journeys only. Content is limited to what has been verified against authoritative sources.
- AI explanations are grounded in retrieved verified records — the AI does not determine legal truth.
- Support services listed are external organisations. SafeSpace does not operate them and cannot guarantee availability.
- Emergency services (999 / 112) are always available regardless of SafeSpace's status.

---

## AI Coding Usage

SafeSpace was built with AI coding assistance (Kiro) for implementation, testing, documentation, and debugging. All product decisions, architecture decisions, journey scope, legal content approval, and trust model design were made by the human developer. No legal content was generated without reference to approved authoritative Kenyan sources listed in `docs/03-legal-framework.md`.
