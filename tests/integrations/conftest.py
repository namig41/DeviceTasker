from fastapi import FastAPI
from fastapi.testclient import TestClient

import pytest
from service_a.bootstrap.di import init_container as container_a
from service_a.presentation.api.v1.main import create_app as create_service_a_app
from service_b.bootstrap.di import init_container as container_b
from service_b.presentation.api.v1.main import create_app as create_service_b_app

from tests.fixtures import init_dummy_container


@pytest.fixture(scope="session")
def service_a() -> FastAPI:
    app: FastAPI = create_service_a_app()
    app.dependency_overrides[container_a] = init_dummy_container
    return app


@pytest.fixture(scope="session")
def service_b() -> FastAPI:
    app: FastAPI = create_service_b_app()
    app.dependency_overrides[container_b] = init_dummy_container
    return app


@pytest.fixture(scope="session")
def service_a_client(service_a: FastAPI) -> TestClient:
    return TestClient(app=service_a)


@pytest.fixture(scope="session")
def service_b_client(service_b: FastAPI) -> TestClient:
    return TestClient(app=service_b)
