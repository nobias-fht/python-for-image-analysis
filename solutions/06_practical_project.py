# %% [markdown]
# # Module 6: Practical project
#
# Time: 2 hours.
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
#   In this project, we are confronted to a real-world image analysis problem. We have data
#   acquired by a collaborator who wants to know the distribution of intensity in the nucleus
#   of their nucleosome target.
#
#   How will you go about to obtain the desired analysis?
# </div>

# %%
# --- Exercise
# Write down the various steps as a comment
# 1 - Inspect images (plot, histogram)
# 2 - Remove background <-- prob not
# 3 - Threshold
# 4 - Morphological operations
# 5 - Watershed
# 6 - Quantification
# 7 - Plot results
# ---

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import ndimage as ndi
from skimage import filters, measure, morphology, segmentation, feature
from tifffile import imread
from cmap import Colormap

# %%
files = list(Path("../data/practical_project/noisy").glob("*.tif"))
images = [imread(f) for f in files]
for img in images:
    print(f"Image size: {img.shape}")

# %%
fig, axes = plt.subplots(
    len(images),
    3,
    figsize=(8, 16),
    gridspec_kw={"width_ratios": [1.4, 1.4, 1]},
    constrained_layout=True,
)

for i in range(len(images)):
    axes[i, 0].imshow(images[i][0])
    axes[i, 0].set_title("Channel 0")
    axes[i, 0].axis("off")

    axes[i, 1].imshow(images[i][1])
    axes[i, 1].set_title("Channel 1")
    axes[i, 1].axis("off")

    axes[i, 2].hist(images[i][0].ravel(), bins=64, alpha=0.5)
    axes[i, 2].hist(images[i][1].ravel(), bins=64, alpha=0.5)
    axes[i, 2].set_title("Histogram")

# %% [markdown]
# <div style="
#   background: #fdecec;
#   border-left: 6px solid #d64545;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #7f1d1d;
# ">
#   <strong style="color: #7f1d1d;">Warning</strong><br>
#   Make bg more bg and not flatfield? alternatively, make it a flat
# field (multiply).
# </div>

# %%
# Background removal with white hat filtering
fig, axes = plt.subplots(len(images), 3, figsize=(6, 12))

images_ch0_no_bg = []
for i, img in enumerate(images):
    img_slice = images[i][0]

    slice_no_bg = morphology.white_tophat(img_slice, footprint=morphology.disk(16))
    bg = img_slice - slice_no_bg

    images_ch0_no_bg.append(slice_no_bg)

    axes[i, 0].imshow(img_slice)
    axes[i, 0].set_title("Image")
    axes[i, 0].axis("off")
    axes[i, 1].imshow(bg)
    axes[i, 1].set_title("Background")
    axes[i, 1].axis("off")
    axes[i, 2].imshow(slice_no_bg)
    axes[i, 2].set_title("Result")
    axes[i, 2].axis("off")

plt.tight_layout()

# %%
# Otsu thresholding
fig, axes = plt.subplots(len(images), 3, figsize=(6, 12))

masks_ch0 = []
for i, img in enumerate(images_ch0_no_bg):

    mask = img > filters.threshold_otsu(img)

    gauss_filt = filters.gaussian(img, sigma=5)
    mask_gauss = gauss_filt > filters.threshold_otsu(gauss_filt)

    masks_ch0.append(mask_gauss)

    axes[i, 0].imshow(img)
    axes[i, 0].set_title("Image - no BG")
    axes[i, 0].axis("off")
    axes[i, 1].imshow(mask)
    axes[i, 1].set_title("Otsu")
    axes[i, 1].axis("off")
    axes[i, 2].imshow(mask_gauss)
    axes[i, 2].set_title("Gauss + Otsu")
    axes[i, 2].axis("off")

plt.tight_layout()

# %%
# Morphology
fig, axes = plt.subplots(len(images), 4, figsize=(8, 12))

final_masks_ch0 = []
for i, raw_mask in enumerate(masks_ch0):

    remove_obj = morphology.remove_small_objects(raw_mask, max_size=150)
    remove_holes = morphology.remove_small_holes(
        remove_obj, max_size=150, connectivity=2
    )
    final_mask = morphology.opening(remove_holes, footprint=morphology.disk(11))

    final_masks_ch0.append(final_mask)

    lst_images = [
        ("Original mask", raw_mask),
        ("Remove objects", remove_obj),
        ("Remove holes", remove_holes),
        ("Opened", final_mask),
    ]

    for idx, (title, img_idx) in enumerate(lst_images):
        axes[i, idx].imshow(img_idx)
        axes[i, idx].set_title(title)
        axes[i, idx].axis("off")

plt.tight_layout()

# %%
# Watershed for labeling
fig, axes = plt.subplots(len(images), 4, figsize=(6, 12))

labels = []
for i, orig_mask in enumerate(final_masks_ch0):

    distance = ndi.distance_transform_edt(orig_mask)
    coords = feature.peak_local_max(
        distance, min_distance=25, footprint=np.ones((12, 12)), labels=orig_mask
    )
    mask = np.zeros(distance.shape, dtype=bool)
    mask[tuple(coords.T)] = True
    markers, _ = ndi.label(mask)
    watershed_labels = segmentation.watershed(-distance, markers, mask=orig_mask)

    labels.append(watershed_labels)

    axes[i, 0].imshow(orig_mask)
    axes[i, 0].set_title("Mask")

    axes[i, 1].imshow(-distance, cmap=plt.cm.gray)
    axes[i, 1].set_title("Distances")

    axes[i, 2].imshow(orig_mask)
    axes[i, 2].set_title("Seeds")
    axes[i, 2].scatter(coords[:, 1], coords[:, 0], c="red", s=3)

    axes[i, 3].imshow(watershed_labels, cmap=Colormap("glasbey").to_matplotlib())
    axes[i, 3].set_title("Labels")

    for a in axes.ravel():
        a.set_axis_off()

fig.tight_layout()

# %%
# Quantification
intensity = []
for i, img in enumerate(images):
    lbl = labels[i]
    idx = np.unique(lbl)

    for val in idx:
        intensity.append(img[1][lbl == val].sum())

plt.hist(intensity, bins=30, color="steelblue", edgecolor="black")
plt.xlabel("Value")
plt.ylabel("Count")
plt.title("Distribution")
plt.show()
