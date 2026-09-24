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
# Time: 10 mins
#
# Scikit-image also has a fantastic [gallery of examples](https://scikit-image.org/docs/stable/auto_examples/index.html).
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
#
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
#
#   A colleague of yours told you to apply a Gaussian filter. Can you find in scikit-image docs the API for the Gaussian filter and import the function here?
# </div>

# %%
# Import the Gaussian filter method from scikit-image
# --- Exercise
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
#
# Time: 10 minutes

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
#
#   Print the shape of the image?
# </div>

# %%
image_cells = data.cells3d()

# Print the image shape
# --- Exercise
print(f"Image shape: {image_cells.shape}")
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
#
#   Plot the histogram of the image using the method `.hist` on the right pane.
#
#   <b>Tip</b>: Don't try to plot the histogram of a 2D image, it will try to make a histogram for each row in the image!
#   We can linearize the image using `img_slice.ravel()`.
# </div>

# %%
# Choose which slice of the image you want to inspect
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

# Plot the histogram
# --- Exercise
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
#
#   We will re-use this code for different images, so let's make it a function.
#
#   <b>Tip</b>: it is important to make sure you are using the function's parameters and
#   not variable defined in your notebook, otherwise you will get strange results. It is a
#   good habit to use different variable names in your functions.
# </div>


# %%
def plot_histogram(array: np.ndarray, label: str = ""):
    # Add the function body for plotting histograms alongside images
    # --- Exercise
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
    axes[1].set_title(f"Histogram {label}")

    plt.show()
    # ---


# %% [markdown]
# ## 3 - Image filters
#
# Time: 20 minutes
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
# There are many reason to use an image filter: it can help smooth an image before segmentation, it can highlights particular features (e.g. edges), etc. Filtering changes pixel values, therefore they should be applied with reason depending on the analysis need, and filtered image should not be used for intensity quantification. But they can be used to help downstream analysis separate region for later intensity quantification on the original image.
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
#
#   Apply the Gaussian filter to a slice of our image. Display the result next to the original image.
#
#   <details>
#   <summary>
#   <strong>Hint</strong>
#   </summary>
#
#   We already imported it, but we also imported the "filters" module from scikit-image.
#   </details>
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
#
#   What does a Gaussian filter do?
# </div>

# %%
# Select the slice
img_slice = image_cells[30, 1]

# Apply the Gaussian filter and show the original and result next to each other.
# --- Exercise
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
#
#   Do the same for the median filter. What does it do?
# </div>

# %%
# Select the slice
img_slice = image_cells[30, 1]

# Apply the median filter and show the original and result next to each other.
# --- Exercise
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
#
#   Let's try again the median filter, but this time let's pretend our image has a lot of hot pixels.
# </div>

# %%
from skimage.util import random_noise

# Select the slice
img_slice = image_cells[30, 1]

# We add noise for the purpose of the exercise
img_slice = random_noise(img_slice, mode="s&p", amount=0.05)

# Apply the median filter and plot the result, use the same code as previously
# --- Exercise
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
#
#   Last filter: the famous Sobel. What does it do?
# </div>

# %%
# Select the slice
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
#
#  Let's try it on another image.
# </div>

# %%
# Select a crop from the human mitosis example data
mito_data = data.human_mitosis()[:200, :200]

# Apply the Sobel filter to the data. Show the original and result next to each other.
# --- Exercise
slice_sobel = filters.sobel(mito_data)

fig, axes = plt.subplots(1, 2, figsize=(8, 3.5))
axes[0].imshow(mito_data)
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
#
#   Explore more filters from scikit-image.
# </div>

# %%
# Try out other filters
# --- Exercise
# ---

