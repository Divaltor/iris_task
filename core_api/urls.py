from django.urls import include, path

from core_api.api.v1.cubes import CalculateCubeStackAPI

api_v1 = [
    path('can-cubes-stack', CalculateCubeStackAPI.as_view(), name='api.can_cube_stack')
]


urlpatterns = [
    path('v1/', include(api_v1))
]
