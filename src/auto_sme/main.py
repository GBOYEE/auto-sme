"""FastAPI application for AutoSME."""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .routers import tasks, inventory, orders, reports, whatsapp
from .dependencies import get_api_key
import yaml

def create_app() -> FastAPI:
    app = FastAPI(title="AutoSME", version="0.1.0")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    app.include_router(tasks.router, prefix="/api/v1")
    app.include_router(inventory.router, prefix="/api/v1")
    app.include_router(orders.router, prefix="/api/v1")
    app.include_router(reports.router, prefix="/api/v1")
    app.include_router(whatsapp.router)  # /webhook/whatsapp

    # CORS (allow all for now)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

app = create_app()
