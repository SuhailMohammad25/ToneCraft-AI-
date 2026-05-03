# ToneCraft AI: Emotion-Aware Response Composer

ToneCraft AI is a customer experience GenAI tool for support agents. It analyzes a customer message, detects sentiment and emotional state, then generates empathetic, brand-aligned support replies for email, chat, WhatsApp, and social media.

The app works with an OpenAI-compatible LLM when `OPENAI_API_KEY` is configured. Without an API key, it still runs offline using rule-based emotion detection and high-quality response templates.

## Features

- Paste a customer message and choose brand tone plus channel
- Detect sentiment, emotion, intensity, and reason
- Generate a main empathetic support reply
- Generate short, detailed, and de-escalation alternatives
- Show do/don't guidance for the support agent
- Save generated cases to SQLite
- Browse, reload, reopen, and delete saved cases
- Copy generated replies to the clipboard
- Run locally or with Docker Compose

## Tech Stack

- Backend: Python, FastAPI, SQLAlchemy, SQLite, Pydantic
- AI/NLP: OpenAI-compatible chat API, optional Transformers sentiment pipeline if installed, rule-based offline fallback
- Frontend: React, Vite, Tailwind CSS, lucide-react
- Testing: pytest and FastAPI TestClient

## Folder Structure

```text
backend/
  app/
    main.py
    config.py
    database.py
    models.py
    schemas.py
    services/
      sentiment_service.py
      llm_service.py
      response_service.py
    routers/
      analyze.py
      cases.py
    prompts/
      response_prompt.py
  tests/
    test_analyze.py
  requirements.txt
frontend/
  src/
    App.jsx
    main.jsx
    index.css
    api.js
    components/
      Header.jsx
      AnalyzeForm.jsx
      ResultPanel.jsx
      SavedCases.jsx
      LoadingState.jsx
  package.json
  vite.config.js
  tailwind.config.js
  postcss.config.js
README.md
.env.example
.gitignore
docker-compose.yml
```

## Environment Variables

Copy `.env.example` to `.env` at the project root if you want local environment configuration.

```bash
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=
# Optional. If omitted, SQLite is stored in a writable local runtime directory.
# DATABASE_URL=sqlite:///./data/tonecraft.db
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
VITE_API_BASE_URL=http://localhost:8000
```

`OPENAI_BASE_URL` can point to another OpenAI-compatible provider. Leave `OPENAI_API_KEY` empty to use the offline fallback. `DATABASE_URL` is optional; by default the backend stores SQLite data in a writable local runtime directory to avoid file-locking issues in synced project folders.

## Run Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

On macOS or Linux, activate the environment with:

```bash
source .venv/bin/activate
```

Health check:

```bash
curl http://localhost:8000/health
```

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

If `vite` dev mode is blocked on your machine, use the production build locally:

```bash
cd frontend
npm install
npm run build
npm run serve
```

To point the frontend at a different backend:

```bash
VITE_API_BASE_URL=http://localhost:8000 npm run dev
```

On Windows PowerShell:

```powershell
$env:VITE_API_BASE_URL="http://localhost:8000"; npm run dev
```

## Run With Docker Compose

```bash
docker compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- SQLite data is stored in the `tonecraft-data` Docker volume.
- The Docker frontend serves the production build instead of the Vite dev server.

## API Examples

Analyze a message:

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "customer_message": "I have contacted your team three times and nobody has solved my refund issue. This is extremely frustrating and I want an answer today.",
    "brand_tone": "Apologetic",
    "channel": "Email"
  }'
```

Save a case:

```bash
curl -X POST http://localhost:8000/api/cases \
  -H "Content-Type: application/json" \
  -d '{ "customer_message": "...", "brand_tone": "Warm", "channel": "Chat", "sentiment": "Negative", "emotion": "Frustration", "intensity": 82, "emotion_reason": "...", "tone_adjustment": "...", "main_reply": "...", "alternatives": { "short": "...", "detailed": "...", "de_escalation": "..." }, "agent_guidance": { "do": ["..."], "dont": ["..."] } }'
```

List saved cases:

```bash
curl http://localhost:8000/api/cases
```

Delete a case:

```bash
curl -X DELETE http://localhost:8000/api/cases/1
```

## Offline Fallback

ToneCraft never fails just because an API key is missing.

- Sentiment analysis first attempts to use a local `transformers` sentiment pipeline if the package is installed and available.
- If Transformers is not installed or cannot load, the backend uses a keyword-weighted rule-based analyzer for anger, frustration, confusion, disappointment, urgency, and satisfaction.
- Response generation uses an OpenAI-compatible LLM when `OPENAI_API_KEY` exists.
- Without an API key, the backend uses channel-aware, tone-aware templates that still acknowledge the emotion, avoid blame, avoid overpromising, and provide practical next steps.

Optional local model support:

```bash
cd backend
pip install transformers torch
```

## Tests

```bash
cd backend
pytest
```

The tests cover the health endpoint, sample frustrated refund analysis, and saved-case CRUD.

## Future Improvements

- Add authentication and per-agent case history
- Add team-level brand voice presets
- Add streaming response generation
- Add CRM/helpdesk integrations
- Add human feedback scoring for response quality
- Add analytics for recurring customer emotions and issue themes
- Add frontend unit tests with Vitest and React Testing Library
