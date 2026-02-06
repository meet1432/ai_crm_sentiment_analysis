---
title: AI Deal Sentiment API
<<<<<<< HEAD
emoji: 🐨
colorFrom: gray
colorTo: purple
sdk: docker
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
=======
colorFrom: gray
colorTo: blue
sdk: docker
pinned: false
short_description: Sentiment API with a simple web UI
---

# AI Deal Sentiment API

A FastAPI service that analyzes customer chat/email sentiment and returns a label, score, and brief reason. Includes a simple web UI.

## Features
- `/sentiment` API for positive/neutral/negative detection
- `/health` for readiness checks
- Simple web UI at `/`

## Run (Local)

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 7860
```

## Run (Docker)

```bash
docker build -t ai-deal-sentiment-api .
docker run -p 7860:7860 ai-deal-sentiment-api
```

## API

### POST `/sentiment`

```json
{
  "text": "Customer message here"
}
```

Response:
```json
{
  "label": "positive",
  "score": 0.82,
  "brief_reason": "Customer intent to buy detected"
}
```

### GET `/health`
Returns:
```json
{ "status": "ok" }
```
>>>>>>> ff9fb03 ([ADD]Initial Commit)
