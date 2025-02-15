from punq import Container
from service_b.bootstrap.di import _init_container


def init_dummy_container() -> Container:
    container: Container = _init_container()
    return container
