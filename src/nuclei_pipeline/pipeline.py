"""Run the analysis steps in order."""

from pathlib import Path

import pandas as pd
from numpy.typing import NDArray

from .io import load_images
from .measurements import measure_objects
from .segmentation import clean_mask, make_mask, remove_background, separate_objects
from .settings import Settings


class Pipeline:
    """The analysis pipeline, bound to one set of settings."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def run_image(self, image: NDArray) -> tuple[NDArray, pd.DataFrame]:
        """Return a 2D label image and one measurement row per nucleus."""
        if image.ndim != 3:
            raise ValueError(
                f"Expected an image of shape (channel, y, x), got {image.shape}."
            )
        nuclei = image[self.settings.nucleus_channel]
        target = image[self.settings.target_channel]
        corrected = remove_background(nuclei, self.settings)
        mask = make_mask(corrected, self.settings)
        mask = clean_mask(mask, self.settings)
        labels = separate_objects(mask, self.settings)
        return labels, measure_objects(labels, target)

    def run_folder(self, folder: str | Path) -> pd.DataFrame:
        """Measure every image of a folder. Return one table, with an image column."""
        paths, images = load_images(folder)
        tables = []
        for path, image in zip(paths, images):
            _, table = self.run_image(image)
            table.insert(0, "image", path.stem)
            tables.append(table)
        return pd.concat(tables, ignore_index=True)
