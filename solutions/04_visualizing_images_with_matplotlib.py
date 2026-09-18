# %% [markdown]
# # Module 4: visualizing images
#
# Time: 1 hour.
#
# When working with images, the most important step is to visualize them efficiently and
# accurately. Working blind on images will always lead to errors.
#
# ### Question
#
# How can we visualize images in Python?
#
# ### Objective
#
# - Learn to navigate matplotlib
# - Learn what is possible to do

# %% [markdown]
# ## 1 - Navigate `matplotlib`
#
#
# Matplotlib has a fantastic [gallery of examples](https://matplotlib.org/stable/gallery/index.html).
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
#   A colleague of yours told you that your experimental images would be easier to interpret
#   if channels were plotted next to each other. They told you to use subplots. Can you find
#   how to plot two plots next to each other?
# </div>

# %%
# --- Exercise
import matplotlib.pyplot as plt
import numpy as np

# Create some fake data.
x1 = np.linspace(0.0, 5.0)
y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
x2 = np.linspace(0.0, 2.0)
y2 = np.cos(2 * np.pi * x2)

plt.subplot(2, 1, 1)
plt.plot(x1, y1, "o-")
plt.title("A tale of 2 subplots")
plt.ylabel("Damped oscillation")

plt.subplot(2, 1, 2)
plt.plot(x2, y2, ".-")
plt.xlabel("time (s)")
plt.ylabel("Undamped")

plt.show()
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
#   Can you find the `subplot` API in matplotlib docs? What parameters does it accept?
# </div>

# %% [markdown]
# ## 2 - Color maps
#
# Color maps help us to visually interpret image data by showing us what value a pixel has.
# Different types of color maps have different use-cases.
# Matplotlib provides access to many color maps, take a look matplotlib's [color map reference](https://matplotlib.org/stable/gallery/color/colormap_reference.html).
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
#   Matplotlib's color map reference splits the color maps into different categories, how do you think the use cases for <em>Sequential</em>, <em>Diverging</em> and <em>Cyclic</em> color maps differ?
# </div>

# %%
# --- Import what we need
import matplotlib.pyplot as plt
import numpy as np
from skimage import data

# %% [markdown]
# Scikit-image (which we will explore in the next module) comes with [example data](https://scikit-image.org/docs/stable/api/skimage.data.html), let's download `cells3d` and inspect the image.
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

# Print the image shape
# --- Exercise
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
#
#   Use `plt.imshow` to show the the membrane slice, use `plt.colorbar` to show which intensity values the color map corresponds to.
# </div>

# %%
membrane_slice = image_cells[30, 0]

# --- Exercise
# Show the image
plt.imshow(membrane_slice)
plt.colorbar()
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
#   What is matplotlib's default color map?
# </div>

# %% [markdown]
# Part of visualizing data involves also choosing color maps and contrast ranges that allow
# you to correctly visualize the features you are interested in. Sometimes, it is also
# a matter of taste.
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
#   Let's change the contrast using `vmin` and `vmax` values.
#
#   <b>Hint</b>: what are the maximum values in the slice you are interested in? Try using the function `np.percentile` to clip the range.
# </div>
#
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
#   What is the default contrast behavior of `plt.imshow`?
# </div>

# %%
# --- Exercise
lower_percentile = 1
upper_percentile = 99
vmin = np.percentile(membrane_slice, lower_percentile)
vmax = np.percentile(membrane_slice, upper_percentile)

# Show the image
plt.imshow(membrane_slice, vmin=vmin, vmax=vmax)
plt.colorbar()
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
#   How has the range changed on the colorbar?
# </div>

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
#   Let's change the color map using the `cmap` argument. Plot two images side by side: the default color map next to your chosen color map.
#
#   <b>Hint</b>: To use `plt.colorbar` in subplots you have to pass it the "mappable" returned from `plt.imshow` and the correct "axes" to the `ax` argument.
# </div>

# %%
# Use a figsize of (10, 4) - it is an argument to the `subplots` function.
# --- Exercise
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

m1 = axes[0].imshow(membrane_slice, vmin=vmin, vmax=vmax)
plt.colorbar(m1, ax=axes[0])
m2 = axes[1].imshow(membrane_slice, cmap="cool", vmin=vmin, vmax=vmax)
plt.colorbar(m2, ax=axes[1])
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
#   Can a color map change how you interpret the data?
#   Look at the following image, do you think this color map is good or bad at representing the data compared to the default color map?
# </div>

# %%
nuclear_slice = image_cells[30, 1]

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

vmin = 2_600
vmax = 27_000

