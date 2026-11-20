# SafeSpace — Hackathon Demo Script
# OSF × Andela Hackathon
# Duration: ~3 minutes (2:58–3:12)
# Speaker: Emmanuel

---

## BEFORE YOU RECORD

1. Open this URL and wait for {"status":"ok"}:
   https://safespace-backend-qmvn.onrender.com/api/v1/health/

2. Open the live app in a clean Chrome window (no bookmarks bar if possible):
   https://safe-space-gmat5au2u-one-term.vercel.app

3. Close all other tabs. Turn off notifications (Windows: Focus Assist → Priority Only).

4. Set browser zoom to 100%. Full screen the browser (F11).

5. Open a screen recorder:
   - Windows built-in: Win + G → Capture → Start Recording
   - OR OBS Studio (free): https://obsproject.com
   - Record at 1920×1080, 30fps

6. Have this script open on a second screen or printed out.

---

## SCENE 1 — Homepage (0:00–0:20)

**ACTION:** Open https://safe-space-gmat5au2u-one-term.vercel.app
Slowly scroll down to show all three journey cards.

**SAY:**
"Hi, I'm Emmanuel, and this is SafeSpace — a trusted rights-information
and protection platform for young people in Kenya.

Young people facing sensitive situations don't just need information.
They need information they can understand, verify, and safely act on.

SafeSpace currently covers three journeys: teenage pregnancy,
sexual exploitation and abuse, and child justice."

---

## SCENE 2 — The Model (0:20–0:40)

**ACTION:** Click on "Child Justice" → click on "Arrest Rights" topic.
Slowly scroll to show UNDERSTAND, VERIFY sections.

**SAY:**
"SafeSpace is built around four principles: Understand, Verify, Act and Protect.

Unlike a conventional AI chatbot, SafeSpace does not treat AI as the
source of legal truth. Verified evidence is retrieved first,
and AI only helps explain that evidence."

---

## SCENE 3 — Teenage Pregnancy Demo (0:40–1:15)

**ACTION:**
- Click "Ask SafeSpace" in the navigation
- In the question box, type EXACTLY:
  "I am under 18 and pregnant. Can my school send me away?"
- Click "Ask SafeSpace" button
- Wait for the full response to load
- Slowly scroll through: answer → verified source → next steps

**SAY:**
"Here, a young person asks whether pregnancy means they can be sent
away from school.

SafeSpace identifies the relevant journey and retrieves verified
information from its curated Kenyan knowledge base —
in this case the National School Re-entry Guidelines, 2020.

It then provides a plain-language explanation together with its source
and appropriate next steps.

The user can see not only the answer, but exactly where that
information came from and when it was last verified."

---

## SCENE 4 — Safety Demo (1:15–1:50)

**ACTION:**
- Click "← Ask another question" to reset
- Type EXACTLY:
  "An adult I depend on is doing something sexual to me. Who can I tell?"
- Submit and wait for response
- Show the risk level, support services (Child Helpline 116, GBV 1195)

**SAY:**
"Sensitive safety questions are handled differently.

Before any AI generation, SafeSpace runs deterministic safety
classification based on verified rules.

When elevated risk is detected, safety and appropriate support
pathways become prominent — Child Helpline 116 and the GBV Helpline 1195.

The AI cannot downgrade this deterministic safety classification."

---

## SCENE 5 — The Trust Test (1:50–2:20) ← MOST IMPORTANT

**ACTION:**
- Click "← Ask another question" to reset
- Type EXACTLY:
  "What is the penalty for tax evasion in Kenya?"
- Submit and wait
- Show the INSUFFICIENT EVIDENCE response clearly
- Pause here for 5–8 seconds. Let judges read the screen.

**SAY:**
"But information you can trust also means knowing when NOT to answer.

Tax law is outside SafeSpace's verified knowledge base.

Instead of asking AI to guess, SafeSpace returns an insufficient
evidence response — and does not call AI at all.

SafeSpace would rather say it does not have enough verified
information than provide a confident but unsupported legal answer.

This is the design choice that makes SafeSpace trustworthy."

**[PAUSE 5 seconds on the screen before moving on]**

---

## SCENE 6 — Privacy + Quick Exit (2:20–2:40)

**ACTION:**
- Click the red "Quick Exit" button in the top right
  (IMPORTANT: have a second SafeSpace tab ready first so you can go back)
  OR just point to it without clicking and describe it

**SAY:**
"Privacy and protection are also part of the design.

No account is required to use SafeSpace. Questions are not
intentionally persisted by the platform.

Quick Exit allows a user to leave the application immediately.
It does not claim to delete browser history — that would be misleading."

---

## SCENE 7 — Technology (2:40–2:58)

**ACTION:**
- Open https://github.com/Emannuh/SafeSpace in a new tab
- Show the README briefly (scroll slowly)

**SAY:**
"The MVP uses Django, Django REST Framework and PostgreSQL on the
backend, with Next.js and TypeScript on the frontend.

OpenAI integration is controlled — the AI receives only pre-verified
evidence and cannot expand it.

The architecture separates the platform from its knowledge base,
creating a path toward locally verified knowledge packs
for other jurisdictions beyond Kenya."

---

## SCENE 8 — Closing (2:58–3:12)

**ACTION:**
- Go back to the SafeSpace homepage:
  https://safe-space-gmat5au2u-one-term.vercel.app
- Show the tagline "Understand your rights. Know your options."

**SAY:**
"SafeSpace demonstrates a different approach to AI for sensitive
public information.

We don't ask AI what your rights are.
We find verified rights information first, then use AI to help
you understand it.

That's SafeSpace: information you can understand, verify, act on —
and trust."

**[Hold on homepage for 3 seconds. End recording.]**

---

## AFTER RECORDING

1. Export as MP4, 1080p, H.264
2. Check duration is between 2:45 and 3:15
3. Check file size is under 250 MB
4. Name the file: SafeSpace_Hackathon_Demo.mp4
