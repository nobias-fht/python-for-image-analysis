"""Read images from disk and write tables to disk."""

from pathlib import Path

import pandas as pd
from numpy.typing import NDArray
from tifffile import imread


def load_images(folder: str | Path) -> tuple[list[Path], list[NDArray]]:
    """Return the TIFF paths of a folder, sorted by name, and their images."""
    paths = sorted(Path(folder).glob("*.tif"))
    if not paths:
        raise FileNotFoundError(f"No TIFF file in {folder}")
    images = [imread(path) for path in paths]
    return paths, images


def save_table(table: pd.DataFrame, path: str | Path) -> None:
    """Write a table to a CSV file, and create the parent folder if needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(path, index=False)
