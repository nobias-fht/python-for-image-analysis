# %% [markdown]
# # Module 8: modular Python
#
# Time: 2 hours 30 minutes.
#
# Essential ideas: a notebook prototype becomes reusable when separate concerns
# are given names. Functions name actions, dataclasses bundle settings, enums
# avoid magic strings, type hints document expectations, validation fails early,
# logging records what happened, and small classes can coordinate state when
# that helps.

# %%
import logging
from dataclasses import asdict, dataclass, replace
from enum import Enum
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import ndimage as ndi
from skimage import filters, measure, morphology, segmentation

from src.python_for_ia import make_two_channel_cells

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger("module_08")

# %% [markdown]
# ## Concepts worth carrying from notebooks into software
#
# In scientific Python, "software engineering" does not mean making everything
# abstract. It means making the analysis easier to understand, rerun, test, and
# change without breaking hidden assumptions.
#
# Useful concepts in this module:
#
# - **Pure functions**: same input gives same output, with no hidden file writes.
#   They are easy to test.
# - **Side effects at the boundary**: saving files, printing, plotting, and
#   logging should be explicit.
# - **Type hints**: lightweight documentation for humans and tools.
# - **Docstrings**: short explanations of purpose, parameters, and returned
#   values.
# - **Validation**: fail early when images, settings, or tables are invalid.
# - **Configuration objects**: keep parameters together instead of scattering
#   numbers across cells.
# - **Small tests**: executable assumptions that protect you while refactoring.

# %% [markdown]
# ## From notebook cells to functions
#
# A good function usually:
#
# - has one main responsibility,
# - has a name that says what it does,
# - receives inputs explicitly,
# - returns outputs rather than relying on global variables.
#
# Utility: functions let students rerun the same analysis on a new image without
# copying five notebook cells and accidentally changing one of them.
#
# Pitfall: turning every line into a tiny function can make code harder to read.
# Refactor around concepts that you expect to reuse or test.

# %%


class PopulationRule(Enum):
    """Available rules for assigning objects to two populations."""

    RATIO_ONE = "ratio_one"
    MEDIAN_RATIO = "median_ratio"


@dataclass(frozen=True)
class SegmentationSettings:
    """Parameters that control the segmentation and classification workflow."""

    min_size: int = 80
    hole_area: int = 80
    threshold_scale: float = 1.0
    population_rule: PopulationRule = PopulationRule.RATIO_ONE

    def __post_init__(self) -> None:
        if self.min_size <= 0:
            raise ValueError("min_size must be positive.")
        if self.hole_area < 0:
            raise ValueError("hole_area cannot be negative.")
        if self.threshold_scale <= 0:
            raise ValueError("threshold_scale must be positive.")


@dataclass
class PipelineResult:
    """Outputs from one pipeline run."""

    labels: np.ndarray
    measurements: pd.DataFrame
    threshold: float


