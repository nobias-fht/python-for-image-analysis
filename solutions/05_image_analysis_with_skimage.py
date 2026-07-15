# %% [markdown]
# # Module 5: image analysis operations
#
# Time: 2 hours 30 minutes.
#
# Essential ideas: most classical bio-image pipelines combine intensity
# inspection, noise reduction, background correction, thresholding, morphology,
# instance separation, and measurement. The goal is not to memorize every
# function, but to learn which operation answers which kind of problem.

# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import ndimage as ndi
from skimage import exposure, filters, measure, morphology, segmentation

from course_utils import make_blobs

# %%
image = make_blobs(shape=(192, 192), n_blobs=35, seed=14)

# %% [markdown]
# ## Inspect intensities first
#
# Histograms are a quick way to see background, foreground, saturation, and
# whether a global threshold might be plausible.
#
# Pitfall: a histogram ignores spatial structure. Always pair it with image
# display.

# %%
fig, axes = plt.subplots(1, 2, figsize=(8, 3))
# --- Exercise
axes[0].imshow(image, cmap="gray")
axes[0].set_title("Image")
axes[0].axis("off")
axes[1].hist(image.ravel(), bins=100)
axes[1].set_xlabel("intensity")
axes[1].set_ylabel("pixel count")
# ---
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Denoising and edge-enhancing filters
#
# When to use:
#
# - Gaussian: reduce high-frequency noise before thresholding.
# - Median: reduce salt-and-pepper noise while preserving edges.
# - Laplace/Sobel: highlight edges, usually for inspection or feature design.
# - Unsharp mask: enhance local contrast for visualization or specific tasks.
#
# Pitfall: filtering changes pixel values. Do not apply filters just because the
# image looks nicer; connect the operation to an analysis need.

# %%
gaussian = filters.gaussian(image, sigma=1.5)
median = filters.median(image, footprint=morphology.disk(2))
laplacian = filters.laplace(image)
sobel = filters.sobel(image)
unsharp = filters.unsharp_mask(image, radius=2, amount=1)

fig, axes = plt.subplots(2, 3, figsize=(10, 6))
for ax, img, title in zip(
    axes.ravel(),
    [image, gaussian, median, laplacian, sobel, unsharp],
    ["raw", "gaussian", "median", "laplacian", "sobel", "unsharp"],
):
    ax.imshow(img, cmap="gray")
    ax.set_title(title)
    ax.axis("off")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Background correction
#
# A simple background estimate can be made with heavy Gaussian smoothing or a
# morphological top-hat. These are not universal solutions, but they introduce
# an important principle: separate slow background variation from object signal.
#
# When to use:
#
# - Gaussian background: smooth uneven illumination.
# - White top-hat: emphasize bright objects smaller than the structuring
#   element.
#
# Pitfall: choose the scale from object size. If the background filter is too
# small, it removes real objects.

# %%
background = filters.gaussian(image, sigma=20)
background_subtracted = np.clip(image - background, 0, None)
top_hat = morphology.white_tophat(image, footprint=morphology.disk(12))

fig, axes = plt.subplots(1, 4, figsize=(12, 3))
for ax, img, title in zip(
    axes,
    [image, background, background_subtracted, top_hat],
    ["raw", "estimated background", "subtracted", "white top-hat"],
):
    ax.imshow(img, cmap="gray")
    ax.set_title(title)
    ax.axis("off")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Thresholding
#
# A threshold turns an intensity image into a foreground/background mask.
#
# - Manual threshold: useful for teaching and controlled images.
# - Otsu threshold: useful when foreground and background form separable
#   intensity distributions.
# - Local threshold: useful when illumination varies across the field.
#
# Pitfall: thresholding is not object detection by itself. You still need QC,
# cleanup, and measurement rules.

# %%
manual_mask = background_subtracted > 0.15
otsu_mask = background_subtracted > filters.threshold_otsu(background_subtracted)
local_threshold = filters.threshold_local(
    background_subtracted, block_size=35, offset=-0.02
)
local_mask = background_subtracted > local_threshold

fig, axes = plt.subplots(1, 4, figsize=(11, 3))
for ax, img, title in zip(
    axes,
    [background_subtracted, manual_mask, otsu_mask, local_mask],
    ["input", "manual", "otsu", "local"],
):
    ax.imshow(img, cmap="gray")
    ax.set_title(title)
    ax.axis("off")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Morphology and filling holes
#
# Morphology changes binary shapes using a neighborhood called a footprint.
#
# - Opening removes small bright structures.
# - Closing bridges small dark gaps.
# - `remove_small_objects` removes connected components below an area cutoff.
# - `remove_small_holes` or `ndi.binary_fill_holes` fills holes inside objects.
#
# When to use: after thresholding, before measurement, when the operation
# matches a clear object definition.

