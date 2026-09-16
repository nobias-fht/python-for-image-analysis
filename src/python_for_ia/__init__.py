"""Small shared helpers for the course draft."""

from .synthetic import (
    image_with_background,
    images_with_problematic_hist,
    images_with_various_degradations,
)
from .tabular_data import get_measurement_paths

__all__ = [
    "image_with_background",
    "images_with_problematic_hist",
    "images_with_various_degradations",
    "get_measurement_paths",
]
