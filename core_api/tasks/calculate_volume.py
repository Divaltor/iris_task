import celery
from pydantic import validate_arguments

from core_api.schema.cube import CubeModel
from settings.celery import app


class CalculateCubesVolume(celery.Task):

    name = 'core.cube.calculate_volume'

    @validate_arguments
    def run(self, cubes: list[CubeModel]) -> int:
        """Return sum of cubes volume."""
        return sum(cube.volume for cube in cubes)


CalculateCubesVolumeTask: CalculateCubesVolume = app.register_task(CalculateCubesVolume)
