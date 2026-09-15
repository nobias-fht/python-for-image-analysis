"""Synthetic image helpers used by multiple draft modules."""

import numpy as np
from skimage import data


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


def image_with_background(noise_level: int = 1_000, bg_level=1) -> np.ndarray:
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
    bg = img_slice.mean() * bg_level * bg  # controls background strength

    # use Poisson distributed noise
    noisy = img_slice + rng.normal(0, noise_level, img_slice.shape)

    # generate final image with same mean as the original
    tot_float = noisy + bg
    tot_float_norm = img_slice.mean() * tot_float / tot_float.mean()

    return np.floor(tot_float_norm)


def images_with_various_degradations() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng()

    img = data.cells3d()
    img_slice = img[30, 1]

    # offset
    offset = 5_000
    img_offset = img_slice + offset

    # background
    img_bg = image_with_background(bg_level=1.5)

    # uneven illumination
    w, h = img_slice.shape
    x = np.linspace(-1, 1, w)
    y = np.linspace(-1, 1, h)
    xx, yy = np.meshgrid(x, y)

    # simulated light gradient
    illumination = 1.0 - 0.5 * (xx + yy) / 1.0
    # illumination = np.clip(illumination, 0.1, 1.0)
    img_uneven = np.floor(img_slice * illumination)

    # all
    img_all = np.floor(img_bg * illumination) + offset

    return img_slice, img_offset, img_bg, img_uneven, img_all
