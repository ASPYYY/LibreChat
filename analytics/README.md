# LibreChat Analytics Module

This module adds **interaction recording** and **visual analytics** to [LibreChat](https://github.com/danny-avila/LibreChat).

## What was added

- `server.py` — Flask backend that records every user ↔ AI interaction to a local JSON file and exposes REST API endpoints
- `index.html` — Single-page analytics dashboard with:
  - Live chat interface with Mock AI responses
  - Real-time stats: total messages, tokens used, avg response time
  - Bar chart: messages per day
  - Doughnut chart: model usage distribution
  - Full interaction history log

## Architecture

```
User → index.html (Chat UI)
         ↓ POST /api/chat
       server.py (Flask)
         ↓ saves to
       interactions.json
         ↑ GET /api/analytics
       index.html (Dashboard)
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send message, get mock AI response, record interaction |
| GET | `/api/analytics` | Get stats and interaction history |
| DELETE | `/api/interactions` | Clear all recorded interactions |

## Mock AI

Real AI calls are replaced with random mock responses. The `model` field can be set per request (defaults to `mock-gpt-4`). Token counts and response times are randomly generated to simulate realistic data.

## Running locally

```bash
# Install dependencies
pip install flask flask-cors

# Start backend
cd analytics
python server.py
# Server runs on http://localhost:5001

# Open frontend
open index.html
# or serve with: python -m http.server 8080
```

## Demo mode

If the backend is not running, `index.html` automatically loads demo data so the dashboard is always viewable.

## Screenshot

See the dashboard in action — metrics cards, bar/doughnut charts, chat interface, and history panel all in a dark-themed UI.
