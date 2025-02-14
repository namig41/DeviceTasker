from fastapi import FastAPI

from service_a.presentation.api.v1.device_task.router import router as device_task_router
from service_a.presentation.api.v1.healthcheck.router import router as healthcheck_router


def apply_routes(app: FastAPI) -> FastAPI:
    app.include_router(healthcheck_router)
    app.include_router(device_task_router)
    return app
