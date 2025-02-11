from fastapi import FastAPI

from presentation.api.service_a.v1.healthcheck.router import router as healthcheck_router


def apply_routes(app: FastAPI) -> FastAPI:
    app.include_router(healthcheck_router)
    return app
