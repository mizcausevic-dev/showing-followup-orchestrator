from __future__ import annotations

import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from app.render import render_api_summary, render_cadence_board, render_intent_evidence, render_overview
from app.services.followup_service import build_service

app = FastAPI(
    title="Showing Follow-up Orchestrator",
    version="0.1.0",
    description=(
        "Real estate follow-up engine for post-showing sequencing, buyer-intent scoring, and agent reminder workflows."
    ),
)

service = build_service()


@app.get("/", response_class=HTMLResponse)
def overview() -> str:
    return render_overview()


@app.get("/cadence-board", response_class=HTMLResponse)
def cadence_board() -> str:
    return render_cadence_board()


@app.get("/intent-evidence", response_class=HTMLResponse)
def intent_evidence() -> str:
    return render_intent_evidence()


@app.get("/api-summary", response_class=HTMLResponse)
def api_summary_page() -> str:
    return render_api_summary()


@app.get("/api/dashboard/summary")
def dashboard_summary() -> dict:
    return service.summary()


@app.get("/api/showings")
def showings() -> list[dict]:
    return service.queue()


@app.get("/api/showings/{showing_id}")
def showing(showing_id: str) -> dict:
    value = service.showing(showing_id)
    if value is None:
        raise HTTPException(status_code=404, detail="Showing not found")
    return value


@app.get("/api/sample")
def sample() -> dict:
    return service.sample_payload()


@app.get("/openapi.json")
def openapi_spec() -> JSONResponse:
    return JSONResponse(json.loads(json.dumps(app.openapi())))


if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", "4806"))
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False)
