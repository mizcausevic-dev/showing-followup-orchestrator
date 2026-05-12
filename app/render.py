from __future__ import annotations

import html
from pathlib import Path

from app.services.followup_service import build_service

service = build_service()


def page_shell(title: str, eyebrow: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #09111d;
      --panel: #101d2f;
      --panel-2: #17263c;
      --line: #29486f;
      --ink: #f3ecde;
      --muted: #b5c2d7;
      --blue: #6db2ff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background:
        radial-gradient(circle at top left, rgba(54, 103, 164, 0.18), transparent 30%),
        linear-gradient(180deg, #08111c 0%, #0b1522 100%);
      color: var(--ink);
      font-family: Georgia, "Times New Roman", serif;
    }}
    .frame {{
      width: 1440px;
      min-height: 920px;
      margin: 0 auto;
      padding: 48px;
    }}
    .shell {{
      background: rgba(13, 24, 39, 0.94);
      border: 1px solid var(--line);
      border-radius: 36px;
      padding: 34px 36px 36px;
    }}
    .eyebrow {{
      margin: 0 0 22px;
      font: 700 13px/1.2 "Segoe UI", sans-serif;
      letter-spacing: 0.35em;
      text-transform: uppercase;
      color: var(--blue);
    }}
    h1 {{
      margin: 0;
      font-size: 70px;
      line-height: 1.02;
      max-width: 1180px;
      letter-spacing: -0.05em;
    }}
    p.lead {{
      margin: 24px 0 0;
      max-width: 1060px;
      color: var(--muted);
      font: 400 19px/1.55 "Segoe UI", sans-serif;
    }}
    .pills {{
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
      margin: 22px 0 26px;
    }}
    .pill {{
      background: #1d2d45;
      border: 1px solid #335a8d;
      color: #f5f7fb;
      padding: 10px 16px;
      border-radius: 999px;
      font: 700 15px/1 "Segoe UI", sans-serif;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
      margin: 8px 0 34px;
    }}
    .card {{
      background: var(--panel-2);
      border: 1px solid #335885;
      border-radius: 24px;
      padding: 22px 22px 18px;
      min-height: 170px;
    }}
    .card h2 {{
      margin: 0 0 12px;
      color: #a8cbff;
      font: 700 12px/1.2 "Segoe UI", sans-serif;
      letter-spacing: 0.24em;
      text-transform: uppercase;
    }}
    .metric {{
      font-size: 58px;
      line-height: 1;
      margin: 0 0 10px;
    }}
    .card p, .card li, .table, .lane {{
      color: var(--muted);
      font: 400 18px/1.45 "Segoe UI", sans-serif;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1.2fr 0.9fr;
      gap: 18px;
    }}
    .table {{
      display: grid;
      gap: 12px;
    }}
    .row {{
      display: grid;
      grid-template-columns: 1.05fr 0.8fr 0.8fr 1fr;
      gap: 14px;
      align-items: center;
      padding: 16px 18px;
      background: #0c1728;
      border: 1px solid #223c5d;
      border-radius: 18px;
    }}
    .row strong {{
      color: var(--ink);
      display: block;
      font: 700 24px/1.1 Georgia, serif;
    }}
    .small {{
      font-size: 15px;
      color: #87a2c7;
    }}
    .lane {{
      padding: 16px 18px;
      background: #0c1728;
      border: 1px solid #223c5d;
      border-radius: 18px;
      margin-bottom: 12px;
    }}
    .lane strong {{
      display: block;
      color: var(--ink);
      font: 700 24px/1.15 Georgia, serif;
      margin-bottom: 6px;
    }}
    pre {{
      margin: 0;
      color: #d7e8ff;
      font: 16px/1.5 Consolas, monospace;
      white-space: pre-wrap;
    }}
  </style>
</head>
<body>
  <div class="frame">
    <div class="shell">
      <p class="eyebrow">{html.escape(eyebrow)}</p>
      {body}
    </div>
  </div>
