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
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import CenteredNorm
import numpy as np
import skimage

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
# - Has any pre-processing already been applied to the image? This is sometimes an option at acquisition time.
# - Did the export preserve metadata or only pixel values?

# %% [markdown]
# ## Saving and Loading images with SciKit-Image
#
# Sci-Kit image has an `io` module that can be used to conveniently open and save a variety of common image format with the `skimage.io.imread` and `skimage.io.imsave` functions.
#
# Real microscopy data should usually be read with format-aware tools that preserve metadata, but the basic principle is the same: read, inspect, and only then analyze.
#
# Nevertheless, let's save the previously introduced example data and then save it again.

# %%
image = skimage.data.cells3d()

output_dir = Path("../data/outputs")
output_dir.mkdir(exist_ok=True)

uint16_image = skimage.util.img_as_uint(image)  # make sure the image is uint16
tif_path = output_dir / "synthetic_cells.tif"
skimage.io.imsave(tif_path, uint16_image)  # save the data

loaded = skimage.io.imread(tif_path)  # load the data we just saved
print("loaded:", loaded.shape, loaded.dtype, loaded.min(), loaded.max())

# %% [markdown]
# <div style="
#   background: #e8f7ec;
#   border-left: 6px solid #2f9e44;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #1f5f2c;
# ">
#   <strong style="color: #1f5f2c;">Question</strong><br>
#
#   What did `imread` return?
#
#   Is there other information related to the data which would be useful to have access to when performing analysis?
# </div>

# %% [markdown]
# ## JPEG compression is convenient, not measurement-safe
#
# Lossy compression changes pixel values. That may be acceptable for a figure,
# but it is usually not acceptable for intensity measurement, segmentation, or
# reproducibility.
#
# If we save the example data again, this time as a JPEG, we see that the resulting image no longer has the same pixel values as the original.

# %%
image_original = loaded[30, 1, :, :]

# save the data in JPEG format
jpg_path = output_dir / "synthetic_cells.jpg"
skimage.io.imsave(jpg_path, skimage.util.img_as_ubyte(image_original), quality=25)
jpeg_loaded = skimage.io.imread(jpg_path)

# we will display the difference to see where each image is greater than the other
difference = (
    image_original.astype(float) / image_original.max()
    - jpeg_loaded.astype(float) / jpeg_loaded.max()
)
print("mean absolute JPEG difference:", np.abs(difference).mean())

fig, axes = plt.subplots(1, 3, figsize=(9, 3))
axes[0].imshow(image_original, cmap="gray")
axes[0].set_title("TIFF")
axes[1].imshow(jpeg_loaded, cmap="gray")
axes[1].set_title("JPEG")
axes[2].imshow(difference, cmap="bwr", norm=CenteredNorm(), interpolation="none")
axes[2].set_title("difference")
for ax in axes:
    ax.axis("off")
plt.tight_layout()
plt.show()

# %% [markdown]
# <div style="
#   background: #fff8db;
#   border-left: 6px solid #e2b200;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #8a6a00;
# ">
#   <strong style="color: #8a6a00;">Note</strong><br>
#
#   Where the difference display is red or blue shows where either the TIFF or JPEG image is greater, respectively.
#
#   We see that most of the pixels did not retain there original value.
# </div>

# %% [markdown]
# And if we look closer at the image, we can see the result of the JPEG compression. Would you want to quantify this image?

# %%
fig, axes = plt.subplots(figsize=(3, 3))
axes.imshow(jpeg_loaded[150:200, 150:200], cmap="gray")


# %% [markdown]
# ## Reader examples for real microscopy formats
#
# Now we will example some vendor microscopy formats. The three you will commonly run into are `.lif` (Leica),
# `.nd2` (Nikon), and `.czi` (Zeiss). Luckily, there is a python package that can read them all (and others!)
#
# In this course we will use the `BioIO` package. The documentation can be found [here](https://bioio-devs.github.io/bioio/index.html).
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
test_czi_path = "/Volumes/imganfac/Damian/test_vendor_formats/test.czi"

# %%
from bioio import BioImage

czi = BioImage(test_czi_path)
czi_data = czi.get_image_data("CZYX")
print(czi_data.shape)

# %% [markdown]
# <div style="
#   background: #e8f7ec;
#   border-left: 6px solid #2f9e44;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #1f5f2c;
# ">
#   <strong style="color: #1f5f2c;">Question</strong><br>
#
#   Read the docs for the `BioImage.get_image_data` method.
#
#   What happens if you request an axes that was not originally present in the data?
# </div>

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
