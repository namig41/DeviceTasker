from fastapi import APIRouter

from service_a.presentation.api.v1.healthcheck.schemas import HealthcheckResponseSchema


router = APIRouter(
    prefix="/ping",
    tags=["ping"],
)


@router.get(
    "",
    description="Application status",
    response_model=HealthcheckResponseSchema,
)
def get_healthcheck_status() -> HealthcheckResponseSchema:
    return HealthcheckResponseSchema()