# %% [markdown]
# ### Conclusion
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
# Time: 30 minutes
#
# In this context, when we talk about "background" we mean unwanted variation in an image.
#
# There are many ways to deal with background, and they are all specific to the type of
# background you are battling with. The first thing is to be aware that not all that is
# perceived as background is true background, and understanding the source(s) of the
# image degradation is crucial to know what recipe to apply.
#
# We might want to apply a background correction so that we can complete downstream tasks such as thresholding and segmenting our cells.
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
#
#   Let's investigate a few degraded images. How can we investigate what the degradation might be?
#
#   <b>Tip</b>: the first image is the image without degradation, for reference.
#
#   <details>
#   <summary>
#   <strong>Hint</strong>
#   </summary>
#
#   What have we already explored as a way to visualize an image and its intensity distribution?
#   </details>
# </div>

# %%
from python_for_ia import images_with_various_degradations

img_1, img_2, img_3, img_4, img_5 = images_with_various_degradations()

# --- Exercise
plot_histogram(img_1, "Vanilla")
plot_histogram(img_2, "Offset")
plot_histogram(img_3, "Background")
plot_histogram(img_4, "Uneven illumination")
plot_histogram(img_5, "All")
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
#
#   What can be done to correct each of these cases?
# </div>

# %% [markdown]
# ### Types of background
#
# There are two main types of background:
#
# - **Additive background**: There is an unwanted background signal added to our signal of interest. Some example sources might be *camera signal* where there is an electronic offset and dark current present even without illumination, or there might be unwanted fluorescence or out-of-focus fluorescence.
# - **Multiplicative background**: There is an uneven effect across the image which multiplies each pixel by a different value causing unwanted variation. An example of a source of multiplicative background is uneven illumination.
#
# Lots of methods for background correction first require an estimate of the background, then if we have additive background we can subtract it, or if we have multiplicative background we can divide our image by our background estimation. Sometimes for multiplicative background you may here this referred to as a *flat-field correction*.
#
# ### Estimating background
#
# 1. If we have a time series, where the signal is moving but the background is stationary, we may be able to get a background estimate by averaging all the frames together. The background dominates the average and the signal is averaged out.
# 2. We can separate the background from signal when they have different spatial frequencies (background is varying slowly across the image, while signal is changing on the small scale).
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
#
#  Let's see what our image with background looks like. Explore the image.
# </div>
#
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
#   Does this look like additive or multiplicative background?
#
#   <details>
#   <summary>
#   <strong>Hint</strong>
#   </summary>
#
#   Sometimes it can be hard to tell, usually if there is unwanted signal added to some regions of an image, those regions will look brighter, while having lower contrast (i.e. they look "washed-out").
#   </details>
# </div>

# %%
from python_for_ia import image_with_background

img = image_with_background()

# --- Exercise
plot_histogram(img)
# ---

# %% [markdown]
# We want to estimate the background by separating the low spatial frequencies from the high spatial frequencies. One way to do this is by applying a Gaussian filter which blurs out the sharp details.
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
#
#   Now let's apply our Gaussian filter to the image and see what we see, experiment with different `sigma` values. How can we use the Gaussian filter result to correct the background? Plot the results.
#
#   <b>Tip:</b>
#
#   1. We don't want to have negative values in our image, use `np.clip` to set all values below `0` to `0`.
#   2. If we want to retain the average brightness of the image while removing the unwanted variation we can add back the mean of the estimated background image.
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
#
#   How do we know when we have a good estimate for the background?
#
#   <details>
#   <summary>
#   <strong>Hint</strong>
#   </summary>
#
#   Look at the histogram of the corrected image, what do we want to see?
#   </details>
# </div>

# %%
# Apply Gaussian filter and subtract background, plot the results
# --- Exercise
bg_gauss = filters.gaussian(img, sigma=32)
# result_gauss = np.clip(img - bg_gauss, 0, None)
# result_gauss = img/(bg_gauss/bg_gauss.mean())
result_gauss = np.clip(img - bg_gauss + np.mean(bg_gauss), 0, None)

fig, axes = plt.subplots(
    1,
    3,
    figsize=(10, 4),
    gridspec_kw={
        "width_ratios": [1.4, 1.4, 1]
    },  # this is just to make the figure look nicer
    constrained_layout=True,
)

axes[0].imshow(result_gauss)
axes[0].set_title("Result Gauss")
axes[0].axis("off")

