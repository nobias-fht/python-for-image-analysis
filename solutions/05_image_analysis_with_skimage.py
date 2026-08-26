# %% [markdown]
# # Module 5: image analysis operations
#
# Time: 2 hours 30 minutes.
#
# Most classical bio-image pipelines will look like something along the lines of:
# - Image inspection
# - Noise reduction
# - Background correction
# - Thresholding
# - Morphology
# - Instance separation
# - Measurement
#
# In this module, we will explore these operations suing `scikit-image`. The goal is not to memorize every
# function, but to learn to navigate the `scikit-image` library.
#
# <div style="display: flex; align-items: center; gap: 12px;">
#     <img src="https://raw.githubusercontent.com/scikit-image/scikit-image/refs/heads/main/doc/source/_static/logo.png" alt="Logo" style="height: 40px; width: auto;">
#     scikit-image
# </div>
#
# scikit-image, or `skimage` (as we will write to import it), is an open-source scientific image processing library.
#
# ### Question
#
# How to run standard image processing on NumPy arrays?
#
# ### Objective
#
# - Learn to navigate scikit-image
# - Learn standard operations

# %% [markdown]
# ## 1 - Navigate `skimage`
#
# Scikit-image has a fantastic [gallery of examples](https://scikit-image.org/docs/stable/auto_examples/index.html).
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
#   Click on one example in the gallery, copy paste the code in the next cell and run it!
# </div>

# %%
# --- Exercise
# Paste example code here
# ---

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
#   A colleague of yours told you to apply a Gaussian filter. Can you find in scikit-image docs the API for the Gaussian filter and import the function here?
# </div>

# %%
# --- Exercise
# Import the Gaussian filter method from scikit-image
from skimage.filters import gaussian

# ---

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
#   Can you find the API in scikit-image docs? What parameters does it require?
# </div>

# %% [markdown]
# ## 2 - Inspecting an image

# %%
# --- Import what we need
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import ndimage as ndi
from skimage import filters, measure, morphology, segmentation, data

# %% [markdown]
# Scikit-image comes with [example data](https://scikit-image.org/docs/stable/api/skimage.data.html), let's download `cells3d` and inspect the image.
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
#   What is the shape of the image?
# </div>

# %%
image = data.cells3d()

# --- Exercise
# Print the image shape
print(f"Image shape: {image.shape}")
# ---

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
#   Can you guess the axes?
# </div>

# %%
# --- Exercise
# Show the image
plt.imshow(image[30, 1])
# ---

# %% [markdown]
# It is always a good idea to start by inspecting the intensity distribution of an image. Histograms are a quick way to see background, foreground, saturation, and
# whether a global threshold might be plausible.
#
# Let's plot the histogram next to an image using `plt.subplots`.
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
#   Plot the histogram of the image using "hist" on the right pane.
#
#   <b>hint</b>: rather than plotting the histogram of a 2D image, we can linearize the image
#   using "img_slice.ravel()".
# </div>

# %%
# --- Choose which slice of the image you want to inspect
img_slice = image[30, 1]

# We create the subplot and show the image in the left-hand panel
fig, axes = plt.subplots(
    1,
    2,
    figsize=(8, 4),
    gridspec_kw={
        "width_ratios": [1.4, 1]
    },  # this is just to make the figure look nicer
    constrained_layout=True,
)
axes[0].imshow(img_slice)
axes[0].set_title("Image")
axes[0].axis("off")

# --- Exercise
# Plot the histogram
axes[1].hist(img_slice.ravel(), bins=50)
axes[1].set_xlabel("Intensity")
axes[1].set_ylabel("Pixel count")
axes[1].set_title("Histogram")
# ---

plt.show()

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
#   What problems can you in an histogram? We've prepared some examples. Plot the iamge and its histogram side by side.
# </div>

# %%
from python_for_ia import images_with_problematic_hist

img_lst = images_with_problematic_hist()

fig, axes = plt.subplots(len(img_lst), 2, figsize=(6, 8), constrained_layout=True)

