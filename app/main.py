"""
HALT / Food Radar — FastAPI entrypoint.

Run: uvicorn app.main:app --reload --port 8000
Open: http://localhost:8000
"""
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app import engine, repository
from app.schemas import PlaceCard, PlaceDetail, Verdict, VerdictNamed

app = FastAPI(title="HALT / Food Radar", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
if _STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")


@app.get("/health")
def health():
    return {"status": "ok", "version": app.version}


@app.get("/places", response_model=List[PlaceCard])
def list_places():
    out: List[PlaceCard] = []
    for p in repository.list_places():
        v = engine.compute_verdict(p)
        out.append(
            PlaceCard(
                id=p["id"],
                name=p["name"],
                cuisine=p["cuisine"],
                address=p["address"],
                district=p.get("district"),
                sector=p.get("sector"),
                lat=p["lat"],
                lng=p["lng"],
                verdict=v["verdict"],
                explanation=v["explanation"],
                sources=v["sources"],
            )
        )
    return out


@app.get("/places/{place_id}", response_model=PlaceDetail)
def get_place(place_id: str):
    p = repository.get_place(place_id)
    if not p:
        raise HTTPException(status_code=404, detail="Place not found")
    v = engine.compute_verdict(p)
    return PlaceDetail(
        id=p["id"],
        name=p["name"],
        cuisine=p["cuisine"],
        address=p["address"],
        district=p.get("district"),
        sector=p.get("sector"),
        lat=p["lat"],
        lng=p["lng"],
        verdict=Verdict(**v),
    )


@app.get("/verdict/{place_id}", response_model=VerdictNamed)
def get_verdict(place_id: str):
    p = repository.get_place(place_id)
    if not p:
        raise HTTPException(status_code=404, detail="Place not found")
    v = engine.compute_verdict(p)
    return VerdictNamed(name=p["name"], **v)


@app.get("/", response_class=HTMLResponse)
def index():
    html_path = _STATIC_DIR / "index.html"
    if html_path.exists():
        return HTMLResponse(html_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>HALT / Food Radar</h1><p>See /docs</p>")