axes[1].imshow(bg_gauss)
axes[1].set_title("Background")
axes[1].axis("off")

axes[2].hist(result_gauss.ravel(), bins=50)
axes[2].set_xlabel("Intensity")
axes[2].set_ylabel("Pixel count")
axes[2].set_title("Histogram")
# ---


# %% [markdown]
# Some methods give us a direct result of the background removed image such as the [white top hat](https://scikit-image.org/docs/stable/api/skimage.morphology.html#skimage.morphology.white_tophat) function.
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
#
#   Apply the white top hat function to the image, how can you inspect what the estimated background is? Plot the results.
#
#   <b>Tip: </b> Use `morphology.disk` for the `footprint` argument, experiment with different radii.
# </div>

# %%
# --- Exercise
fig, axes = plt.subplots(
    1,
    3,
    figsize=(10, 4),
    gridspec_kw={
        "width_ratios": [1.4, 1.4, 1]
    },  # this is just to make the figure look nicer
    constrained_layout=True,
)

result_top_hat = morphology.white_tophat(img, footprint=morphology.disk(32))
# bg_top_hat = img - result_top_hat
bg_top_hat = img - result_top_hat

axes[0].imshow(result_top_hat)
axes[0].set_title("Result Top hat")
axes[0].axis("off")

axes[1].imshow(bg_top_hat)
axes[1].set_title("Background")
axes[1].axis("off")

axes[2].hist(result_top_hat.ravel(), bins=50)
axes[2].set_xlabel("Intensity")
axes[2].set_ylabel("Pixel count")
axes[2].set_title("Histogram")
# ---

# %% [markdown]
# Another way to estimate the low frequency background is by applying a low pass filter, such as the low-pass variation of the butterworth filter.
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
#
#   Check out the [butterworth filter](https://scikit-image.org/docs/stable/auto_examples/filters/plot_butterworth.html) example on skimage and use it to get an estimate of the background.
#
#   <b>Tip: </b> Make sure to use `high_pass=False`.
# </div>

# %%
# --- Exercise
butterworth_bg = filters.butterworth(
    img,
    cutoff_frequency_ratio=0.005,
    high_pass=False,
    squared_butterworth=True,
    npad=32,
)

fig, axes = plt.subplots(
    1,
    3,
    figsize=(10, 4),
    gridspec_kw={
        "width_ratios": [1.4, 1.4, 1]
    },  # this is just to make the figure look nicer
    constrained_layout=True,
)

result_butterworth = np.clip(img - butterworth_bg + np.mean(butterworth_bg), 0, None)

axes[0].imshow(result_butterworth)
axes[0].set_title("Result Top hat")
axes[0].axis("off")

axes[1].imshow(butterworth_bg)
axes[1].set_title("Background")
axes[1].axis("off")

axes[2].hist(result_butterworth.ravel(), bins=50)
axes[2].set_xlabel("Intensity")
axes[2].set_ylabel("Pixel count")
axes[2].set_title("Histogram")
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
#
#   Check out the rolling-ball algorithm from scikit-image example gallery.
# </div>

# %%
# --- Exercise
import skimage
from python_for_ia import image_with_background

image = image_with_background()
background = skimage.restoration.rolling_ball(image, radius=30)
result = np.clip(image - background + np.mean(background), 0, None)

fig, axes = plt.subplots(1, 3, figsize=(8, 6))
axes[0].imshow(image)
axes[0].set_title("Original")
axes[0].axis("off")
axes[1].imshow(background)
axes[1].set_title("Background")
axes[1].axis("off")
axes[2].imshow(result)
axes[2].set_title("Result")
axes[2].axis("off")

plt.tight_layout()
# ---

