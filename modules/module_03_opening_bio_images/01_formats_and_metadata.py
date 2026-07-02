# %% [markdown]
# # Module 3: opening bio-image formats
#
# Essential ideas: file format is not just pixels. Metadata describes axes,
# physical pixel size, channels, time points, and acquisition settings.

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from skimage import io, util

from course_utils import make_blobs

# %% [markdown]
# ## Format landscape
#
# - OME-TIFF: common, open, stores pixels plus OME metadata.
# - OME-NGFF / OME-Zarr: cloud/HPC-friendly chunked arrays plus metadata.
# - Vendor formats: `.lif`, `.nd2`, `.czi`, `.lsm`; often need specialized readers.
# - JPEG/PNG: useful for figures, usually poor archival formats for quantitative data.
#
# For real files, start by asking: axis order, dtype, pixel size, channels,
# compression, and whether metadata survived export.

# %% [markdown]
# ## Simulate saving and opening an image

# %%
output_dir = Path("scratch_outputs")
output_dir.mkdir(exist_ok=True)

image = make_blobs(seed=8)
uint16_image = util.img_as_uint(image)
tif_path = output_dir / "synthetic_cells.tif"
io.imsave(tif_path, uint16_image)

loaded = io.imread(tif_path)
print("loaded:", loaded.shape, loaded.dtype, loaded.min(), loaded.max())

# %% [markdown]
# ## JPEG compression is visually convenient, not measurement-safe

# %%
jpg_path = output_dir / "synthetic_cells.jpg"
io.imsave(jpg_path, util.img_as_ubyte(image), quality=25)
jpeg_loaded = io.imread(jpg_path)

difference = loaded.astype(float) / loaded.max() - jpeg_loaded.astype(float) / 255
print("mean absolute JPEG difference:", np.abs(difference).mean())

fig, axes = plt.subplots(1, 3, figsize=(9, 3))
axes[0].imshow(loaded, cmap="gray")
axes[0].set_title("TIFF")
axes[1].imshow(jpeg_loaded, cmap="gray")
axes[1].set_title("JPEG")
axes[2].imshow(difference, cmap="coolwarm")
axes[2].set_title("difference")
for ax in axes:
    ax.axis("off")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## High-level reader examples
#
# These are examples to discuss, not required for this draft:
#
# ```python
# import tifffile
# image = tifffile.imread("experiment.ome.tif")
#
# import zarr
# root = zarr.open("plate.zarr", mode="r")
#
# from bioio import BioImage
# img = BioImage("experiment.czi")
# data = img.get_image_data("CZYX")
# ```

# %% [markdown]
# ## Optional exercises
#
# 1. Save the synthetic image as PNG and compare its dtype after loading.
# 2. List three metadata fields you would want before measuring cell size.

# %%
# Answer sketch (optional, removable)
png_path = output_dir / "synthetic_cells.png"
io.imsave(png_path, util.img_as_ubyte(image))
png_loaded = io.imread(png_path)
print(png_loaded.shape, png_loaded.dtype)
print(["pixel size", "axis order", "channel names"])
