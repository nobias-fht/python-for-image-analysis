# %% [markdown]
# # Module 4: visualizing images
#
# Time: 1 hour.
#
# Essential ideas: visualization is part of analysis, not decoration. Display
# choices can reveal objects, hide artifacts, or accidentally suggest a result
# that the data do not support.

# %%
import matplotlib.pyplot as plt
import numpy as np
from skimage import color, exposure, filters, measure, segmentation

from src.python_for_ia import make_blobs

# %%
image = make_blobs(seed=11)
mask = image > filters.threshold_otsu(image)
labels = measure.label(mask)
labels = segmentation.clear_border(labels)

# %% [markdown]
# ## Display contrast is not data processing
#
# `vmin` and `vmax` change how an image is displayed. They do not change the
# array stored in memory. This is useful for inspection, but the chosen limits
# should be reported when they affect interpretation.

# %%
p1, p99 = np.percentile(image, (1, 99))

fig, axes = plt.subplots(1, 3, figsize=(9, 3))
axes[0].imshow(image, cmap="gray")
axes[0].set_title("default")
axes[1].imshow(image, cmap="gray", vmin=p1, vmax=p99)
axes[1].set_title("1-99% display")
axes[2].hist(image.ravel(), bins=80)
axes[2].axvline(p1, color="tab:orange")
axes[2].axvline(p99, color="tab:orange")
axes[2].set_title("histogram")
for ax in axes[:2]:
    ax.axis("off")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Images, masks, labels, and overlays
#
# When to use:
#
# - image alone: inspect signal and background,
# - mask: inspect foreground/background decisions,
# - labels: inspect instance segmentation,
# - overlay: inspect whether labels align with the image.
#
# Pitfall: colorful label images are categorical. Do not interpret label colors
# as intensities.

# %%
overlay = color.label2rgb(labels, image=image, bg_label=0, alpha=0.35)
boundaries = segmentation.find_boundaries(labels)

rgb = np.dstack([image, image, image])
rgb = exposure.rescale_intensity(rgb, out_range=(0, 1))
rgb[boundaries] = [1, 0, 0]

fig, axes = plt.subplots(1, 4, figsize=(11, 3))
for ax, img, title, cmap in zip(
    axes,
    [image, mask, labels, overlay],
    ["image", "mask", "labels", "overlay"],
    ["gray", "gray", "nipy_spectral", None],
):
    ax.imshow(img, cmap=cmap)
    ax.set_title(title)
    ax.axis("off")
plt.tight_layout()
plt.show()

plt.figure(figsize=(4, 4))
plt.imshow(rgb)
plt.title("label boundaries")
plt.axis("off")
plt.show()

# %% [markdown]
# ## Small multiples for parameter comparison
#
# Small multiples are often clearer than one "best" image. Use them when you
# need to explain how a parameter changes the result.

# %%
thresholds = [0.25, 0.35, 0.45, filters.threshold_otsu(image)]
titles = ["0.25", "0.35", "0.45", "Otsu"]

fig, axes = plt.subplots(1, len(thresholds), figsize=(10, 3))
for ax, threshold, title in zip(axes, thresholds, titles):
    ax.imshow(image > threshold, cmap="gray")
    ax.set_title(title)
    ax.axis("off")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Napari preview
#
# Napari is useful for interactive inspection of multidimensional images, label
# layers, points, shapes, and manual quality control.
#
# When to use: visual QC, browsing z-stacks/time series, checking labels across
# channels. For automated scripts and papers, still export static plots or data
# tables that document what was checked.

# %%
try:
    import napari

    viewer = napari.Viewer()
    viewer.add_image(image, name="synthetic image", colormap="gray")
    viewer.add_labels(labels, name="segmentation")
except ImportError:
    print("napari is optional. Install with: uv add --optional napari 'napari[all]'")

# %% [markdown]
# ## Optional exercises
#
# 1. Make a 2 x 2 figure showing image, mask, labels, and boundaries.
# 2. Change the overlay alpha and describe what becomes easier or harder to see.
# 3. Plot the same image with `gray`, `magma`, and `viridis` colormaps.
# 4. Count labels and write the count in a plot title.

# %%
# Answer sketch (optional, removable)
fig, axes = plt.subplots(2, 2, figsize=(7, 7))
axes = axes.ravel()
for ax, img, title, cmap in zip(
    axes,
    [image, mask, labels, rgb],
    ["image", "mask", f"{labels.max()} labels", "boundaries"],
    ["gray", "gray", "nipy_spectral", None],
):
    ax.imshow(img, cmap=cmap)
    ax.set_title(title)
    ax.axis("off")
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 3, figsize=(9, 3))
for ax, cmap in zip(axes, ["gray", "magma", "viridis"]):
    ax.imshow(image, cmap=cmap, vmin=p1, vmax=p99)
    ax.set_title(cmap)
    ax.axis("off")
plt.tight_layout()
plt.show()
