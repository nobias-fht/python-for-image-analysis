"""Compare the pipeline output across settings."""

from dataclasses import replace
from pathlib import Path

import pandas as pd

from .pipeline import Pipeline
from .settings import Settings


def sweep_one_parameter(settings: Settings, name: str, values: list) -> list[Settings]:
    """Return a list of settings that differ by one parameter only."""
    if not hasattr(settings, name):
        raise ValueError(f"Settings has no parameter named {name}.")
    return [replace(settings, **{name: value}) for value in values]


def run_sweep(folder: str | Path, settings_list: list[Settings]) -> pd.DataFrame:
    """Run the pipeline once per setting. Return one summary row each."""
    rows = []
    for settings in settings_list:
        table = Pipeline(settings).run_folder(folder)
        rows.append(
            {
                "gaussian_sigma": settings.gaussian_sigma,
                "min_object_size": settings.min_object_size,
                "n_objects": len(table),
                "mean_intensity_sum": table["intensity_sum"].mean(),
            }
        )
    return pd.DataFrame(rows)
