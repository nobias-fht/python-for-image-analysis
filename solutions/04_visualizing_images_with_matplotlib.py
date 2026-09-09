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
# ## 2 - Inspecting an image
#
# Let's start simple and just explore one image.

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
#
#   Can you show a slice of the image using `plt.imshow` and guess the axes?
# </div>

# %%
# --- Exercise
# Show the image
plt.imshow(image_cells[30, 0])
plt.show()
# ---

# %% [markdown]
# Part of visualizing data involves also choosing colormaps and contrast ranges that allow
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
#   <b>Hint</b>: what are the maximum values in the slice you are interested in?
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
#   What is the default contrast behaviour of `plt.imshow`?
# </div>

# %%
image_slice = image_cells[30, 0]

# --- Exercise
# get vmin, vmax
vmin, vmax = image_slice.min(), image_slice.max()
print(f"vmin: {vmin}, vmax: {vmax}")

# Show the image
plt.imshow(image_slice, vmin=1_500, vmax=20_000)
plt.show()
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
#   Let's change the color map using `cmap`.
#
#   <b>Hint</b>: Can you list the colormaps?
# </div>

# %%
image_slice = image_cells[30, 0]

# --- Exercise
# list colormaps
from matplotlib import colormaps

print(f"List of colormaps: {list(colormaps)}")

# Show the image
plt.imshow(image_slice, cmap="twilight")
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
#   We often omit `plt.show()` because Jupyter notebooks are interactive envrionment that
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
image_slice = image_cells[30, 0]

# --- Exercise
plt.imshow(image_slice, cmap="gray")
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
#   What's a good usecase for overlays?
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
#   <b>Hint</b>: Use the `gray` and `inferno` colormaps, and play on the contrast.
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
#   What is wrong with this two-channels image?
#
#   <b>Hint</b>: the answer might be clear from knowing who cannot see this image "correctly".
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
image_slice = image_cells[30, 1]
labels = image_slice > 25_000

fig, ax = plt.subplots()

# --- Exercise
ax.imshow(image_slice, cmap="gray")
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
image_slice = image_cells[30, 1]

# --- Exercise
plt.hist(image_slice.ravel(), bins=256)
plt.xlabel("Pixel intensity")
plt.ylabel("Pixel count")
# ---

plt.title("Image histogram")
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
