from pathlib import Path
from dataclasses import dataclass

import numpy as np
import pandas as pd


def intensity_ratio(channel_a, channel_b):
    """Return the channel-B/channel-A intensity ratio."""
    return np.asarray(channel_b) / np.asarray(channel_a)


def ellipticity_from_axes(axis_major, axis_minor):
    """Return standard ellipticity, ``1 - minor_axis / major_axis``."""
    return 1 - np.asarray(axis_minor) / np.asarray(axis_major)


def ellipticity_from_ratio(
    ratio,
    baseline: float = 0.18,
    amplitude: float = 0.34,
    exponent: float = 1.35,
):
    """Return the deterministic power-law ellipticity/ratio relationship."""
    return baseline + amplitude * np.asarray(ratio) ** exponent


def axes_from_area_ellipticity(area, ellipticity):
    """Return major and minor axes for an ellipse with area and ellipticity."""
    area = np.asarray(area)
    ellipticity = np.asarray(ellipticity)
    axis_major = np.sqrt(4 * area / (np.pi * (1 - ellipticity)))
    axis_minor = axis_major * (1 - ellipticity)
    return axis_major, axis_minor


def area_from_axes(axis_major, axis_minor):
    """Return ellipse area from its major and minor axis lengths."""
    return np.pi * np.asarray(axis_major) * np.asarray(axis_minor) / 4


@dataclass(frozen=True)
class PopulationProfile:
    """Parameters describing one synthetic cell population."""

    name: str
    population_probability: float = 0.0
    area_mean: float | None = None
    area_sd: float | None = None
    area_min: float | None = None
    area_max: float | None = None
    channel_a_mean: float | None = None
    channel_a_sd: float | None = None
    channel_a_min: float | None = None
    channel_a_max: float | None = None
    marker_noise_sd: float = 0.0
    ratio_baseline: float | None = None
    ratio_growth: float = 0.0
    ratio_time_exponent: float = 1.0
    ratio_sd: float | None = None
    ratio_min: float | None = None
    ratio_max: float | None = None
    ratio_floor_jitter: float = 0.0
    ellipticity_baseline: float | None = None
    ellipticity_sd: float | None = None
    ellipticity_amplitude: float = 0.0
    ellipticity_exponent: float = 1.0
    ellipticity_ceiling_jitter: float = 0.0
    artifact: bool = False


BRIGHT_PROFILE = PopulationProfile(
    name="bright",
    population_probability=0.5,
    area_mean=190,
    area_sd=28,
    area_min=30,
    channel_a_mean=1.0,
    channel_a_sd=0.20,
    channel_a_min=0.05,
    marker_noise_sd=0.0,
    ratio_baseline=0.35,
    ratio_growth=1.15,
    ratio_time_exponent=0.40,
    ratio_sd=0.28,
    ratio_min=0.05,
    ratio_floor_jitter=0.06,
    ellipticity_baseline=0.18,
    ellipticity_sd=0.035,
    ellipticity_amplitude=0.28,
    ellipticity_exponent=2.0,
    ellipticity_ceiling_jitter=0.05,
)

DIM_PROFILE = PopulationProfile(
    name="dim",
    area_mean=105,
    area_sd=18,
    area_min=30,
    channel_a_mean=1.0,
    channel_a_sd=0.12,
    channel_a_min=0.05,
    marker_noise_sd=0.01,
    ratio_baseline=0.48,
    ratio_sd=0.04,
    ratio_min=0.05,
    ellipticity_baseline=0.18,
    ellipticity_sd=0.07,
)

ARTIFACT_PROFILE = PopulationProfile(
    name="artifact",
    area_min=5,
    area_max=25,
    channel_a_min=0.1,
    channel_a_max=0.4,
    ratio_min=0.2,
    ratio_max=0.8,
    artifact=True,
)


