"""Synthetic image helpers used by multiple draft modules."""

import numpy as np
from skimage import data, filters


def images_with_problematic_hist() -> list[tuple[str, np.ndarray]]:
    """Process images so that their histograms have issues.

    Used in module 05.
    """
    img = data.cells3d()[30, 1]

    # normalize to [0, 1] for controlled manipulations
    img01 = (img - img.min()) / (img.max() - img.min())

    # simulate coarse quantization, like reducing many intensity levels
    img_holes = np.round(img01 * 31) / 31  # only 32 gray levels

    # clip bright values so many pixels pile up at the maximum
    img_sat = np.clip(img01 * 2.5, 0, 1)

    return [("Original", img), ("Example 1", img_holes), ("Example 2", img_sat)]


def image_with_background(noise_level: int = 1_000) -> np.ndarray:
    """Add noise and background to a cells3d slice.

    Used in module 05.
    """
    rng = np.random.default_rng()

    img = data.cells3d()
    img_slice = img[30, 1]

    # generate background as a single gaussian
    yy, xx = np.indices(img_slice.shape)
    bg = np.zeros_like(img_slice)
    cy = 0.4 * img_slice.shape[0]
    cx = 0.7 * img_slice.shape[1]
    sigma = 80

    bg = np.exp(-((yy - cy) ** 2 + (xx - cx) ** 2) / (2 * sigma**2))
    bg = img_slice.mean() * bg  # controls background strength

    # # generate background by averaging, smoothing and scaling
    # bg = np.sum(img[:15, 1], axis=0)
    # bg = filters.gaussian(bg, sigma=10)
    # bg = 10 * bg * img_slice.mean() / bg.mean()

    # use Poisson distributed noise
    noisy = img_slice + rng.normal(0, noise_level, img_slice.shape)

    # generate final image with same mean as the original
    tot_float = noisy + bg
    tot_float_norm = img_slice.mean() * tot_float / tot_float.mean()

    return np.floor(tot_float_norm)
