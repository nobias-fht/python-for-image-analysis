"""Synthetic image generators used by multiple draft modules."""

from __future__ import annotations

import numpy as np
from skimage import draw, filters, measure, segmentation, util


def make_blobs(
    shape: tuple[int, int] = (160, 160),
    n_blobs: int = 24,
    radius_range: tuple[int, int] = (5, 12),
    seed: int = 0,
) -> np.ndarray:
    """Return a simple noisy fluorescence-like image with bright blobs."""
    rng = np.random.default_rng(seed)
    image = rng.normal(loc=0.08, scale=0.03, size=shape)

    for _ in range(n_blobs):
        radius = int(rng.integers(radius_range[0], radius_range[1] + 1))
        row = int(rng.integers(radius, shape[0] - radius))
        col = int(rng.integers(radius, shape[1] - radius))
        rr, cc = draw.disk((row, col), radius=radius, shape=shape)
        image[rr, cc] += rng.uniform(0.4, 1.0)

    image = filters.gaussian(image, sigma=1.2)
    image = util.random_noise(image, mode="poisson", rng=seed)
    return image.astype(np.float32)


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

