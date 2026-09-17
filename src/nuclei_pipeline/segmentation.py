"""Turn a raw channel into a label image."""

import numpy as np
from numpy.typing import NDArray
from scipy import ndimage as ndi
from skimage import feature, filters, morphology, segmentation

from .settings import Settings


def remove_background(channel: NDArray, settings: Settings) -> NDArray:
    """Remove an uneven background with a white top-hat filter."""
    footprint = morphology.disk(settings.tophat_radius)
    return morphology.white_tophat(channel, footprint=footprint)


def make_mask(channel: NDArray, settings: Settings) -> NDArray:
    """Blur the channel, threshold it with Otsu, and return a boolean mask."""
    smoothed = filters.gaussian(channel, sigma=settings.gaussian_sigma)
    threshold = filters.threshold_otsu(smoothed)
    return smoothed > threshold


def clean_mask(mask: NDArray, settings: Settings) -> NDArray:
    """Drop small objects, close small holes, and smooth the outlines."""
    mask = morphology.remove_small_objects(mask, max_size=settings.min_object_size)
    mask = morphology.remove_small_holes(
        mask, max_size=settings.min_hole_size, connectivity=2
    )
    footprint = morphology.disk(settings.opening_radius)
    return morphology.opening(mask, footprint=footprint)


def separate_objects(mask: NDArray, settings: Settings) -> NDArray:
    """Split touching objects with a watershed, and return a label image."""
    distance = ndi.distance_transform_edt(mask)
    footprint = np.ones((settings.peak_footprint, settings.peak_footprint))
    coords = feature.peak_local_max(
        distance,
        min_distance=settings.peak_distance,
        footprint=footprint,
        labels=mask,
    )
    seeds = np.zeros(mask.shape, dtype=bool)
    seeds[tuple(coords.T)] = True
    markers, _ = ndi.label(seeds)
    return segmentation.watershed(-distance, markers, mask=mask)
