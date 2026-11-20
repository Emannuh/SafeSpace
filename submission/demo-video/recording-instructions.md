# SafeSpace Demo — Recording Instructions

## What you need (all free)

1. **Screen recorder** — use Windows built-in:
   - Press Win + G → click the red Record button
   - OR download OBS Studio: https://obsproject.com (better quality)

2. **Microphone** — your laptop mic is fine. Record somewhere quiet.

3. **Time needed** — about 20–30 minutes total.

---

## Step-by-step

### Step 1 — Wake the backend (do this first)
Open this URL and wait for {"status":"ok"} to appear:
https://safespace-backend-qmvn.onrender.com/api/v1/health/

This wakes up the Render server. Takes up to 30 seconds.

### Step 2 — Prepare Chrome
- Open a new Chrome window (not incognito)
- Go to: https://safe-space-gmat5au2u-one-term.vercel.app
- Confirm the three journey cards load
- Hide bookmarks bar: Ctrl+Shift+B
- Set zoom: Ctrl+0 (resets to 100%)
- Full screen: F11

### Step 3 — Turn off notifications
- Windows: Start → Focus Assist → Priority Only
- Close Slack, Teams, email

### Step 4 — Start recording
- Win + G → Start Recording (or OBS: click Start Recording)

### Step 5 — Record following the script
- Open: SafeSpace_Demo_Script.md
- Read through it once before recording
- Go scene by scene — you can pause and re-record

### Step 6 — The three key demo questions (type these EXACTLY)

**Scene 3:**
"I am under 18 and pregnant. Can my school send me away?"

**Scene 4:**
"An adult I depend on is doing something sexual to me. Who can I tell?"

**Scene 5 — MOST IMPORTANT:**
"What is the penalty for tax evasion in Kenya?"
→ This MUST show the insufficient-evidence response
→ Pause on this screen for 5 seconds

### Step 7 — Stop recording
- Stop after the homepage closing shot
- Win + G → Stop Recording

### Step 8 — Export
- Windows Game Bar saves to: C:\Users\YourName\Videos\Captures\
- If using OBS: File is in your OBS output folder
- Rename to: SafeSpace_Hackathon_Demo.mp4

### Step 9 — Check
- Duration: should be 2:45–3:15
- File size: under 250 MB
- Watch it back and confirm all three demo responses show correctly

---

## If something goes wrong

**Backend shows an error instead of a response:**
The Render server may have gone to sleep. Reload the health check URL,
wait 30 seconds, try again.

**Journey cards don't load:**
Hard refresh: Ctrl+Shift+R

**The tax evasion question returns a real answer instead of INSUFFICIENT:**
Stop. Do not submit that recording. Report the issue.

---

## Upload to hackathon portal

Upload: SafeSpace_Hackathon_Demo.mp4

Supported formats: MP4 / MOV / WebM / AVI
Maximum size: 250 MB
