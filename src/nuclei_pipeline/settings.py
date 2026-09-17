"""Pipeline parameters."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Parameters of one pipeline run. Lengths are in pixels."""

    nucleus_channel: int = 0
    target_channel: int = 1

    tophat_radius: int = 16

    gaussian_sigma: float = 5.0

    min_object_size: int = 150
    min_hole_size: int = 150
    opening_radius: int = 11

    peak_distance: int = 25
    peak_footprint: int = 12
