from skimage import data


import numpy as np
import pandas as pd
from scipy import ndimage as ndi
from skimage import feature, filters, measure, morphology, segmentation
from pathlib import Path


def _measure_slice(membrane, nuclei):
    """Segment the nuclei of one slice and measure both channels."""
    # segment, as in module 5
    smoothed = filters.gaussian(nuclei, sigma=2, preserve_range=True)
    mask = smoothed > filters.threshold_otsu(smoothed)
    mask = morphology.remove_small_objects(mask, max_size=199)
    mask = ndi.binary_fill_holes(mask)

    # separate touching nuclei with a watershed
    distance = ndi.distance_transform_edt(mask)
    peaks = feature.peak_local_max(distance, min_distance=20, labels=mask)
    markers = np.zeros(mask.shape, dtype=int)
    markers[tuple(peaks.T)] = np.arange(1, len(peaks) + 1)
    labels = segmentation.watershed(-distance, markers, mask=mask)
    labels = morphology.remove_small_objects(labels, max_size=199)

    # measure both channels at once, by stacking them along the last axis
    table = pd.DataFrame(
        measure.regionprops_table(
            labels,
            intensity_image=np.stack([membrane, nuclei], axis=-1),
            properties=(
                "label",
                "area",
                "perimeter",
                "eccentricity",
                "axis_major_length",
                "axis_minor_length",
                "intensity_mean",
            ),
        )
    )
    table = table.rename(
        columns={
            "intensity_mean-0": "mean_intensity_membrane",
            "intensity_mean-1": "mean_intensity_nuclei",
        }
    )

    # objects touching the image border are truncated, flag them
    interior = np.unique(segmentation.clear_border(labels))
    table["on_border"] = ~table["label"].isin(interior)

    return table


def get_measurement_paths() -> list[Path]:

    image = data.cells3d()

    folder = Path("data") / "module_07"
    folder.mkdir(parents=True, exist_ok=True)

    z_slices = [24, 28, 32, 36, 40, 44]

    for index, z in enumerate(z_slices):
        table = _measure_slice(image[z, 0], image[z, 1])
        table.insert(0, "image_id", f"image_{index:02d}")
        table.to_csv(folder / f"image_{index:02d}.csv", index=False)

    return sorted(folder.glob("*.csv"))
