# %% [markdown]
# # Module 6: practical pipeline exercise
#
# Time: 2 hours.
#
# Goal: simulate a two-channel image, segment cell instances, classify two
# populations from intensity ratio, extract ellipticity, and perform basic QC.
#
# This module intentionally combines previous ideas. It should feel like a
# realistic notebook prototype: not yet polished software, but coherent enough
# to become one.

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import ndimage as ndi
from skimage import color, filters, measure, morphology, segmentation

from course_utils import make_two_channel_cells

# %%
image_yxc, true_labels, true_population_id = make_two_channel_cells(seed=21)
channel_a = image_yxc[..., 0]
channel_b = image_yxc[..., 1]
combined = channel_a + channel_b

print("image:", image_yxc.shape, image_yxc.dtype)
print("true labels:", true_labels.shape, true_labels.max())

# %% [markdown]
# ## Step 1: inspect channels
#
# Before segmentation, check whether both channels have signal and whether one
# channel dominates the combined image. A quick histogram can catch failed
# acquisitions or wrong channel selection.

# %%
fig, axes = plt.subplots(2, 3, figsize=(10, 6))
for ax, img, title in zip(
    axes[0],
    [channel_a, channel_b, combined],
    ["channel A", "channel B", "combined"],
):
    ax.imshow(img, cmap="gray")
    ax.set_title(title)
    ax.axis("off")

axes[1, 0].hist(channel_a.ravel(), bins=60)
axes[1, 0].set_title("A histogram")
axes[1, 1].hist(channel_b.ravel(), bins=60)
axes[1, 1].set_title("B histogram")
axes[1, 2].hist(combined.ravel(), bins=60)
axes[1, 2].set_title("combined histogram")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Step 2: segment foreground and split instances
#
# We use the sum of both channels to segment objects. This is reasonable when
# either population should be detected. If only one marker defines the object
# boundary, use that marker instead.
#
# Pitfall: using a classification channel for segmentation can bias downstream
# intensity ratios. Keep the biological question in mind.

# %%
threshold = filters.threshold_otsu(combined)
mask = combined > threshold
mask = morphology.remove_small_objects(mask, min_size=80)
mask = morphology.remove_small_holes(mask, area_threshold=80)
mask = ndi.binary_fill_holes(mask)

distance = ndi.distance_transform_edt(mask)
markers = measure.label(morphology.local_maxima(distance))
labels = segmentation.watershed(-distance, markers, mask=mask)
labels = segmentation.clear_border(labels)

print("threshold:", threshold)
print("objects:", labels.max())

# %% [markdown]
# ## Step 3: measure channel intensities and shape
#
# Each row in the table is one segmented object. The label column links table
# rows back to pixels in the label image.

# %%
props_a = measure.regionprops_table(
    labels,
    intensity_image=channel_a,
    properties=(
        "label",
        "area",
        "mean_intensity",
        "major_axis_length",
        "minor_axis_length",
    ),
)
props_b = measure.regionprops_table(
    labels,
    intensity_image=channel_b,
    properties=("label", "mean_intensity"),
)

df = pd.DataFrame(props_a).rename(columns={"mean_intensity": "mean_a"})
df["mean_b"] = props_b["mean_intensity"]
df["ratio_a_over_b"] = df["mean_a"] / (df["mean_b"] + 1e-6)
df["population"] = np.where(df["ratio_a_over_b"] >= 1, "A-high", "B-high")
df["ellipticity"] = 1 - df["minor_axis_length"] / df["major_axis_length"]
print(df.head())

# %% [markdown]
# ## Step 4: visual QC
#
# The fastest way to detect many pipeline mistakes is to overlay labels on the
# image and inspect outliers in the measurement table.

# %%
overlay = color.label2rgb(labels, image=combined, bg_label=0, alpha=0.35)

fig, axes = plt.subplots(1, 4, figsize=(12, 3))
for ax, img, title in zip(
    axes,
    [channel_a, channel_b, labels, overlay],
    ["channel A", "channel B", "labels", "overlay"],
):
    ax.imshow(img, cmap="gray" if title != "labels" else "nipy_spectral")
    ax.set_title(title)
    ax.axis("off")
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(8, 3))
df.boxplot(column="ellipticity", by="population", ax=axes[0])
axes[0].set_title("ellipticity")
axes[0].set_ylabel("ellipticity")
axes[1].scatter(df["ratio_a_over_b"], df["ellipticity"], alpha=0.8)
axes[1].set_xlabel("A/B ratio")
axes[1].set_ylabel("ellipticity")
plt.suptitle("")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Step 5: parameter sensitivity
#
# A pipeline is more trustworthy when small parameter changes do not completely
# change the conclusion. Here we quickly compare object counts for different
# minimum sizes.

# %%
for min_size in [40, 80, 160]:
    test_mask = morphology.remove_small_objects(combined > threshold, min_size=min_size)
    test_labels = measure.label(test_mask)
    print(f"min_size={min_size}: {test_labels.max()} objects")

# %% [markdown]
# ## Optional exercises
#
# 1. Replace the ratio rule with a threshold based on the median ratio.
# 2. Filter out objects smaller than the 10th percentile area.
# 3. Add a QC flag for objects with ellipticity greater than 0.8.
# 4. Compare segmentation from `combined` versus `channel_a` only.
# 5. Save the measurement table to `scratch_outputs/module06_measurements.csv`.

# %%
# Answer sketch (optional, removable)
median_ratio = df["ratio_a_over_b"].median()
df["population_median_rule"] = np.where(
    df["ratio_a_over_b"] >= median_ratio, "high ratio", "low ratio"
)

area_cutoff = df["area"].quantile(0.10)
df_filtered = df[df["area"] >= area_cutoff].copy()
df_filtered["qc_flag"] = np.where(df_filtered["ellipticity"] > 0.8, "elongated", "ok")
print(df_filtered.head())

channel_a_mask = channel_a > filters.threshold_otsu(channel_a)
channel_a_mask = morphology.remove_small_objects(channel_a_mask, min_size=80)
print("combined labels:", labels.max())
print("channel A labels:", measure.label(channel_a_mask).max())

output_path = "scratch_outputs/module06_measurements.csv"
Path(output_path).parent.mkdir(parents=True, exist_ok=True)
pd.DataFrame(df_filtered).to_csv(output_path, index=False)
print("saved:", output_path)
