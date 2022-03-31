from pydantic import BaseModel


class CubeModel(BaseModel):
    """Data structure for a cube."""

    side_size: int

    @property
    def volume(self) -> int:
        """Return cube volume."""
        return self.side_size ** 3
