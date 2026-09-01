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
#   background: #e8f7ec;
#   border-left: 6px solid #2f9e44;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #1f5f2c;
# ">
#   <strong style="color: #1f5f2c;">Question</strong><br>
#   Can you find the Gaussian filter API in scikit-image docs? What parameters does it require?
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
#   Print the shape of the image?
# </div>

# %%
image_cells = data.cells3d()

# --- Exercise
# Print the image shape
print(f"Image shape: {image_cells.shape}")
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
#   Can you show a slice of the image and guess the axes?
# </div>

# %%
# --- Exercise
# Show the image
plt.imshow(image_cells[30, 1])
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
#   <b>Hint</b>: rather than plotting the histogram of a 2D image, we can linearize the image
#   using "img_slice.ravel()".
# </div>

# %%
# --- Choose which slice of the image you want to inspect
img_slice = image_cells[30, 1]

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
#   What can you infer from an histogram? We've prepared some examples. Plot the images and their histogram side by side.
# </div>
# <div style="
#   background: #e8f7ec;
#   border-left: 6px solid #2f9e44;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #1f5f2c;
# ">
#   <strong style="color: #1f5f2c;">Question</strong><br>
#   Can you guess what happened to the images based on the histogram?
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
def plot_histogram(array):
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

    axes[0].imshow(array, cmap="gray")
    axes[0].set_title("Image")
    axes[0].axis("off")

    axes[1].hist(array.ravel(), bins=50)
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
#   Apply the Gaussian filter to a slice of our image.
#
#   <b>Hint:</b> We already imported it, but we also imported the "filters" module from scikit-image.
# </div>
# <div style="
#   background: #e8f7ec;
#   border-left: 6px solid #2f9e44;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #1f5f2c;
# ">
#   <strong style="color: #1f5f2c;">Question</strong><br>
#   What does a Gaussian filter do?
# </div>

# %%
# --- Select the slice
img_slice = image_cells[30, 1]

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
# --- Select the slice
img_slice = image_cells[30, 1]

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

# --- Select the slice
img_slice = image_cells[30, 1]

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
# --- Select the slice
img_slice = image_cells[30, 0]

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
# --- Select the slice
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
#   background: #fdecec;
#   border-left: 6px solid #d64545;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #7f1d1d;
# ">
#   <strong style="color: #7f1d1d;">TODO</strong><br>
#   Offset, flatfield, background (subtraction vs division)
#   </div>
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
#   Now let's apply our Gaussian filter to the image and see what we see. How can you subtract the background from the image?
# </div>
# <div style="
#   background: #e8f7ec;
#   border-left: 6px solid #2f9e44;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #1f5f2c;
# ">
#   <strong style="color: #1f5f2c;">Question</strong><br>
#   Do you see something strange in the histogram?
# </div>

# %%
# --- Exercise
# Apply Gaussian filter and subtract background
bg_gauss = filters.gaussian(img, sigma=20)
result_gauss = np.clip(img - bg_gauss, 0, None)

result_top_hat = morphology.white_tophat(img, footprint=morphology.disk(16))
bg_top_hat = img - result_top_hat


fig, axes = plt.subplots(
    2,
    3,
    figsize=(10, 8),
    gridspec_kw={
        "width_ratios": [1.4, 1.4, 1]
    },  # this is just to make the figure look nicer
    constrained_layout=True,
)

axes[0, 0].imshow(result_gauss)
axes[0, 0].set_title("Result Gauss")
axes[0, 0].axis("off")

axes[0, 1].imshow(bg_gauss)
axes[0, 1].set_title("Background")
axes[0, 1].axis("off")

axes[0, 2].hist(result_gauss.ravel(), bins=50)
axes[0, 2].set_xlabel("Intensity")
axes[0, 2].set_ylabel("Pixel count")
axes[0, 2].set_title("Histogram")

axes[1, 0].imshow(result_top_hat)
axes[1, 0].set_title("Result Top hat")
axes[1, 0].axis("off")

axes[1, 1].imshow(bg_top_hat)
axes[1, 1].set_title("Background")
axes[1, 1].axis("off")

axes[1, 2].hist(result_top_hat.ravel(), bins=50)
axes[1, 2].set_xlabel("Intensity")
axes[1, 2].set_ylabel("Pixel count")
axes[1, 2].set_title("Histogram")

plt.tight_layout()
# ---


# %% [markdown]
# <details>
#   <summary>Mystery function</summary>
#
#   ```python
#   img_subtraction = np.clip(resultat, 0, None) # clip negative values
#   ```
# </details>

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
#   Check out the rolling-ball algorithm from scikit-image example gallery.
# </div>
#

# %% [markdown]
# ## 5 - Thresholding
#
# A threshold turns an intensity image into a binary mask (foreground/background). These
# masks are useful because they allow us to select pixels from a particular area, for
# instance to measure intensity in the foreground compared to the background.
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
#   Perform a manual threshold on the image, and visualize the image, the mask and an
#   overlay of the two next to each other. Find the best threshold!
#
#   <b>Hint</b>: Remember the module on manipulating numpy arrays and on plotting.
# </div>

