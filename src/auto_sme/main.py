"""AutoSME — AI Automation for African Small Businesses (Production)."""
import os
import time
import uuid
import logging
from typing import Dict

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .routers import tasks, inventory, orders, reports, whatsapp

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logger = logging.getLogger("auto_sme")

# Settings
APP_VERSION = "0.2.0"
ENV = os.getenv("AUTOSME_ENV", "production")
ALLOWED_ORIGINS = os.getenv("AUTOSME_CORS_ORIGINS", "*").split(",")

# Metrics store (in-memory; use Redis in production)
metrics_store: Dict[str, int] = {
    "requests_total": 0,
    "requests_failed": 0,
}

def create_app() -> FastAPI:
    app = FastAPI(
        title="AutoSME",
        version=APP_VERSION,
        description="AI automation for African small businesses",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    @app.middleware("http")
    async def logging_middleware(request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id

        start_time = time.time()
        metrics_store["requests_total"] += 1

        try:
            response = await call_next(request)
            elapsed = time.time() - start_time
            logger.info(
                "request completed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": int(elapsed * 1000),
                }
            )
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as exc:
            metrics_store["requests_failed"] += 1
            logger.error(
                "request failed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(exc),
                },
                exc_info=True
            )
            raise

    @app.get("/health")
    def health():
        """Health check for load balancers."""
        return {
            "status": "ok",
            "timestamp": time.time(),
            "version": APP_VERSION,
            "environment": ENV,
        }

    @app.get("/metrics")
    def metrics():
        """Expose internal metrics."""
        return metrics_store

    # Include routers (they have their own API key dependency)
    app.include_router(tasks.router, prefix="/api/v1")
    app.include_router(inventory.router, prefix="/api/v1")
    app.include_router(orders.router, prefix="/api/v1")
    app.include_router(reports.router, prefix="/api/v1")
    app.include_router(whatsapp.router)  # /webhook/whatsapp

    # CORS — restrict in production
    if ENV == "production":
        origins = ALLOWED_ORIGINS if ALLOWED_ORIGINS != ["*"] else []
    else:
        origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "src.auto_sme.main:app",
        host="0.0.0.0",
        port=int(os.getenv("AUTOSME_PORT", 8000)),
        reload=ENV == "development",
    )
