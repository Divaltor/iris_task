from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from pydantic import ValidationError
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from core_api.tasks.calculate_cube_stack import CalculateCubeStackTask
from core_api.tasks.calculate_volume import CalculateCubesVolumeTask
from core_api.tasks.convert_cube import ConvertCubesTask


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        name='',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'cubes': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_INTEGER
                    ),
                    description='List with numbers - each number is size of a cube'
                )
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Success response',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'can_stack': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            description='Boolean value if cubes can be stacked'
                        ),
                        'cubes_volume': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description='The sum of the volumes of all cubes'
                        )
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: 'Error response with invalid passed data'
        }
    )
)
class CalculateCubeStackAPI(GenericAPIView):

    # noinspection PyMethodMayBeStatic
    def post(self, request: Request) -> Response:
        raw_cubes = request.data.get('cubes')

        if not raw_cubes or not isinstance(raw_cubes, list):
            return Response(
                data={
                    'error': 'Passed data must be non empty array with numbers'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validated_cubes = ConvertCubesTask.delay(raw_cubes).get()
        except ValidationError:
            return Response(
                data={
                    'error': 'Passed data has invalid values (not numbers)'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        can_stack_cubes = CalculateCubeStackTask.delay(validated_cubes)
        cubes_volume = CalculateCubesVolumeTask.delay(validated_cubes)

        return Response(
            data={
                'can_stack': can_stack_cubes.get(),
                'cubes_volume': cubes_volume.get()
            },
            status=status.HTTP_200_OK
        )