# %%
# --- Select the slice and threshold
img_slice = image_cells[30, 1]

# absolute threshold
threshold = 8_000  # 30_000

# --- Exercise
# Threshold the image and plot it as an overlay
mask_man = img_slice > threshold

fig, axes = plt.subplots(1, 3, figsize=(8, 3.5))
axes[0].imshow(img_slice)
axes[0].set_title("Image")
axes[0].axis("off")
axes[1].imshow(mask_man)
axes[1].set_title("Mask")
axes[1].axis("off")
axes[2].imshow(img_slice)
axes[2].imshow(mask_man, cmap="gray", alpha=0.5)
axes[2].set_title("Overlay")
axes[2].axis("off")

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
#   Let's try an automatic threshold. Have you heard of Otsu method?
#
#   <b>Hint</b>: Choose a different name for the mask so we can reuse it later together
#   with the previous one.
# </div>

# %%
# --- Select the slice and threshold
img_slice = image_cells[30, 1]

# --- Exercise
# Threshold the image using Otsu's threshold and plot it as an overlay
mask_otsu = img_slice > filters.threshold_otsu(img_slice)

fig, axes = plt.subplots(1, 3, figsize=(8, 3.5))
axes[0].imshow(img_slice)
axes[0].set_title("Image")
axes[0].axis("off")
axes[1].imshow(mask_otsu)
axes[1].set_title("Mask (Otsu)")
axes[1].axis("off")
axes[2].imshow(img_slice)
axes[2].imshow(mask_otsu, cmap="gray", alpha=0.5)
axes[2].set_title("Overlay")
axes[2].axis("off")

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
#   One of the main issue with simple thresholding is that it is global and not region
#   dependent. Search scikit-image <a href="https://scikit-image.org/docs/stable/api/skimage.filters.html">filters module docs</a>
#   for a potentially better solution.
# </div>

# %%
# --- Select the slice and threshold
img_slice = image_cells[30, 1]

# --- Exercise
# Threshold the image using Otsu's threshold and plot it as an overlay
mask_local = img_slice > filters.threshold_local(
    img_slice, block_size=127  # , offset=-0.02
)

fig, axes = plt.subplots(1, 3, figsize=(8, 3.5))
axes[0].imshow(img_slice)
axes[0].set_title("Image")
axes[0].axis("off")
axes[1].imshow(mask_local)
axes[1].set_title("Mask (Local)")
axes[1].axis("off")
axes[2].imshow(img_slice)
axes[2].imshow(mask_local, cmap="gray", alpha=0.5)
axes[2].set_title("Overlay")
axes[2].axis("off")

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
#   Now, plot all three next to each other.
# </div>

# %%
# --- Exercise
fig, axes = plt.subplots(1, 3, figsize=(8, 3.5))
axes[0].imshow(mask_man)
axes[0].set_title("Manual")
axes[0].axis("off")
axes[1].imshow(mask_otsu)
axes[1].set_title("Otsu")
axes[1].axis("off")
axes[2].imshow(mask_local)
axes[2].set_title("Local")
axes[2].axis("off")

plt.tight_layout()
# ---

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
#   What could we do to improve the masks?
# </div>

# %% [markdown]
# ## 6 - Morphological operations
#
# Morphological operations change binary shapes. For instance, they can be used to remove
# small bright structures, closing small gaps, fill holes etc.
#
# <div style="
#   background: #fff8db;
#   border-left: 6px solid #e2b200;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #8a6a00;
# ">
#   <strong style="color: #8a6a00;">Note</strong><br>
#   Scikit-image often uses a `footprint` as kernel for the morphological operations. Check out
#   <a href="https://scikit-image.org/docs/stable/auto_examples/numpy_operations/plot_structuring_elements.html">this page</a>
#   for some examples.
# </div>
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
#   Go to the docs page of `skimage.morphology` and browse the various operations. Try applying
#   two-three of them to the mask of your choice from the previous section. Show the results
#   side by side in a plot.
#
#   <b>Hint</b>: You can apply the operations on top of each other.
# </div>

# %%
# --- Choose a mask from the previous section
raw_mask = mask_man

# --- Exercise
remove_obj = morphology.remove_small_objects(raw_mask, max_size=40)
closed = morphology.closing(remove_obj, footprint=morphology.disk(1))
remove_holes = morphology.remove_small_holes(closed, max_size=100, connectivity=2)
final_mask = morphology.opening(remove_holes, footprint=morphology.disk(15))


lst_images = [
    ("Original mask", raw_mask),
    ("Remove small objects", remove_obj),
    ("Closed", closed),
    ("Remove small holes", remove_holes),
    ("Opened", final_mask),
]

fig, axes = plt.subplots(1, 5, figsize=(12, 3.5))

for idx, (title, img_idx) in enumerate(lst_images):
    axes[idx].imshow(img_idx)
    axes[idx].set_title(title)
    axes[idx].axis("off")

plt.tight_layout()
# ---

# %% [markdown]
# <details>
#   <summary>Mystery functions</summary>
#
#   Try remove_small_objects, closing, remove_small_holes and/or opening.
# </details>

