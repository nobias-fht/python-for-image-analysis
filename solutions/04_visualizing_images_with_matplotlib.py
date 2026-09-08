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
# ## Histogram
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
#   Plot histogram
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
# ## X - Subplots

# %% [markdown]
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
#   Let's plot the histogram next to an image using `plt.subplots`, using "hist" on the right pane.
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


# %%

# %%
# simple


# %%
# with loop


# %%
# change layout and sizes

# %% [markdown]
# ## X - Saving figures

# %%
# --- Exercise
plt.savefig()
# ---

# %%