m = axes[0].imshow(nuclear_slice, vmin=vmin, vmax=vmax)
plt.colorbar(m, ax=axes[0])
axes[0].set_title("viridis")
m = axes[1].imshow(nuclear_slice, cmap="jet", vmin=vmin, vmax=vmax)
plt.colorbar(m, ax=axes[1])
axes[1].set_title("jet")

# %% [markdown]
# ### Diverging color maps
#
# Diverging color maps can be useful when you have positive and negative values.
# Let's use a diverging color map to show how far from the median each pixel is.

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
#   What is wrong with the image displayed below?
#
#   <details>
#   <summary><strong>Hint❓</strong></summary>
#     Think about what we want the central white value in the color map to be.
#   </details>
# </div>

# %%
median = np.median(nuclear_slice)
median_diff = nuclear_slice - median

plt.imshow(median_diff, cmap="bwr")
plt.colorbar()

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
#   Fix the example above so that we can interpret the data correctly.
#
#   <details>
#   <summary><strong>Hint ❓</strong></summary>
#     Choose appropriate values for <code>vmin</code> and <code>vmax</code>.
#   </details>
# </div>

# %%
# --- Exercise
v = np.abs(median_diff).max()
plt.imshow(median_diff, cmap="bwr", vmin=-v, vmax=v)
plt.colorbar()
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
#   `cmap` is a great package for color maps that can be passed directly to matplotlib. [Try it out](https://cmap-docs.readthedocs.io/en/stable/catalog/).
#
#   <b>Hint</b>: e.g. `Colormap("viridis").to_mpl()`
# </div>

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
#   We often omit `plt.show()` because Jupyter notebooks are interactive environment that
#   automatically trigger it. In scripts, you may have to add it.
# </div>
#

# %% [markdown]
# ## 2 - Plot properties
#
# `plt.imshow` is nice for a quick visualization. However, it does alone not allow us to
# change other aspects of the plot, such as title or axes labels.
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
#   Try out `plt.title("my_title")` and `plt.axis("off")`
# </div>
#
#

# %%
membrane_slice = image_cells[30, 0]

# --- Exercise
plt.imshow(membrane_slice, cmap="gray")
plt.title("My image")
plt.axis("off")
plt.show()
# ---

# %% [markdown]
# ## 3 - Overlaying images
#
# When visualizing images, it is often useful to visualize them as overlays: two images
# superimposed.
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
#   What's a good use-case for overlays?
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
#   Create an overlay with the image by using `ax.imshow`.
#
#   <b>Hint</b>: Use the `gray` and `inferno` color maps, and play on the contrast.
# </div>

# %%
fig, ax = plt.subplots()

# --- Exercise
ax.imshow(image_cells[30, 0], cmap="gray", vmin=2_000, vmax=15_000)
ax.imshow(image_cells[30, 1], cmap="inferno", alpha=0.7)
# ---

ax.set_title("Overlay")
ax.axis("off")
plt.show()

# %% [markdown]
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
#   What is wrong with the two-channels image below?
#
#   <b>Hint</b>: think about people who might not be able to see the image "correctly".
# </div>

# %%
fig, ax = plt.subplots()

ax.imshow(image_cells[30, 0], cmap="Reds", vmin=2_000, vmax=15_000)
ax.imshow(image_cells[30, 1], cmap="Greens", alpha=0.7)

ax.axis("off")
plt.show()

# %% [markdown]
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
#   Another use case is overlaying images with labels. Create an overlay with the the `image_slice` and the `labels`.
# </div>

# %%
nuclear_slice = image_cells[30, 1]
labels = nuclear_slice > 25_000

fig, ax = plt.subplots()

# --- Exercise
ax.imshow(nuclear_slice, cmap="gray")
ax.imshow(labels, alpha=0.4)
# ---

ax.set_title("Mask overlay")
ax.axis("off")
plt.show()


# %% [markdown]
# ## 4 - Image histogram
#
# It is always a good idea to start by inspecting the intensity distribution of an image. Histograms are a quick way to see background, foreground, saturation, and
# whether a global threshold might be plausible.
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
#   Plot the histogram of a slice of the image.
#
#   <b>Hint</b>: rather than plotting the histogram of a 2D image, we can linearize the image
#   using "img_slice.ravel()".
# </div>

# %%
nuclear_slice = image_cells[30, 1]

# --- Exercise
plt.hist(nuclear_slice.ravel(), bins=256)
plt.xlabel("Pixel intensity")
plt.ylabel("Pixel count")
# ---

plt.title("Image histogram")
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
titles = ["Original", "Example 1", "Example 2"]

for i, (img, title) in enumerate(zip(img_lst, titles, strict=True)):
    # --- Exercise
    plt.hist(img.ravel(), bins=100)
    # ---

    plt.xlabel("Pixel intensity")
    plt.ylabel("Pixel count")
    plt.title(title)
    plt.show()