# %% [markdown]
# ## 5 - Thresholding
#
# Time: 20 minutes
#
# A threshold turns an intensity image into a binary mask (foreground/background) by separating pixels above and below a particular intensity.
# Often the areas of an image we are interested in are the bright regions, particularly in fluorescence microscopy.
# Thresholding allows us to easily select these regions to then complete further analysis.
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
#
#   Perform a manual threshold on the image, and visualize the image, the mask and an
#   overlay of the two next to each other. Find the best threshold!
#
#   <b>Tip: </b> Remember the module on manipulating numpy arrays and on plotting.
#
#   <details>
#   <summary>
#   <strong>Hint</strong>
#   </summary>
#
#   Try looking at the histogram of the image to find a good threshold.
#   </details>
# </div>

# %%
# The image to find a threshold for
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
#
#   Let's try an automatic threshold. Have you heard of Otsu method? Find it in the [filters module doc](https://scikit-image.org/docs/stable/api/skimage.filters.html) and apply it to the image.
# </div>

# %%
# The image to find a threshold for
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
#
#   Now try applying Otsu thresholding to the image with background.
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
#
#   Why does this not work so well?
# </div>

# %%
# The image to find a threshold for
img_slice_bg = image_with_background()

# Threshold the image using Otsu's threshold and plot it as an overlay
# --- Exercise
mask_otsu = img_slice_bg > filters.threshold_otsu(img_slice_bg)

fig, axes = plt.subplots(1, 3, figsize=(8, 3.5))
axes[0].imshow(img_slice_bg)
axes[0].set_title("Image")
axes[0].axis("off")
axes[1].imshow(mask_otsu)
axes[1].set_title("Mask (Otsu)")
axes[1].axis("off")
axes[2].imshow(img_slice_bg)
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
#
#   One of the main issue with simple thresholding is that it is global and not region
#   dependent. Search scikit-image <a href="https://scikit-image.org/docs/stable/api/skimage.filters.html">filters module docs</a>
#   for a potentially better solution to find a threshold for the image with background.
#
#   <b>Tip: </b>Use a different name for the mask variable so we can plot it again.
# </div>

# %%
# The image to find a threshold for
img_slice_bg = image_with_background()

# Try a different thresholding method that might work better on the image with bg
# --- Exercise
mask_local = img_slice_bg > filters.threshold_local(
    img_slice_bg, block_size=127  # , offset=-0.02
)

fig, axes = plt.subplots(1, 3, figsize=(8, 3.5))
axes[0].imshow(img_slice_bg)
axes[0].set_title("Image")
axes[0].axis("off")
axes[1].imshow(mask_local)
axes[1].set_title("Mask (Local)")
axes[1].axis("off")
axes[2].imshow(img_slice_bg)
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
#
#   Plot the two masks for the image with background next to each other (the Otsu mask and your chosen thresholding technique).
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
#
#   Do you think the result could be better if we correct for the background first?
# </div>

# %%
# --- Exercise
fig, axes = plt.subplots(1, 2, figsize=(8, 4))
axes[0].imshow(mask_otsu)
axes[0].set_title("Otsu")
axes[0].axis("off")
axes[1].imshow(mask_local)
axes[1].set_title("Local")
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
#
#   How does Otsu's thresholding work? Read about the theory: https://en.wikipedia.org/wiki/Otsu%27s_method.
# </div>

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
#   What could we do to improve the masks?
# </div>

# %% [markdown]
# ## 6 - Morphological operations
#
# Time: 20 minutes
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
#
#   Scikit-image often uses a `footprint` as kernel for the morphological operations. Check out
#   <a href="https://scikit-image.org/docs/stable/auto_examples/numpy_operations/plot_structuring_elements.html">this page</a>
#   for some examples.
#
#   We already used the `morphology.disk` footprint for the white top hat function.
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
#
#   Go to the docs page of `skimage.morphology` and browse the various operations.
#
#   Try applying two or three of them to the mask `raw_mask` below.
#   The aim is to improve the mask so we can better select the cells.
#
#   Show the results of each operation side by side in a plot.
#
#   <b>Tip</b>: You can chain the operations by applying one after the other.
# </div>

# %%
# Recreate the manual mask for demonstration
img_slice = image_cells[30, 1]
threshold = 8_000
raw_mask = img_slice > threshold

