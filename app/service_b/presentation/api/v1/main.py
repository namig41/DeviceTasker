from fastapi import FastAPI

import uvicorn
from service_b.presentation.api.v1.lifespan import lifespan
from service_b.presentation.api.v1.middleware import apply_middleware
from service_b.presentation.api.v1.router import apply_routes
from service_b.settings.config import settings


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(
        title="ServiceB",
        docs_url="/api/docs/",
        debug=True,
        lifespan=lifespan,
    )

    app = apply_routes(apply_middleware(app))

    return app


if __name__ == "__main__":

    uvicorn.run(
        "main:create_app",
        factory=True,
        host=settings.SERVICE_B_API_HOST,
        port=settings.SERVICE_B_API_PORT,
        log_level="debug",
        reload=True,
        workers=1,
    )
