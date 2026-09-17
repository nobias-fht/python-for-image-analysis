# %% [markdown]
# # Module 3: opening bio-image formats
#
# Time: 1 hour.
#
# There are many file formats that you might use during your career as a microscopist or bioimage analyst.
# Many of these file formats contain more than just pixel data - they contain metadata including
# information about the setitngs of the microscope and information about the acquisition.
#
# Much of this information will be essential in any downstream processing!
# In this section we will explore some of these formats, and the tools we can use to open them.
#
#
# The BioFormats team keeps a list of file formats and some infomation about each [here](https://bio-formats.readthedocs.io/en/v8.5.0/supported-formats.html).
# At current count there are more than 160 file formats, and that's just the ones that can be read by BioFormats!
#
#

# %%


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


# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from skimage import io, util
from skimage import data, filters

# %% [markdown]
# ## Format landscape
#
# Some of the more common file formats you might encounter are:
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
# - Use JPEG/PNG only for presentation or quick visual checks.
# <div style="
#   background: #fdecec;
#   border-left: 6px solid #d64545;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #7f1d1d;
# ">
#   <strong style="color: #7f1d1d;">Warning</strong><br>
#  You should ALWAYS keep the original files that came off the microscope. These are primary data and should be safely stored!  </div>
#

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

image = data.cells3d()

output_dir = Path("scratch_outputs")
output_dir.mkdir(exist_ok=True)

# image = image_with_background()
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

image_original = loaded[30, 1, :, :]

io.imsave(jpg_path, util.img_as_ubyte(image_original), quality=25)
jpeg_loaded = io.imread(jpg_path)

difference = (
    image_original.astype(float) / image_original.max()
    - jpeg_loaded.astype(float) / 255
)
print("mean absolute JPEG difference:", np.abs(difference).mean())

fig, axes = plt.subplots(1, 3, figsize=(9, 3))
axes[0].imshow(image_original, cmap="gray")
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
# And if we look closer at the image, we can see the result of the JPEG compression. Do you want to quantify this image?

# %%
fig, axes = plt.subplots(figsize=(3, 3))
axes.imshow(jpeg_loaded[150:200, 150:200], cmap="gray")


# %% [markdown]
# ## Reader examples for real microscopy formats
#
# Now we will example some vendor microscopy formats. The three you will commonly run into are `.lif` (Leica),
# `.nd2` (Nikon), and `.czi` (Zeiss). Luckily, there is a python package that can read them all (and others!)
#
# In this course we will use the `BioIO` plugin. The documentation can be found [here](https://bioio-devs.github.io/bioio/index.html)
#
# We can install BioIO into our environment using .
#
#
# ```bash
# uv add bioio
# ```
# However, BioIO has a modular framework, so we will also need to install the individual reader plugins for each format.
# We can do this all in one line by using:
# ```bash
# uv add bioio bioio-ome-tiff bioio-ome-zarr bioio-lif bioio-nd2 bioio-czi
# ```
#
# Once installed, the common pattern is:
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
# Here we generate a `BioImage` object that contains not just the image data, but also associated metadata.

# %% [markdown]
# ## Let's try opening some real file formats!
#
#

# %% [markdown]
# <div style="
#   background: #accffb;
#   border-left: 6px solid #2f80ed;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #21457f;
# ">
#   <strong style="color: #21457f;">Exercise</strong><br>
#  Use BioIO to open the supplied CZI file. Print the axis dimensions
# </div>

# %%
test_czi_path = "/facility/imganfac/Damian/test_vendor_formats/test.czi"

# %%
from bioio import BioImage

czi = BioImage(test_czi_path)
czi_data = czi.get_image_data("CZYX")
print(czi_data.shape)

# %% [markdown]
# ## Inspect the file types
#
# <div style="
#   background: #accffb;
#   border-left: 6px solid #2f80ed;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #21457f;
# ">
#   <strong style="color: #21457f;">Exercise</strong><br>
#  Inspect the type of each of the objects ('czi' and 'czi_data'). Why are they different?
# </div>

# %%
print(type(czi))
print(type(czi_data))

# %% [markdown]
# ## Reading Metadata
#
# One advantage of using microscope vendor formats is that they come with a lot of metadata that can be inspected. Let's look at some of the metadata from our images.
#
# BioIO can read the metadata from any image format it supports. You can find the documentation [here](https://bioio-devs.github.io/bioio/OVERVIEW.html#metadata-reading).
#
# Once we have a BioImage object, we can access the metadata using
#
# ```python
# metadata = img.metadata
# ```
#
# In this case this returns an XML document

# %%
metadata = czi.metadata

print(type(metadata))


# %% [markdown]
# BioIO exposes some more common useful metadata directly from the BioImage object
#
# <div style="
#   background: #accffb;
#   border-left: 6px solid #2f80ed;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #21457f;
# ">
#   <strong style="color: #21457f;">Exercise</strong><br>
#  Print the X and Y pixel sizes from the metadata. Hint: Check the documentation
# </div>

# %%
print(czi.physical_pixel_sizes.X)
print(czi.physical_pixel_sizes.Y)

# %% [markdown]
# BioIO also exposes a list of standard metadata, which can be access using
#
# ```python
# standard_metadata = dir(czi.standard_metadata)
# ```
#
# From here we can see all the associated metadata, and access it diretcly using, for example:
#
# ```python
# image_size_x = czi.standard_metadata.image_size_x
# ```
#
#
# <div style="
#   background: #accffb;
#   border-left: 6px solid #2f80ed;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #21457f;
# ">
#   <strong style="color: #21457f;">Exercise</strong><br>
#  Print the standard metadata, and see if you can find out who collected this image
# </div>

# %%
standard_properties = dir(czi.standard_metadata)
print(standard_properties)
print(czi.standard_metadata.imaged_by)


# %% [markdown]
# ## Other file formats
#
# Try opening some other file formats with BioIO. Access the metadata and see what it contains.

# %%

# %% [markdown]
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
#

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
