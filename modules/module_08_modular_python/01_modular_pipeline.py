# %% [markdown]
# # Module 8: modular Python
#
# Essential ideas: functions name reusable actions; dataclasses bundle related
# settings; enums avoid magic strings; classes can collect state when useful.

# %%
from dataclasses import dataclass
from enum import Enum

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import ndimage as ndi
from skimage import filters, measure, morphology, segmentation

from course_utils import make_two_channel_cells

# %%


class PopulationRule(Enum):
    RATIO_ONE = "ratio_one"
    MEDIAN_RATIO = "median_ratio"


@dataclass
class SegmentationSettings:
    min_size: int = 80
    hole_area: int = 80
    population_rule: PopulationRule = PopulationRule.RATIO_ONE


def segment_instances(channel_a: np.ndarray, channel_b: np.ndarray, settings: SegmentationSettings) -> np.ndarray:
    combined = channel_a + channel_b
    mask = combined > filters.threshold_otsu(combined)
    mask = morphology.remove_small_objects(mask, min_size=settings.min_size)
    mask = morphology.remove_small_holes(mask, area_threshold=settings.hole_area)
    distance = ndi.distance_transform_edt(mask)
    markers = measure.label(morphology.local_maxima(distance))
    labels = segmentation.watershed(-distance, markers, mask=mask)
    return segmentation.clear_border(labels)


def measure_objects(labels: np.ndarray, channel_a: np.ndarray, channel_b: np.ndarray) -> pd.DataFrame:
    props_a = measure.regionprops_table(
        labels,
        intensity_image=channel_a,
        properties=("label", "area", "mean_intensity", "major_axis_length", "minor_axis_length"),
    )
    props_b = measure.regionprops_table(labels, intensity_image=channel_b, properties=("label", "mean_intensity"))
    df = pd.DataFrame(props_a).rename(columns={"mean_intensity": "mean_a"})
    df["mean_b"] = props_b["mean_intensity"]
    df["ratio_a_over_b"] = df["mean_a"] / (df["mean_b"] + 1e-6)
    df["ellipticity"] = 1 - df["minor_axis_length"] / df["major_axis_length"]
    return df


def classify_populations(df: pd.DataFrame, rule: PopulationRule) -> pd.DataFrame:
    df = df.copy()
    if rule == PopulationRule.RATIO_ONE:
        threshold = 1.0
    elif rule == PopulationRule.MEDIAN_RATIO:
        threshold = df["ratio_a_over_b"].median()
    else:
        raise ValueError(f"Unknown rule: {rule}")
    df["population"] = np.where(df["ratio_a_over_b"] >= threshold, "A-high", "B-high")
    return df


class CellPipeline:
    def __init__(self, settings: SegmentationSettings):
        self.settings = settings

    def run(self, image_yxc: np.ndarray) -> tuple[np.ndarray, pd.DataFrame]:
        channel_a = image_yxc[..., 0]
        channel_b = image_yxc[..., 1]
        labels = segment_instances(channel_a, channel_b, self.settings)
        measurements = measure_objects(labels, channel_a, channel_b)
        measurements = classify_populations(measurements, self.settings.population_rule)
        return labels, measurements


# %%
image_yxc, _true_labels, _population_id = make_two_channel_cells(seed=5)
settings = SegmentationSettings(population_rule=PopulationRule.MEDIAN_RATIO)
pipeline = CellPipeline(settings)
labels, measurements = pipeline.run(image_yxc)

print(measurements.head())

plt.imshow(labels, cmap="nipy_spectral")
plt.axis("off")
plt.show()

# %% [markdown]
# ## Separation of concerns
#
# A later repository version could split this into:
#
# - `io.py`: loading images
# - `segmentation.py`: masks and labels
# - `measurements.py`: regionprops and tables
# - `visualization.py`: plotting
# - `cli.py`: command-line entry point

# %% [markdown]
# ## Optional exercises
#
# 1. Add a `threshold_scale` setting that multiplies the Otsu threshold.
# 2. Add a function that saves the measurement table to CSV.

# %%
# Answer sketch (optional, removable)
from pathlib import Path


def save_measurements(df: pd.DataFrame, path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


save_measurements(measurements, "scratch_outputs/module08_measurements.csv")
