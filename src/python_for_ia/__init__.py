"""Small shared helpers for the course draft."""

from .synthetic import (
    image_with_background,
    images_with_problematic_hist,
    images_with_various_degradations,
    make_two_channel_cells,
    project_data,
)

__all__ = [
    "project_data",
    "image_with_background",
    "images_with_problematic_hist",
    "images_with_various_degradations",
    "make_two_channel_cells",
]