</body>
</html>"""


def render_overview() -> str:
    summary = service.summary()
    queue = service.queue()[:3]
    rows = "".join(
        f"""
        <div class="row">
          <div>
            <strong>{html.escape(item['buyerName'])}</strong>
            <div class="small">{html.escape(item['listingTitle'])}</div>
          </div>
          <div>{item['intentScore']}</div>
          <div>{item['urgencyScore']}</div>
          <div>{html.escape(item['status'])}</div>
        </div>
        """
        for item in queue
    )
    body = f"""
      <h1>Turn every showing into a follow-up plan before buyer intent cools into indecision.</h1>
      <p class="lead">
        Showing Follow-up Orchestrator scores post-showing interest, urgency, objections, and timing so agents know who needs same-day action,
        who needs objection handling, and who belongs in a longer nurture lane.
      </p>
      <div class="pills">
        <div class="pill">post-showing intent scoring</div>
        <div class="pill">same-day follow-up routing</div>
        <div class="pill">objection-aware cadence</div>
        <div class="pill">buyer nurture sequencing</div>
      </div>
      <div class="stats">
        <div class="card"><h2>showings tracked</h2><div class="metric">{summary['showingCount']}</div><p>Buyer follow-up opportunities actively sequenced.</p></div>
        <div class="card"><h2>hot leads</h2><div class="metric">{summary['hotLeadCount']}</div><p>Buyers who need same-day follow-up and disclosure-ready outreach.</p></div>
        <div class="card"><h2>warm leads</h2><div class="metric">{summary['warmLeadCount']}</div><p>Buyers who still need fast follow-up with objection handling.</p></div>
        <div class="card"><h2>avg. intent</h2><div class="metric">{summary['averageIntentScore']}</div><p>{html.escape(summary['leadRecommendation'])}</p></div>
      </div>
      <div class="grid-2">
        <div class="card"><h2>follow-up queue</h2><div class="table">{rows}</div></div>
        <div class="card"><h2>lead recommendation</h2><p>{html.escape(summary['leadRecommendation'])}</p></div>
      </div>
    """
    return page_shell("Showing Follow-up Orchestrator", "Showing Follow-up Orchestrator", body)


def render_cadence_board() -> str:
    queue = service.queue()[:4]
    cards = "".join(
        f"""
        <div class="lane">
          <strong>{html.escape(item['buyerName'])} · {html.escape(item['status'])}</strong>
          <div>{html.escape(item['cadence'])}</div>
          <div class="small">{html.escape(item['nextAction'])}</div>
        </div>
        """
        for item in queue
    )
    body = f"""
      <h1>Cadence planning stays visible so agents can act with the right speed and message instead of sending the same template to everyone.</h1>
      <p class="lead">
        The board separates hot, warm, and cool buyer sequences and keeps channel choice attached to the actual showing outcome.
      </p>
      <div class="card">
        <h2>cadence board</h2>
        {cards}
      </div>
    """
    return page_shell("Cadence Board", "Cadence Board", body)


def render_intent_evidence() -> str:
    item = service.showing("shw-7002") or service.queue()[0]
    body = f"""
      <h1>Each showing record keeps enough signal to explain why a buyer is hot, warm, or cooling off.</h1>
      <p class="lead">
        Disclosures, second-showing interest, financing readiness, and objections all stay tied to the buyer follow-up path instead of getting lost in notes.
      </p>
      <div class="card">
        <h2>showing evidence</h2>
        <pre>{html.escape(str(item))}</pre>
      </div>
    """
    return page_shell("Intent Evidence", "Intent Evidence", body)


def render_api_summary() -> str:
    payload = service.sample_payload()
    body = f"""
      <h1>The API exposes follow-up priorities in a shape that agents, CRMs, and brokerage ops workflows can use immediately.</h1>
      <p class="lead">
        Intent, urgency, and next-action guidance stay together so downstream systems can trigger reminders and buyer sequences without extra interpretation.
      </p>
      <div class="card">
        <h2>sample payload</h2>
        <pre>{html.escape(str(payload))}</pre>
      </div>
    """
    return page_shell("API Summary", "API Summary", body)


def write_static_proof_pages(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    pages = {
        "01-overview.html": render_overview(),
        "02-cadence-board.html": render_cadence_board(),
        "03-intent-evidence.html": render_intent_evidence(),
        "04-api-summary.html": render_api_summary(),
    }
    written: list[Path] = []
    for name, contents in pages.items():
        path = output_dir / name
        path.write_text(contents, encoding="utf-8")
        written.append(path)
    return written
