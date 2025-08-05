from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import asdict

from data.gfgUserProfile import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/gfg/{username}")
def get_gfg_profile(username: str):
    try:
        profile = scrape_gfg_profile(username)
        return asdict(profile)
    except Exception as e:
        return {"error": str(e)}