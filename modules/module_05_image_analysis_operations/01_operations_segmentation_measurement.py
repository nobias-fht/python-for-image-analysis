# %% [markdown]
# # Module 5: image analysis operations
#
# Essential ideas: inspect intensity distributions, reduce noise, segment
# foreground, split touching objects, clean masks, and measure labeled regions.

# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import ndimage as ndi
from skimage import filters, measure, morphology, segmentation

from course_utils import make_blobs

# %%
image = make_blobs(shape=(192, 192), n_blobs=35, seed=14)

# %% [markdown]
# ## Histogram and filtering

# %%
gaussian = filters.gaussian(image, sigma=1.5)
median = filters.median(image, morphology.disk(2))
laplacian = filters.laplace(image)

fig, axes = plt.subplots(1, 4, figsize=(11, 3))
for ax, img, title in zip(
    axes,
    [image, gaussian, median, laplacian],
    ["raw", "gaussian", "median", "laplacian"],
):
    ax.imshow(img, cmap="gray")
    ax.set_title(title)
    ax.axis("off")
plt.tight_layout()
plt.show()

plt.hist(image.ravel(), bins=80)
plt.xlabel("intensity")
plt.ylabel("pixel count")
plt.show()

# %% [markdown]
# ## Thresholding, morphology, and watershed

# %%
manual_mask = image > 0.35
otsu_mask = image > filters.threshold_otsu(image)
clean = morphology.remove_small_objects(otsu_mask, min_size=40)
clean = morphology.remove_small_holes(clean, area_threshold=40)

distance = ndi.distance_transform_edt(clean)
peaks = morphology.local_maxima(distance)
markers = measure.label(peaks)
labels = segmentation.watershed(-distance, markers, mask=clean)

fig, axes = plt.subplots(1, 4, figsize=(11, 3))
for ax, img, title in zip(
    axes,
    [manual_mask, otsu_mask, distance, labels],
    ["manual", "otsu", "distance", "watershed"],
):
    ax.imshow(img, cmap="gray" if title != "watershed" else "nipy_spectral")
    ax.set_title(title)
    ax.axis("off")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Region properties

# %%
props = measure.regionprops_table(
    labels,
    intensity_image=image,
    properties=("label", "area", "mean_intensity", "eccentricity"),
)
df = pd.DataFrame(props)
print(df.head())

# %% [markdown]
# ## Optional exercises
#
# 1. Compare the object count from manual and Otsu thresholding.
# 2. Add `solidity` to the measured region properties.

# %%
# Answer sketch (optional, removable)
manual_count = measure.label(manual_mask).max()
otsu_count = measure.label(otsu_mask).max()
print(manual_count, otsu_count)
props_with_solidity = measure.regionprops_table(labels, properties=("label", "solidity"))
print(pd.DataFrame(props_with_solidity).head())
