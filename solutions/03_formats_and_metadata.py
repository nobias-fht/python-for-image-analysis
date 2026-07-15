# %% [markdown]
# # Module 3: opening bio-image formats
#
# Time: 1 hour.
#
# Essential ideas: file format is not just pixels. Metadata describes axes,
# physical pixel size, channels, time points, scenes, acquisition settings, and
# sometimes the difference between a usable quantitative dataset and a pretty
# picture.

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
# - OME-NGFF / OME-Zarr: chunked, multiscale, cloud/HPC-friendly image stores.
# - Vendor formats: `.lif`, `.nd2`, `.czi`, `.lsm`; often need specialized
#   readers and may contain multiple scenes/series.
# - JPEG/PNG: useful for figures, usually poor archival formats for
#   quantitative microscopy data.
#
# When to use:
#
# - Use vendor files when you need original acquisition metadata.
# - Convert to OME-TIFF or OME-Zarr when building a reproducible analysis
#   workflow that should outlive one microscope vendor.
# - Use JPEG/PNG only for presentation or quick visual checks unless the data
#   are explicitly non-quantitative.

# %% [markdown]
# ## Metadata checklist
#
# Before measuring anything, ask:
#
# - What is the axis order?
# - What is the dtype and bit depth?
# - What are the channel names and wavelengths?
# - What is the physical pixel size in x, y, and z?
# - Are there multiple scenes, positions, time points, or pyramid levels?
# - Was compression used? If yes, was it lossless?
# - Did the export preserve metadata or only pixel values?

# %% [markdown]
# ## Simulate saving and opening an image
#
# This example writes a toy TIFF so every student can run the cell. Real
# microscopy data should usually be read with format-aware tools that preserve
# metadata, but the basic principle is the same: read, inspect, and only then
# analyze.

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
#
# Lossy compression changes pixel values. That may be acceptable for a figure,
# but it is usually not acceptable for intensity measurement, segmentation, or
# reproducibility.

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
# ## Reader examples for real microscopy formats
#
# The course does not ship real `.lif`, `.nd2`, or `.czi` files. The snippets
# below are intentionally not executed here; they show the shape of the code we
# will complete once example files are available.
#
# A current unified option is BioIO with reader plug-ins:
#
# ```bash
# uv add bioio bioio-ome-tiff bioio-ome-zarr bioio-lif bioio-nd2 bioio-czi
# ```
#
# The common pattern is:
#
# ```python
# from bioio import BioImage
#
# img = BioImage("path/to/file")
# print(img.scenes)
# print(img.dims.order, img.shape)
# data = img.get_image_data("CZYX", T=0)
# ```
#
# `.lif` example, often with multiple scenes or acquisitions:
#
# ```python
# lif = BioImage("experiment.lif")
# print(lif.scenes)
# lif.set_scene(0)
# lif_data = lif.get_image_data("CZYX", T=0)
# ```
#
# `.nd2` example, often time-lapse, z-stack, or multichannel Nikon data:
#
# ```python
# nd2 = BioImage("timelapse.nd2")
# print(nd2.dims.order, nd2.shape)
# first_time = nd2.get_image_data("CZYX", T=0)
# ```
#
# `.czi` example, often Zeiss data with scenes, pyramids, or mosaics:
#
# ```python
# czi = BioImage("experiment.czi")
# print(czi.scenes)
# czi.set_scene(0)
# czi_data = czi.get_image_data("CZYX", T=0)
# ```
#
# Pitfall: a reader may return a 5D array even when you think the image is 2D.
# Always inspect dimensions and select axes explicitly.

# %%
reader_examples = {
    "lif": "BioImage('experiment.lif').get_image_data('CZYX', T=0)",
    "nd2": "BioImage('timelapse.nd2').get_image_data('CZYX', T=0)",
    "czi": "BioImage('experiment.czi').get_image_data('CZYX', T=0)",
}
for extension, example in reader_examples.items():
    print(f".{extension}: {example}")

# %% [markdown]
# ## When a reader fails
#
# Practical troubleshooting order:
#
# 1. Confirm the file opens in the vendor software or Fiji/Bio-Formats.
# 2. Check whether the Python reader needs a plug-in or Java/Bio-Formats.
# 3. Try reading a single scene or plane before loading the whole dataset.
# 4. Convert a copy to OME-TIFF or OME-Zarr and record the conversion command.
# 5. Never overwrite the raw acquisition file.

# %% [markdown]
# ## Optional exercises
#
# 1. Save the synthetic image as PNG and compare its dtype after loading.
# 2. List five metadata fields you would want before measuring cell area.
# 3. Write a pseudocode function `open_first_scene(path)` that returns a
#    `CZYX` array from a BioIO-readable file.
# 4. Explain why JPEG is risky for threshold-based segmentation.

# %%
# Answer sketch (optional, removable)
png_path = output_dir / "synthetic_cells.png"
io.imsave(png_path, util.img_as_ubyte(image))
png_loaded = io.imread(png_path)
print(png_loaded.shape, png_loaded.dtype)

metadata_fields = [
    "axis order",
    "pixel size x/y/z",
    "channel names",
    "time interval",
    "compression",
]
print(metadata_fields)


def open_first_scene_pseudocode(path: str) -> str:
    return (
        "from bioio import BioImage\n"
        f"img = BioImage({path!r})\n"
        "img.set_scene(0)\n"
        "data = img.get_image_data('CZYX', T=0)"
    )


print(open_first_scene_pseudocode("example.czi"))
print("JPEG can shift intensities near the threshold and create false edges or holes.")