def _fake_tabular(
    n_cells: int = 32,
    n_frames: int = 6,
    seed: int = 24,
) -> list[pd.DataFrame]:
    """Return mock measurements with two cell populations and artifacts.

    The bright population has an increasing channel-B/channel-A ratio with a
    gradually decreasing slope. Its standard ellipticity,
    ``1 - axis_minor_length / axis_major_length``,
    follows a noisy power law of that ratio. The dim population has a constant
    noisy ratio and an independent ellipticity distribution.
    """
    if n_cells < 1:
        raise ValueError("n_cells must be at least 1")
    if n_frames < 1:
        raise ValueError("n_frames must be at least 1")

    rng = np.random.default_rng(seed)
    rows = []
    label = 1

    for frame_index in range(n_frames):
        progress = frame_index / max(n_frames - 1, 1)
        growth = progress**BRIGHT_PROFILE.ratio_time_exponent
        frame_size = max(1, int(round(rng.normal(n_cells, np.sqrt(n_cells)))))
        n_artifacts = max(1, int(round(0.08 * frame_size)))
        n_real_cells = max(1, frame_size - n_artifacts)

        for _ in range(n_real_cells):
            profile = (
                BRIGHT_PROFILE
                if rng.random() < BRIGHT_PROFILE.population_probability
                else DIM_PROFILE
            )
            channel_a = max(
                profile.channel_a_min,
                rng.normal(profile.channel_a_mean, profile.channel_a_sd),
            )
            raw_ratio = (
                profile.ratio_baseline
                + profile.ratio_growth * growth
                + rng.normal(0, profile.ratio_sd)
            )
            if raw_ratio < profile.ratio_min:
                ratio = profile.ratio_min + rng.uniform(0, profile.ratio_floor_jitter)
            else:
                ratio = raw_ratio
            target_area = max(
                profile.area_min,
                rng.normal(profile.area_mean, profile.area_sd),
            )
            if profile is BRIGHT_PROFILE:
                ellipticity = ellipticity_from_ratio(
                    ratio,
                    baseline=profile.ellipticity_baseline,
                    amplitude=profile.ellipticity_amplitude,
                    exponent=profile.ellipticity_exponent,
                ) + rng.normal(0, profile.ellipticity_sd)
            else:
                ellipticity = rng.normal(
                    profile.ellipticity_baseline,
                    profile.ellipticity_sd,
                )

            marker_intensity = channel_a * ratio + rng.normal(
                0, profile.marker_noise_sd
            )
            marker_intensity = max(0.01, marker_intensity)

            ellipticity = max(0.02, ellipticity)
            ellipticity_ceiling = np.nextafter(1.0, 0.0)
            if ellipticity > ellipticity_ceiling:
                ellipticity = ellipticity_ceiling - rng.uniform(
                    0, profile.ellipticity_ceiling_jitter
                )
            axis_major, axis_minor = axes_from_area_ellipticity(
                target_area, ellipticity
            )
            on_border = bool(rng.random() < 0.15)
            if on_border:
                axis_major = rng.uniform(5, 45)
                axis_minor = rng.uniform(5, 45)
            area = area_from_axes(axis_major, axis_minor)

            rows.append(
                {
                    "frame_id": f"frame_{frame_index:02d}",
                    "label": label,
                    "area": area,
                    "perimeter": np.pi * np.sqrt((axis_major**2 + axis_minor**2) / 2),
                    "eccentricity": np.sqrt(max(0, 1 - (axis_minor / axis_major) ** 2)),
                    "axis_major_length": axis_major,
                    "axis_minor_length": axis_minor,
                    "nuclear_intensity": channel_a,
                    "marker_intensity": marker_intensity,
                    "on_border": on_border,
                    "population": profile.name,
                }
            )
            label += 1

        for k in range(n_artifacts):
            profile = ARTIFACT_PROFILE
            target_area = rng.uniform(profile.area_min, profile.area_max)
            axis_length = np.sqrt(4 * target_area / np.pi)
            axis_major = axis_length
            axis_minor = axis_length
            area = area_from_axes(axis_major, axis_minor)
            channel_a = rng.uniform(profile.channel_a_min, profile.channel_a_max)

            rows.append(
                {
                    "frame_id": f"frame_{frame_index:02d}",
                    "label": label,
                    "area": area,
                    "perimeter": np.pi * np.sqrt((axis_major**2 + axis_minor**2) / 2),
                    "eccentricity": np.sqrt(max(0, 1 - (axis_minor / axis_major) ** 2)),
                    "axis_major_length": axis_major,
                    "axis_minor_length": axis_minor,
                    "nuclear_intensity": channel_a,
                    "marker_intensity": channel_a
                    * rng.uniform(profile.ratio_min, profile.ratio_max),
                    "on_border": bool(rng.random() < 0.15),
                    "population": profile.name,
                }
            )
            label += 1

    table = pd.DataFrame(rows)
    return [
        frame.reset_index(drop=True)
        for _, frame in table.groupby("frame_id", sort=False)
    ]


def get_measurements() -> Path:
    folder = Path("scratch_outputs/module_07")
    folder.mkdir(parents=True, exist_ok=True)

    n_frames = 6

    tables = _fake_tabular(n_frames=n_frames)
    for i, subtable in enumerate(tables):
        subtable.to_csv(folder / f"frame_{i:02d}.csv", index=False)

    return folder