# Apply morphological operations to the mask to clean it up
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
# The most useful operations for cleaning up masks are:
#
#   - `erosion`
#   - `dilation`
#   - `closing`
#   - `opening`
#   - `remove_small_objects`
#   - `remove_small_holes`
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
#
#   If in the last exercise you did not use these operations, try using them now to improve the mask.
#
#   <details>
#   <summary>
#   <strong>Hint</strong>
#   </summary>
#
#   Think about the order of operations, what should we do first?
#   </details>
# </div>

# %%
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
# ## 7 - Instance labels
#
# Time: 30 minutes
#
# Often, it will be interesting to have more than a binary mask: all individual instances
# of a type of object. Instances of an object are represented by unique labels identifying
# each object, e.g. nuclei. This way we can do per instance analysis to discover how particular features vary over given populations of instances.
#
# The nuclei in the final mask of the previous section seem easy to separate.
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
#
#   Use `measure.label` to get instances.
#   Plot the resulting labels and the labels overlaid over the original image.
#
#   <b>Tip: </b>When creating the overlay, try setting the `alpha` parameter in `plt.imshow` to an array where the background pixels are `0`. This will make the background pixels transparent.
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
#
#   `measure.label` finds *connected components* in the binary image, all pixels that are touching each other are considered part of the same instance.
#
#   Can you think of any situations where we might not get the instances that we want?
# </div>

# %%
from cmap import Colormap  # A color map library with lots of useful color maps

# Try using this colormap when plotting labels (do plt.imshow(..., cmap=glasbey_cmap))
glasbey_cmap = Colormap("glasbey").to_matplotlib()

# Select the mask from the previous section
binary_mask = final_mask

# Get instance labels from your mask, display the labels and a label overlay.
# --- Exercise
labels = measure.label(binary_mask)

fig, axes = plt.subplots(1, 2, figsize=(8, 3.5))
axes[0].imshow(labels, cmap=glasbey_cmap)
axes[0].axis("off")
axes[0].set_title("Labels")
axes[1].imshow(img_slice, "gray")
axes[1].imshow(labels, cmap=glasbey_cmap, alpha=(labels != 0) * 0.5)
axes[1].axis("off")
axes[1].set_title("Overlay")

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
#
#   What happens when our objects of interest are touching each other?
#
#   Use the `measure.label` function on the example mask `fused_mask` below. Display the binary mask and the labels.
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
#
#   How can we separate the objects?
# </div>

# %%
# Create a mask with touching objects for demonstration purposes
img_slice = image_cells[30, 1]
threshold = 8_000
raw_mask = img_slice > threshold
remove_obj = morphology.remove_small_objects(raw_mask, max_size=40)
closed = morphology.closing(remove_obj, footprint=morphology.disk(1))
remove_holes = morphology.remove_small_holes(closed, max_size=100, connectivity=2)
opened = morphology.opening(remove_holes, footprint=morphology.disk(15))

# Find the connected components of this mask
fused_mask = morphology.dilation(opened, morphology.disk(3))

# Get the labels and display the result
# --- Exercise
labels = measure.label(fused_mask)

fig, axes = plt.subplots(1, 2, figsize=(8, 3.5))

axes[0].imshow(fused_mask)
axes[0].axis("off")
axes[0].set_title("Binary mask")
axes[1].imshow(labels, cmap=glasbey_cmap)
axes[1].axis("off")
axes[1].set_title("Labels")

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
#
#   Checkout the "Watershed segmentation" from scikit-image examples gallery and adapt it for our mask, `fused_mask`.
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
# ## 8 - Region properties
#
# Time: 5 minutes
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
#   Checkout the scikit-image "Measure region properties" example. Without spending too much time
#   trying to understand the example, identify the call to a scikit-image method that
#   returns a set of measurement for each labeled object and apply it on our labels.
#
#   <b>Tip</b>: there are two similar functions, one performs lazy evaluation on demand,
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
#
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
# and to know where to find the answer in scikit-image docs, than to know it by heart.
#