for row, (title, img_r) in enumerate(img_lst):
    # --- Exercise
    # Plot image `img_r` and its histogram side by side
    axes[row, 0].imshow(img_r)

    axes[row, 1].hist(img_r.ravel(), bins=64)
    # ---

    axes[row, 0].set_title(title)
    axes[row, 0].axis("off")

    axes[row, 1].set_title(f"{title} histogram")
    axes[row, 1].set_xlabel("Intensity")
    axes[row, 1].set_ylabel("Pixel count")


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
#   We will re-use this code, so let's make it a function.
#
#   <b>Hint</b>: it is important to make sure you are using the function's parameters and
#   not variable defined in your notebook, otherwise you will get strange results. It is a
#   good habit to use different variable names in your functions.
# </div>


# %%
def plot_histogram(img):
    # --- Exercise
    # Add code here
    _, axes = plt.subplots(
        1,
        2,
        figsize=(8, 4),
        gridspec_kw={
            "width_ratios": [1.4, 1]
        },  # this is just to make the figure look nicer
        constrained_layout=True,
    )

    axes[0].imshow(img, cmap="gray")
    axes[0].set_title("Image")
    axes[0].axis("off")

    axes[1].hist(img.ravel(), bins=50)
    axes[1].set_xlabel("Intensity")
    axes[1].set_ylabel("Pixel count")
    axes[1].set_title("Histogram")

    plt.show()
    # ---


# %% [markdown]
# ## 3 - Image filters
#
# An image filter is a small matrix representing a mathematical operation that gets applied to each pixel in an image (we talk of "convolutions"). An example is the following:
#
# $$
# \begin{bmatrix}
# 0 & 1 & 0 \\
# 1 & -4 & 1 \\
# 0 & 1 & 0
# \end{bmatrix}
# $$
#
# There are many reason to use an image filter: it can help smooth an image before segmentation, it can highlights particular features (e.g. edges), etc. Filtering changes pixel values, therefore they should be applied with reason dependeing on the analysis need, and filtered image should not be used for intensity quantification. But they can be used to help downstream analysis separate region for later intensity quantification on the original image.
#
# Here are a few standard image filters: Gaussian, Median, Sobel. Let's play around with them!
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
#   Apply the Gaussian filter to a slice of our image. What does it do?
#
#   <b>hint:</b> We already imported it, but we also imported the "filters" module from scikit-image.
# </div>

# %%
# --- Choose the slice
img_slice = image[30, 1]

# --- Exercise
# Apply the Gaussian filter and show the original and result next to each other.
slice_gauss = filters.gaussian(img_slice, sigma=1.5)

fig, axes = plt.subplots(1, 2, figsize=(8, 3.5))
axes[0].imshow(img_slice)
axes[0].set_title("Original")
axes[0].axis("off")
axes[1].imshow(slice_gauss)
axes[1].set_title("Gaussian-filtered")
axes[1].axis("off")

plt.tight_layout()
# ---

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
#   Do the same for the median filter. What does it do?
# </div>

# %%
# --- Choose the slice
img_slice = image[30, 1]

# --- Exercise
# Apply the Gaussian filter and show the original and result next to each other.
slice_median = filters.median(img_slice)

fig, axes = plt.subplots(1, 2, figsize=(8, 3.5))
axes[0].imshow(img_slice)
axes[0].set_title("Original")
axes[0].axis("off")
axes[1].imshow(slice_median)
axes[1].set_title("Median-filtered")
axes[1].axis("off")

plt.tight_layout()
# ---

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
#   Let's try again the median filter, but this time let's pretend our image has a lot of hot pixels.
# </div>

# %%
from skimage.util import random_noise

# --- Choose the slice
img_slice = image[30, 1]

# We add noise for the purpose of the exercise
img_slice = random_noise(img_slice, mode="s&p", amount=0.05)

# --- Exercise
# Use the same code as previously
slice_median = filters.median(img_slice)

