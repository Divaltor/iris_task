import logging

import celery

from core_api.schema.cube import CubeModel
from settings.celery import app


logger = logging.getLogger(__name__)


class ConvertCubes(celery.Task):

    name = 'core.cube.create_models'

    def run(self, cubes: list[int]) -> list[dict]:
        """
        Validate input cubes and convert them to Cube structure.

        Args:
            cubes: list with numbers, each number is a size of cube side

        Returns:
            List with converted cube structure to dict for storing in Redis as JSON
        """
        logger.info(cubes)

        validated_cubes = [CubeModel(side_size=cube).dict() for cube in cubes]

        return validated_cubes


ConvertCubesTask: ConvertCubes = app.register_task(ConvertCubes)