# %%
raw_mask = otsu_mask
opened = morphology.binary_opening(raw_mask, footprint=morphology.disk(1))
closed = morphology.binary_closing(opened, footprint=morphology.disk(2))
size_clean = morphology.remove_small_objects(closed, min_size=40)
holes_removed = morphology.remove_small_holes(size_clean, area_threshold=80)
filled_holes = ndi.binary_fill_holes(size_clean)

fig, axes = plt.subplots(1, 5, figsize=(13, 3))
for ax, img, title in zip(
    axes,
    [raw_mask, opened, closed, size_clean, filled_holes],
    ["raw mask", "opened", "closed", "small removed", "holes filled"],
):
    ax.imshow(img, cmap="gray")
    ax.set_title(title)
    ax.axis("off")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Skeletonization
#
# Skeletonization reduces binary objects to thin centerlines. It is useful for
# neurites, filaments, vessels, roots, or other elongated structures where
# length and branching matter more than area.
#
# Pitfall: skeletons are extremely sensitive to segmentation noise. Clean the
# mask first and inspect the result.

# %%
elongated = image > np.percentile(image, 80)
elongated = morphology.binary_closing(elongated, footprint=morphology.disk(2))
elongated = morphology.remove_small_objects(elongated, min_size=120)
skeleton = morphology.skeletonize(elongated)

fig, axes = plt.subplots(1, 3, figsize=(9, 3))
for ax, img, title in zip(
    axes,
    [image, elongated, skeleton],
    ["image", "clean mask", "skeleton"],
):
    ax.imshow(img, cmap="gray")
    ax.set_title(title)
    ax.axis("off")
plt.tight_layout()
plt.show()

print("skeleton length in pixels:", skeleton.sum())

# %% [markdown]
# ## Watershed for touching objects
#
# Watershed can split touching objects when a distance transform has meaningful
# peaks near object centers.
#
# When to use: roundish touching cells or nuclei. It is less appropriate for
# highly irregular objects unless markers are carefully designed.

# %%
clean = holes_removed
distance = ndi.distance_transform_edt(clean)
peaks = morphology.local_maxima(distance)
markers = measure.label(peaks)
labels = segmentation.watershed(-distance, markers, mask=clean)

fig, axes = plt.subplots(1, 4, figsize=(11, 3))
for ax, img, title in zip(
    axes,
    [clean, distance, markers, labels],
    ["clean mask", "distance", "markers", "watershed labels"],
):
    ax.imshow(img, cmap="gray" if title != "watershed labels" else "nipy_spectral")
    ax.set_title(title)
    ax.axis("off")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Region properties
#
# Measurements connect image processing to biological questions. Always keep
# the label image, measurement table, and parameters together so results can be
# checked later.

# %%
props = measure.regionprops_table(
    labels,
    intensity_image=image,
    properties=(
        "label",
        "area",
        "mean_intensity",
        "eccentricity",
        "solidity",
        "major_axis_length",
        "minor_axis_length",
    ),
)
df = pd.DataFrame(props)
df["ellipticity"] = 1 - df["minor_axis_length"] / df["major_axis_length"]
print(df.head())

# %% [markdown]
# ## Optional exercises
#
# 1. Compare object count after manual, Otsu, and local thresholding.
# 2. Change the `min_size` parameter and plot object count versus parameter.
# 3. Add `perimeter` and `centroid` to the region properties table.
# 4. Use `ndi.binary_fill_holes` on `local_mask` and show before/after.
# 5. Compute skeleton length for masks generated with two thresholds.

# %%
# Answer sketch (optional, removable)
for name, mask in [("manual", manual_mask), ("otsu", otsu_mask), ("local", local_mask)]:
    print(name, measure.label(mask).max())

min_sizes = [10, 40, 80, 160]
counts = []
for min_size in min_sizes:
    cleaned = morphology.remove_small_objects(otsu_mask, min_size=min_size)
    counts.append(measure.label(cleaned).max())
print(list(zip(min_sizes, counts)))

props_more = measure.regionprops_table(
    labels,
    intensity_image=image,
    properties=("label", "perimeter", "centroid", "mean_intensity"),
)
print(pd.DataFrame(props_more).head())

local_filled = ndi.binary_fill_holes(local_mask)
fig, axes = plt.subplots(1, 2, figsize=(6, 3))
axes[0].imshow(local_mask, cmap="gray")
axes[0].set_title("local mask")
axes[1].imshow(local_filled, cmap="gray")
axes[1].set_title("filled")
for ax in axes:
    ax.axis("off")
plt.tight_layout()
plt.show()

for threshold in [0.25, 0.4]:
    mask = morphology.remove_small_objects(image > threshold, min_size=120)
    print(threshold, morphology.skeletonize(mask).sum())