fig, axes = plt.subplots(1, 2, figsize=(8, 3.5))
axes[0].imshow(img_slice)
axes[0].set_title("Original")
axes[0].axis("off")
axes[1].imshow(slice_median)
axes[1].set_title("Median-filtered")
axes[1].axis("off")

plt.tight_layout()
# ---

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
#   Last filter: the famous Sobel. What does it do?
# </div>

# %%
# --- Choose the slice
img_slice = image[30, 0]

# --- Exercise
# Apply the Gaussian filter and show the original and result next to each other.
slice_sobel = filters.sobel(img_slice)

fig, axes = plt.subplots(1, 2, figsize=(8, 3.5))
axes[0].imshow(img_slice)
axes[0].set_title("Original")
axes[0].axis("off")
axes[1].imshow(slice_sobel)
axes[1].set_title("Sobel-filtered")
axes[1].axis("off")

plt.tight_layout()
# ---

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
#  Let's try it on another image.
# </div>

# %%
# --- Choose the slice
sobel_image = data.human_mitosis()[:200, :200]

# --- Exercise
# Apply the Gaussian filter and show the original and result next to each other.
slice_sobel = filters.sobel(sobel_image)

fig, axes = plt.subplots(1, 2, figsize=(8, 3.5))
axes[0].imshow(sobel_image)
axes[0].set_title("Original")
axes[0].axis("off")
axes[1].imshow(slice_sobel)
axes[1].set_title("Sobel-filtered")
axes[1].axis("off")

plt.tight_layout()
# ---

# %% [markdown]
# <div style="
#   background: #f3f4f6;
#   border-left: 6px solid #6b7280;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #374151;
# ">
#   <strong>Optional Exercise</strong><br>
#   Explore more filters from scikit-image.
# </div>
#
#
# ### Conclusion
#
#
# <details>
#   <summary>So what are these filters used for?</summary>
#
#   <ul>
#     <li><strong>Gaussian:</strong> reduce high-frequency noise (smoothing) before thresholding.</li>
#     <li><strong>Median:</strong> reduce salt-and-pepper noise while preserving edges.</li>
#     <li><strong>Sobel:</strong> highlight edges, usually for inspection or feature design.</li>
#   </ul>
# </details>

# %% [markdown]
# ## 4 - Background correction
#
# There are many ways to deal with background, and they are all specific to the type of
# background you are battling with. You will not deal with uneven background the same way
# than uniform one for instance.
#
# Two main methods are used for background correction: averaging a stack when your signal
# is moving but not the background, or separating the background from signal when they have
# different spatial frequencies (background is varying slowly across the image, while
# signal is changing on the small scale).
#
# In the second case, a simple background estimate can be made with heavy Gaussian smoothing or a
# morphological top-hat. These are not universal solutions, but they introduce
# an important principle: separate slow background variation from object signal.
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
#  Let's see what our image with background looks like. Explore the image.
# </div>

# %%
from python_for_ia import image_with_background

img = image_with_background()

# --- Exercise
plot_histogram(img)
# ---

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
#   Now let's apply our Gaussian filter to the image and see what we see. How can you subtract the background from the image?
#
#   <b>Hint</b>: don't forget to look at the histogram.
# </div>

# %%
# --- Exercise
# Apply Gaussian filter and subtract background
bg = filters.gaussian(img, sigma=20)
plot_histogram(img - bg)
# ---


# %% [markdown]
# <div style="
#   background: #f3f4f6;
#   border-left: 6px solid #6b7280;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #374151;
# ">
#   <strong>Optional Exercise</strong><br>
#   There is a way to directly filter the backgroudn from the image using "morphology.white_tophat(img, footprint=morphology.disk(16))". Give it a try.
# </div>
#
#
# <div style="
#   background: #f3f4f6;
#   border-left: 6px solid #6b7280;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #374151;
# ">
#   <strong>Optional Exercise</strong><br>
#   Check out the rolling-ball algorithm from scikit-image example gallery.
# </div>
#

# %% [markdown]
# ## 5 - Thresholding
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
