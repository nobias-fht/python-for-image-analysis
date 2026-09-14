"""Measure labelled objects."""

import pandas as pd
from numpy.typing import NDArray
from skimage import measure


def measure_objects(labels: NDArray, channel: NDArray) -> pd.DataFrame:
    """Return one row per label, with area, intensity_mean and intensity_sum."""
    if labels.shape != channel.shape:
        raise ValueError(
            f"Labels and channel must share a shape, got {labels.shape} "
            f"and {channel.shape}."
        )
    properties = measure.regionprops_table(
        labels,
        intensity_image=channel,
        properties=("label", "area", "intensity_mean"),
    )
    table = pd.DataFrame(properties)
    table["intensity_sum"] = table["area"] * table["intensity_mean"]
    return table