# %% [markdown]
# ## 5 - Assembling figures with subplots

# %% [markdown]
# We have already briefly used `subplots`. It is quite powerful as it allows you to generate
# complex figures.
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
#   Let's plot the histogram next to an image using `plt.subplots`, using "hist" on the right pane.
#
# </div>

# %%
img_slice = image_cells[30, 1]

# We create the subplot and show the image in the left-hand panel
fig, axes = plt.subplots(1, 2)  # 1 row x 2 columns

# Access the first panel using `axes[0]`
axes[0].imshow(img_slice)
axes[0].set_title("Image")
axes[0].axis("off")

# Plot the histogram in the second panel
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
#   That does not look pretty. Play with the following parameters that can be passed
#   to the `subplots` function:
#   - `figsize`: tuple
#   - `constrained_layout`: bool
#   - `gridspec_kw{"width_ratios": [1.4, 1]}`
# </div>

# %%
img_slice = image_cells[30, 1]

# --- Exercise
fig, axes = plt.subplots(
    1,
    2,
    figsize=(8, 4),  # size of the figure (hight, width)
    gridspec_kw={  # this is just to make the figure look nicer
        "width_ratios": [1.4, 1]
    },
    constrained_layout=True,
)
# ---

# Access the first panel using `axes[0]`
axes[0].imshow(img_slice)
axes[0].set_title("Image")
axes[0].axis("off")

# Plot the histogram in the second panel
axes[1].hist(img_slice.ravel(), bins=50)
axes[1].set_xlabel("Intensity")
axes[1].set_ylabel("Pixel count")
axes[1].set_title("Histogram")


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
#   What if we have more images and we want more than one row? Plot the same pairs of
#   image and histogram, but this time for each channel, in the same plot.
#
#   <b>Hint</b>: think of how to loop over the figure.
# </div>

# %%
img_slice = image_cells[30]  # we only select the Z slice

# --- Exercise
n_channels = img_slice.shape[0]
fig_size = (8, 4 * n_channels)

fig, axes = plt.subplots(
    n_channels,
    2,
    figsize=fig_size,
    gridspec_kw={"width_ratios": [1.4, 1]},
    constrained_layout=True,
)

for idx in range(n_channels):
    axes[idx, 0].imshow(img_slice[idx])
    axes[idx, 0].set_title(f"Channel {idx}")
    axes[idx, 0].axis("off")

    # Plot the histogram in the second panel
    axes[idx, 1].hist(img_slice[idx].ravel(), bins=50)
    axes[idx, 1].set_xlabel("Intensity")
    axes[idx, 1].set_ylabel("Pixel count")
    axes[idx, 1].set_title("Histogram")
# ---

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
#   Automating your figure creation with scripts is going to save you tons of time in your
#   projects.
# </div>

# %% [markdown]
# ## 6 - Saving figures
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
#   Once you have produced the perfect figure, it is important to save it. No need for
#   screenshots, `matplotlib` has you covered with `plt.savefig`. Save a figure!
# </div>

# %%
img_slice = image_cells[30]  # we only select the Z slice

n_channels = img_slice.shape[0]
fig_size = (8, 4 * n_channels)

fig, axes = plt.subplots(
    n_channels,
    2,
    figsize=fig_size,
    gridspec_kw={"width_ratios": [1.4, 1]},
    constrained_layout=True,
)

for idx in range(n_channels):
    axes[idx, 0].imshow(img_slice[idx])
    axes[idx, 0].set_title(f"Channel {idx}")
    axes[idx, 0].axis("off")

    # Plot the histogram in the second panel
    axes[idx, 1].hist(img_slice[idx].ravel(), bins=50)
    axes[idx, 1].set_xlabel("Intensity")
    axes[idx, 1].set_ylabel("Pixel count")
    axes[idx, 1].set_title("Histogram")

# --- Exercise
plt.savefig("channels_histogram.png")
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
#   What is the best export format for editing your figures for a paper or presentation?
# </div>

# %% [markdown]
# ## Going further
#
# - `matplotlib` [example gallery](https://matplotlib.org/stable/gallery/index.html)
# - There are alternative ways to explore images in python:
#     - other packages, e.g. `seaborn`, `plotnine`
#     - real image viewers, such as `napari`

# %% [markdown]
# ## Summary
#
# In this module, we learned to navigate `matplotlib` docs and perform everyday plotting:
# single images, overlays, and subplots. A large portion of your need are covered with these
# examples, but there is an infinite world of possibilities with `matplotlib`.

# %% [markdown]
# - histograms to investigate images
# - colormaps, not be fooled by the color ranges
# - read the docs
# - automate your figures
