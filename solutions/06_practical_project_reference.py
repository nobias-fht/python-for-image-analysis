# %% [markdown]
# # Module 6: Practical project
#
# Time: 2 hours.
#
# In this project, we are confronted to a real-world image analysis problem. We have data
# acquired by a collaborator who wants to know the distribution of intensity in the nucleus
# of their nucleosome target.
#
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
#   Let's start by looking more closely at the data.
# </div>

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndi
from bioio import BioImage
from cmap import Colormap
from skimage import feature, filters, morphology, segmentation

from python_for_ia import project_data

# %%
# downloading the data we will work on
data_path = project_data(Path("../data"))

files = list(data_path.glob("*.tif"))
image_files = [BioImage(f) for f in files]
for img_file in image_files:
    print(f"Image size: {img_file.shape}")

images = [img_file.get_image_data().squeeze() for img_file in image_files]

# %%
data_path

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
    axes[i, 2].hist(images[i][1].ravel(), fc="r", bins=64, alpha=0.5)
    axes[i, 2].set_title("Histogram")

# %%
# Background removal with white hat filtering
fig, axes = plt.subplots(len(images), 3, figsize=(6, 12))

images_ch0_no_bg = []
for i, img in enumerate(images):
    img_slice = img[0]

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
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].imshow(img)
axes[1].imshow(gauss_filt)


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

# %% [markdown]
# In the quantification below, instead of using regionprops, we manually select the pixels for each nucleus instance and find the mean of the pixels in the second channel.

# %%
# Quantification
intensity = []
for i, img in enumerate(images):
    lbl = labels[i]  # the matching label image for the image
    # idx = np.unique(lbl) # numpy can find the unique labels in the image
    max_label = lbl.max()

    # loop through all the labels in the label
    # for val in idx:
    for val in range(1, max_label + 1):
        intensity.append(img[1, lbl == val].mean())
intensity = np.array(intensity)

plt.hist(intensity, bins=30, color="steelblue", edgecolor="black")
plt.xlabel("Value")
plt.ylabel("Count")
plt.title("Distribution")


# inspect the histogram also without the top 1 percentile to zoom in on the distribution
intensity_no_outliers = intensity[intensity < np.quantile(intensity, 0.99)]

plt.figure()
plt.hist(intensity_no_outliers, bins=30, color="steelblue", edgecolor="black")
plt.xlabel("Value")
plt.ylabel("Count")
plt.title("Distribution without outliers")

plt.show()
