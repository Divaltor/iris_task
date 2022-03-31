import celery
from pydantic import validate_arguments

from core_api.schema.cube import CubeModel
import collections

from settings.celery import app


class CalculateCubeStack(celery.Task):

    name = 'core.cube.calculate_stack'

    @validate_arguments
    def run(self, cubes: list[CubeModel]) -> bool:
        cubes = collections.deque(cubes)

        result = []

        for _ in range(len(cubes)):
            if cubes[0].side_size <= cubes[-1].side_size:
                result.append(cubes.pop())
            else:
                result.append(cubes.popleft())

        for index in range(len(result) - 1):
            if result[index].side_size < result[index + 1].side_size:
                return False

        return True


CalculateCubeStackTask: CalculateCubeStack = app.register_task(CalculateCubeStack)
