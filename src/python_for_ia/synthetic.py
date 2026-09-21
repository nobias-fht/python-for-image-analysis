"""Synthetic image helpers used by multiple draft modules."""

from pathlib import Path
import numpy as np
from skimage import data, draw, filters, measure, segmentation


def project_data() -> list[Path]:
    return list(Path("../data/practical_project/noisy").glob("*.tif"))


def images_with_problematic_hist() -> list[np.ndarray]:
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

    return [img, img_holes, img_sat]


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


def make_two_channel_cells(
    shape: tuple[int, int] = (192, 192),
    n_cells: int = 32,
    seed: int = 2,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (image_yxc, instance_labels, population_id) for a toy assay."""
    rng = np.random.default_rng(seed)
    labels = np.zeros(shape, dtype=np.uint16)
    population_by_label = np.zeros(n_cells + 1, dtype=np.uint8)

    for label in range(1, n_cells + 1):
        row = int(rng.integers(18, shape[0] - 18))
        col = int(rng.integers(18, shape[1] - 18))
        radius_r = int(rng.integers(7, 15))
        radius_c = int(rng.integers(5, 13))
        rr, cc = draw.ellipse(row, col, radius_r, radius_c, shape=shape)
        labels[rr, cc] = label
        population_by_label[label] = int(rng.integers(0, 2))

    channel_a = rng.normal(0.04, 0.015, size=shape)
    channel_b = rng.normal(0.04, 0.015, size=shape)

    for props in measure.regionprops(labels):
        label = props.label
        mask = labels == label
        if population_by_label[label] == 0:
            channel_a[mask] += rng.uniform(0.55, 0.85)
            channel_b[mask] += rng.uniform(0.15, 0.35)
        else:
            channel_a[mask] += rng.uniform(0.15, 0.35)
            channel_b[mask] += rng.uniform(0.55, 0.85)

    channel_a = filters.gaussian(channel_a, sigma=1.1)
    channel_b = filters.gaussian(channel_b, sigma=1.1)
    image = np.stack([channel_a, channel_b], axis=-1)
    image = np.clip(image, 0, 1).astype(np.float32)

    cleaned = segmentation.clear_border(labels)
    return image, cleaned, population_by_label
