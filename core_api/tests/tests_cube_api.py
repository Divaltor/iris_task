from typing import Any

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class TestsCubesAPI:

    @pytest.mark.parametrize(
        'api_data',
        [
            [],
            'Test',
            123,
            {},
            ['a', 'b', 'c'],
            [1, 2, 'a'],
            [{}],
            [[]]
        ]
    )
    def test_api_with_invalid_data(self, api: APIClient, api_data: Any):
        response = api.post(
            reverse(
                'api.can_cube_stack'
            ),
            data={
                'cubes': api_data
            },
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize(
        'api_data',
        [
            [1, 3, 2],
            [3, 1, 2, 1],
            [6, 8, 0, 3, 4],
            [99, 100, 100, 0, 15],
            [100_000, 999_999, 100_000, 100_101],
            [1, 2, 3, 4, 4, 3, 2, 1]
        ]
    )
    def test_api_with_not_stacked_cubes(self, api: APIClient, api_data: Any):
        response = api.post(
            reverse(
                'api.can_cube_stack'
            ),
            data={
                'cubes': api_data
            },
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['can_stack'] is False
        assert response.data['cubes_volume'] == sum(side ** 3 for side in api_data)

    @pytest.mark.parametrize(
        'api_data',
        [
            [4, 3, 2, 1, 3, 4],
            [10, 10, 10],
            [0],
            [0, 1, 1],
            [15, 12, 6, 8, 13, 14],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1]
        ]
    )
    def test_api_with_stacked_cubes(self, api: APIClient, api_data: Any):
        response = api.post(
            reverse(
                'api.can_cube_stack'
            ),
            data={
                'cubes': api_data
            },
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['can_stack'] is True
        assert response.data['cubes_volume'] == sum(side ** 3 for side in api_data)