# %% [markdown]
# ## 7 - Instance labels
#
# Often, it will be interesting to have more than a binary mask: all individual instances
# of a type of object. Instances of an object are represented by unique labels identifying
# each object, e.g. nuclei.
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
#   The nuclei in the final mask of the previous section seem easy to separate. Use `measure.label` to get instances and plot the result.
# </div>
# <div style="
#   background: #e8f7ec;
#   border-left: 6px solid #2f9e44;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #1f5f2c;
# ">
#   <strong style="color: #1f5f2c;">Question</strong><br>
#   Do you see a potential issue with the result?
# </div>

# %%
# --- Select the mask from the previous section
binary_mask = final_mask

# --- Exercise
from cmap import Colormap

fig, axes = plt.subplots(1, 2, figsize=(8, 3.5))
axes[0].imshow(measure.label(final_mask, connectivity=1))
axes[0].axis("off")
axes[0].set_title("Default color map")
axes[1].imshow(
    measure.label(final_mask, connectivity=1), cmap=Colormap("glasbey").to_matplotlib()
)
axes[1].axis("off")
axes[1].set_title("Glasbey")

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
#   Let's make it more obvious, do the same using this new mask.
# </div>
# <div style="
#   background: #e8f7ec;
#   border-left: 6px solid #2f9e44;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #1f5f2c;
# ">
#   <strong style="color: #1f5f2c;">Question</strong><br>
#   How can we separate the objects?
# </div>

# %%
fused_mask = morphology.dilation(binary_mask, morphology.disk(3))

# --- Exercise
from cmap import Colormap

fig, axes = plt.subplots(1, 2, figsize=(8, 3.5))
axes[0].imshow(measure.label(fused_mask, connectivity=1))
axes[0].axis("off")
axes[0].set_title("Default color map")
axes[1].imshow(
    measure.label(fused_mask, connectivity=1), cmap=Colormap("glasbey").to_matplotlib()
)
axes[1].axis("off")
axes[1].set_title("Glasbey")

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
#   Checkout the "Watershed segmentation" from scikit-image examples gallery and adapt it for our mask.
# </div>

# %%
# --- Exercise
from skimage.feature import peak_local_max

distance = ndi.distance_transform_edt(fused_mask)
coords = peak_local_max(distance, footprint=np.ones((12, 12)), labels=fused_mask)
mask = np.zeros(distance.shape, dtype=bool)
mask[tuple(coords.T)] = True
markers, _ = ndi.label(mask)
watershed_labels = segmentation.watershed(-distance, markers, mask=fused_mask)

fig, axes = plt.subplots(ncols=3, figsize=(9, 3), sharex=True, sharey=True)
ax = axes.ravel()

ax[0].imshow(fused_mask, cmap=plt.cm.gray)
ax[0].set_title("Overlapping objects")
ax[1].imshow(-distance, cmap=plt.cm.gray)
ax[1].set_title("Distances")
ax[2].imshow(watershed_labels, cmap=Colormap("glasbey").to_matplotlib())
ax[2].set_title("Separated objects")

for a in ax:
    a.set_axis_off()

fig.tight_layout()
# ---

# %% [markdown]
# ## Region properties
#
# Once we have labeled objects, we can perform all sorts of measurements on them. We can use
# the individual masks to quantify the intensity in each nuclei of the raw image, we can
# also measure properties of individual nuclei, such as their ellipticity.
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
#   Checkout the scikit-image "Measure region properties". Without spending too much time
#   trying to understand the example, identify the call to a scikit-image method that
#   returns a set of measurement for each labeled object and apply it on our labels.
#
#   <b>Hint</b>: there are two similar functions, one performs lazy evaluation on demand,
#   the other one can take a set of measurement names and returns all results.
# </div>
# <div style="
#   background: #e8f7ec;
#   border-left: 6px solid #2f9e44;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #1f5f2c;
# ">
#   <strong style="color: #1f5f2c;">Question</strong><br>
#   Can you find in the docs a list of possible measurements?
# </div>

# %%
# --- Select the final labels from the previous section
labels = watershed_labels
raw_image = image_cells[30, 1]

# --- Exercise
props = measure.regionprops_table(
    labels,
    intensity_image=raw_image,
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
print(df.head())
# ---

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
#   We will see in a coming module how to process and visualize such results.
# </div>
#

# %% [markdown]
# ## Going further
#
# Image analysis is a rich field and there is never one-size-fits-all solution. Knowing where to find resources and helps to perform your analysis is paramount. Here is a selection:
#
# - Pete Bankhead's [BioImage Analysis Book](https://bioimagebook.github.io/index.html)
# - [image.sc forum](image.sc): the bioimage analysis community is fantastic and eager to help you!

# %% [markdown]
# ## Summary
#
# In this module, we touched on many classical image analysis operations (image inspection,
# filtering, thresholding, morphological, etc.). These are not independent operations, but
# they are usually stacked in a pipeline, and the nature and number of steps depend on the
# analysis' need. Once again, it is more valuable to have a general idea of what's possible
# and to know where to find the answer in scikit-image docs, that to know it by heart.
#

# %% [markdown]
#
