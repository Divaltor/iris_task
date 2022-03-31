import celery
from pydantic import validate_arguments

from core_api.schema.cube import CubeModel
import collections

from settings.celery import app


class CalculateCubeStack(celery.Task):

    name = 'core.cube.calculate_stack'

    @validate_arguments
    def run(self, cubes: list[CubeModel]) -> bool:
        # Create deque with optimized deletion of the first element
        cubes = collections.deque(cubes)

        result = []

        # Iterate through the cubes and create a list with the faces of cubes by decreasing order
        # like [4, 4, 3, 2, 1]
        for _ in range(len(cubes)):
            if cubes[0].side_size <= cubes[-1].side_size:
                result.append(cubes.pop())
            else:
                result.append(cubes.popleft())

        # Check the list for the presence of ordered elements in decreasing order
        for index in range(len(result) - 1):
            # if the next cube is larger than current, then they can't be stacked
            if result[index].side_size < result[index + 1].side_size:
                return False

        return True


CalculateCubeStackTask: CalculateCubeStack = app.register_task(CalculateCubeStack)
