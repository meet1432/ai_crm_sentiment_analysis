from functools import lru_cache
import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import re
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

app = FastAPI(title="AI Deal Sentiment API")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

MODEL_NAME = os.getenv("SENTIMENT_MODEL", "IberaSoft/customer-sentiment-analyzer")


class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1)


class SentimentResponse(BaseModel):
    label: str
    score: float
    brief_reason: str


@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    return pipeline("text-classification", model=model, tokenizer=tokenizer)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/sentiment", response_model=SentimentResponse)
def sentiment(payload: SentimentRequest) -> SentimentResponse:
    if not payload.text.strip():
        return SentimentResponse(label="neutral", score=0.0, brief_reason="No customer chat to assess")

    classifier = get_sentiment_pipeline()
    result = classifier(payload.text[:4000])
    print("result:", result)
    if not result:
        raise HTTPException(status_code=500, detail="Sentiment model returned no result")

    data = result[0]
    label = (data.get("label") or "neutral").lower()
    score = float(data.get("score", 0.0))

    normalized = payload.text.lower()
    normalized = normalized.replace("’", "'")
    normalized = re.sub(r"[^a-z0-9\\s']", " ", normalized)
    normalized = re.sub(r"\\s+", " ", normalized).strip()

    disinterest = [
        "not interested",
        "dont want to buy",
        "don't want to buy",
        "do not want to buy",
        "wont buy",
        "won't buy",
        "not good",
    ]
    positive_intent = [
        "interested",
        "want to buy",
        "would like to buy",
        "ready to buy",
        "buy in cash",
        "purchase",
        "proceed",
    ]

    if any(k in normalized for k in disinterest):
        return SentimentResponse(label="negative", score=1.0, brief_reason="Explicit disinterest from customer")
    if any(k in normalized for k in positive_intent):
        return SentimentResponse(label="positive", score=max(score, 0.7), brief_reason="Customer intent to buy detected")

    if label == "negative" and score >= 0.6:
        reason = f"Negative sentiment detected (score {score:.2f})"
    elif label == "positive" and score >= 0.6:
        reason = f"Positive sentiment detected (score {score:.2f})"
    else:
        reason = f"Neutral sentiment (score {score:.2f})"

    return SentimentResponse(label=label, score=score, brief_reason=reason)