def split_channels(image_yxc: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return channel A and channel B from a YXC image."""
    if image_yxc.ndim != 3 or image_yxc.shape[-1] != 2:
        raise ValueError("Expected image with shape Y, X, C and two channels.")
    return image_yxc[..., 0], image_yxc[..., 1]


def validate_same_shape(*arrays: np.ndarray) -> None:
    """Raise an error if input arrays do not share the same shape."""
    shapes = {array.shape for array in arrays}
    if len(shapes) != 1:
        raise ValueError(f"Expected matching shapes, got {sorted(shapes)}")


def make_foreground_mask(
    channel_a: np.ndarray, channel_b: np.ndarray, settings: SegmentationSettings
) -> tuple[np.ndarray, float]:
    """Create a binary foreground mask from two channels."""
    validate_same_shape(channel_a, channel_b)
    combined = channel_a + channel_b
    threshold = filters.threshold_otsu(combined) * settings.threshold_scale
    mask = combined > threshold
    mask = morphology.remove_small_objects(mask, min_size=settings.min_size)
    mask = morphology.remove_small_holes(mask, area_threshold=settings.hole_area)
    mask = ndi.binary_fill_holes(mask)
    return mask, threshold


def segment_instances(
    channel_a: np.ndarray, channel_b: np.ndarray, settings: SegmentationSettings
) -> tuple[np.ndarray, float]:
    """Segment foreground objects into instance labels."""
    mask, threshold = make_foreground_mask(channel_a, channel_b, settings)
    distance = ndi.distance_transform_edt(mask)
    markers = measure.label(morphology.local_maxima(distance))
    labels = segmentation.watershed(-distance, markers, mask=mask)
    return segmentation.clear_border(labels), threshold


def measure_objects(
    labels: np.ndarray, channel_a: np.ndarray, channel_b: np.ndarray
) -> pd.DataFrame:
    """Measure per-object intensity and shape features."""
    validate_same_shape(labels, channel_a, channel_b)
    props_a = measure.regionprops_table(
        labels,
        intensity_image=channel_a,
        properties=(
            "label",
            "area",
            "mean_intensity",
            "major_axis_length",
            "minor_axis_length",
        ),
    )
    props_b = measure.regionprops_table(
        labels, intensity_image=channel_b, properties=("label", "mean_intensity")
    )
    df = pd.DataFrame(props_a).rename(columns={"mean_intensity": "mean_a"})
    df["mean_b"] = props_b["mean_intensity"]
    df["ratio_a_over_b"] = df["mean_a"] / (df["mean_b"] + 1e-6)
    df["ellipticity"] = 1 - df["minor_axis_length"] / df["major_axis_length"]
    return df


def classify_populations(df: pd.DataFrame, rule: PopulationRule) -> pd.DataFrame:
    """Return a copy of the table with a population column."""
    required = {"ratio_a_over_b"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = df.copy()
    if rule == PopulationRule.RATIO_ONE:
        threshold = 1.0
    elif rule == PopulationRule.MEDIAN_RATIO:
        threshold = df["ratio_a_over_b"].median()
    else:
        raise ValueError(f"Unknown rule: {rule}")
    df["population"] = np.where(df["ratio_a_over_b"] >= threshold, "A-high", "B-high")
    return df


def save_measurements(df: pd.DataFrame, path: str | Path) -> None:
    """Save a measurement table to CSV.

    This function has a side effect: it writes a file. Keeping that side effect
    in one small function makes the rest of the pipeline easier to test.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


# %% [markdown]
# ## Type hints, docstrings, and validation
#
# Type hints do not make Python run faster, and they are not a substitute for
# tests. Their utility is communication: they tell readers and editors what
# kind of object a function expects.
#
# Docstrings answer "why does this function exist?" Validation catches mistakes
# near their source. A clear `ValueError` is much more useful than a mysterious
# error five functions later.

# %%
print("split_channels annotations:")
print(split_channels.__annotations__)
print("split_channels docstring:")
print(split_channels.__doc__)

try:
    split_channels(np.zeros((32, 32)))
except ValueError as error:
    print("clear validation error:", error)


# %% [markdown]
# ## Configuration objects and immutable settings
#
# A dataclass is a compact way to keep parameters together.
#
# Utility:
#
# - one object can be passed through the pipeline,
# - parameters can be saved with results,
# - defaults are visible in one place,
# - validation can live next to the settings.
#
# Here `SegmentationSettings` is frozen, meaning it cannot be modified after
# creation. For parameter sweeps, use `dataclasses.replace` to create a changed
# copy instead of mutating the original.

# %%
default_settings = SegmentationSettings()
relaxed_settings = replace(default_settings, min_size=40, threshold_scale=0.9)

print("default settings:", asdict(default_settings))
print("relaxed settings:", asdict(relaxed_settings))

try:
    SegmentationSettings(min_size=-1)
except ValueError as error:
    print("invalid settings caught early:", error)


# %% [markdown]
# ## A small pipeline class
#
# A class is useful here because settings are shared across multiple steps. If
# there is no shared state, plain functions are often simpler.
#
# Utility: this class gives us a single object representing "the pipeline with
# these settings". It remains small because the real work still happens in
# testable functions.

# %%


class CellPipeline:
    def __init__(self, settings: SegmentationSettings):
        self.settings = settings

    def run(self, image_yxc: np.ndarray) -> PipelineResult:
        logger.info("running pipeline with settings: %s", asdict(self.settings))
        channel_a, channel_b = split_channels(image_yxc)
        labels, threshold = segment_instances(channel_a, channel_b, self.settings)
        measurements = measure_objects(labels, channel_a, channel_b)
        measurements = classify_populations(measurements, self.settings.population_rule)
        return PipelineResult(
            labels=labels, measurements=measurements, threshold=threshold
        )


# %%
image_yxc, _true_labels, _population_id = make_two_channel_cells(seed=5)
settings = SegmentationSettings(
    population_rule=PopulationRule.MEDIAN_RATIO, threshold_scale=1.0
)
pipeline = CellPipeline(settings)
result = pipeline.run(image_yxc)

print("threshold:", result.threshold)
print(result.measurements.head())

plt.imshow(result.labels, cmap="nipy_spectral")
plt.axis("off")
plt.show()

# %% [markdown]
# ## Parameter sweeps without copy-paste
#
# A common notebook smell is copy-pasting the same analysis cell with one number
# changed. A small loop over settings is usually safer and easier to summarize.
#
# When to use: checking sensitivity to thresholds, object-size filters, or other
# parameters before deciding which settings are robust enough for a dataset.

# %%


def run_parameter_sweep(
    image_yxc: np.ndarray, settings_list: list[SegmentationSettings]
) -> pd.DataFrame:
    """Run the pipeline for several settings and return one summary row each."""
    rows = []
    for settings in settings_list:
        sweep_result = CellPipeline(settings).run(image_yxc)
        rows.append(
            {
                "min_size": settings.min_size,
                "threshold_scale": settings.threshold_scale,
                "population_rule": settings.population_rule.value,
                "threshold": sweep_result.threshold,
                "n_objects": int(sweep_result.labels.max()),
                "mean_ratio": sweep_result.measurements["ratio_a_over_b"].mean(),
            }
        )
    return pd.DataFrame(rows)


sweep_settings = [
    replace(default_settings, threshold_scale=scale, min_size=min_size)
    for scale in [0.8, 1.0, 1.2]
    for min_size in [40, 80]
]
sweep_table = run_parameter_sweep(image_yxc, sweep_settings)
print(sweep_table)

# %% [markdown]
# ## Lightweight checks
#
# These are not a full test suite, but they show the habit of checking
# assumptions near the code.
#
# Utility: checks protect the behavior while you refactor. Later these can move
# into `tests/test_pipeline.py` and run automatically with `pytest`.

# %%
assert result.labels.shape == image_yxc.shape[:2]
assert {"label", "area", "ratio_a_over_b", "ellipticity", "population"}.issubset(
    result.measurements.columns
)
assert result.measurements["area"].min() > 0
print("basic checks passed")

# %% [markdown]
# ## Test-shaped functions
#
# A test is just a small function that makes an expectation executable. In a
# real project, these functions would live in a `tests/` directory and use
# `pytest`.
#
# Start with tests for mistakes you are likely to make: wrong channel order,
# missing columns, empty masks, or parameter changes that silently alter output
# shape.

# %%


def test_split_channels_rejects_wrong_shape() -> None:
    try:
        split_channels(np.zeros((32, 32, 3)))
    except ValueError:
        return
    raise AssertionError("split_channels should reject images with three channels.")


def test_pipeline_result_has_expected_columns() -> None:
    expected = {
        "label",
        "area",
        "mean_a",
        "mean_b",
        "ratio_a_over_b",
        "ellipticity",
        "population",
    }
    missing = expected - set(result.measurements.columns)
    assert not missing, f"missing columns: {missing}"


test_split_channels_rejects_wrong_shape()
test_pipeline_result_has_expected_columns()
print("test-shaped checks passed")

# %% [markdown]
# ## Logging instead of scattered print calls
#
# `print` is fine in a notebook. Logging is better in scripts and HPC jobs
# because messages can include severity levels, module names, and timestamps.
#
# Utility:
#
# - `INFO`: normal progress messages,
# - `WARNING`: unexpected but recoverable situations,
# - `ERROR`: failures that need attention.
#
# Pitfall: logging every pixel-level step creates noise. Log run-level events,
# parameters, file paths, and summary counts.

# %%
logger.info("finished one run with %s objects", result.labels.max())
if result.labels.max() == 0:
    logger.warning("no objects were detected")

# %% [markdown]
# ## Separation of concerns
#
# A later repository version could split this into:
#
# - `io.py`: loading images and validating axis order,
# - `segmentation.py`: masks and labels,
# - `measurements.py`: regionprops and tables,
# - `visualization.py`: plotting and QC overlays,
# - `settings.py`: dataclasses and enums,
# - `cli.py`: command-line entry point.
#
# When to split files: when one file becomes hard to navigate or when different
# concepts change for different reasons. Do not split just to look professional.
#
# Related concepts:
#
# - **Cohesion**: keep code that changes together in the same module.
# - **Coupling**: reduce unnecessary dependence between modules.
# - **Public API**: decide which functions students/users should call directly.
# - **Private helpers**: prefix with `_` when a helper is internal to a module.
# - **Reproducibility**: keep settings, code version, inputs, and outputs linked.

# %% [markdown]
# ## Common Python pitfalls in scientific code
#
# - Mutable default arguments: avoid `def f(items=[])`; use `None` or a
#   dataclass `default_factory`.
# - Hidden globals: a function that silently reads a variable from an earlier
#   notebook cell is hard to reuse.
# - In-place mutation: changing a dataframe or array inside a function can
#   surprise callers. Return a copy unless mutation is intentional.
# - Broad `except:` blocks: catching every error can hide real bugs.
# - Hard-coded paths: prefer `Path` objects and pass paths as parameters.
# - Mixed units: make units explicit in names or metadata.

# %% [markdown]
# ## Optional exercises
#
# 1. Add a `max_area` setting and filter objects larger than that value.
# 2. Add a `summarize_measurements` function returning counts per population.
# 3. Save measurements to CSV using `save_measurements`.
# 4. Write one assertion that catches an image with the wrong number of channels.
# 5. Change `threshold_scale` and compare the number of labels.
# 6. Add a test-shaped function for `classify_populations`.
# 7. Add one logging message to `save_measurements`.

# %%
# Answer sketch (optional, removable)


def summarize_measurements(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("population")
        .agg(n_objects=("label", "count"), mean_ratio=("ratio_a_over_b", "mean"))
        .reset_index()
    )


print(summarize_measurements(result.measurements))
save_measurements(result.measurements, "scratch_outputs/module08_measurements.csv")

try:
    split_channels(np.zeros((32, 32, 3)))
except ValueError as error:
    print("caught expected error:", error)

for scale in [0.8, 1.0, 1.2]:
    scaled_result = CellPipeline(SegmentationSettings(threshold_scale=scale)).run(
        image_yxc
    )
    print(scale, scaled_result.labels.max())


def test_classify_populations_adds_expected_values() -> None:
    tiny = pd.DataFrame({"ratio_a_over_b": [0.5, 2.0]})
    classified = classify_populations(tiny, PopulationRule.RATIO_ONE)
    assert classified["population"].tolist() == ["B-high", "A-high"]


test_classify_populations_adds_expected_values()
logger.info("saved measurements exercise output")
