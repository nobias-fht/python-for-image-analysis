"""Synthetic image helpers used by multiple draft modules."""

from __future__ import annotations

import numpy as np
from scipy.ndimage import gaussian_filter
from skimage import data, filters


def images_with_problematic_hist() -> list[tuple[str, np.ndarray]]:
    """Process images so that their histograms have issues."""
    img = data.cells3d()[30, 1]

    # normalize to [0, 1] for controlled manipulations
    img01 = (img - img.min()) / (img.max() - img.min())

    # simulate coarse quantization, like reducing many intensity levels
    img_holes = np.round(img01 * 31) / 31  # only 32 gray levels

    # clip bright values so many pixels pile up at the maximum
    img_sat = np.clip(img01 * 2.5, 0, 1)

    return [("Original", img), ("Example 1", img_holes), ("Example 2", img_sat)]


def image_with_background(noise_level: int = 1_000) -> np.ndarray:
    """Add noise and background to a cells3d slice."""
    rng = np.random.default_rng()

    img = data.cells3d()
    img_slice = img[30, 1]

    # generate background by averaging, smoothing and scaling
    bg = np.sum(img[:15, 1], axis=0)
    bg = filters.gaussian(bg, sigma=10)
    bg = 10 * bg * img_slice.mean() / bg.mean()

    # use Poisson distributed noise
    noisy = noise_level * rng.poisson(img_slice / noise_level)

    # generate final image with same mean as the original
    tot_float = noisy + bg
    tot_float_norm = img_slice.mean() * tot_float / tot_float.mean()

    return np.floor(tot_float_norm)
