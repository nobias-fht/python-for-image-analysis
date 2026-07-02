# %% [markdown]
# # Module 6: practical pipeline exercise
#
# Goal: simulate a two-channel image, segment cell instances, classify two
# populations from intensity ratio, and extract ellipticity.

# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import ndimage as ndi
from skimage import color, filters, measure, morphology, segmentation

from course_utils import make_two_channel_cells

# %%
image_yxc, true_labels, _population_id = make_two_channel_cells(seed=21)
channel_a = image_yxc[..., 0]
channel_b = image_yxc[..., 1]
combined = channel_a + channel_b

# %% [markdown]
# ## Segment foreground and split instances

# %%
mask = combined > filters.threshold_otsu(combined)
mask = morphology.remove_small_objects(mask, min_size=80)
mask = morphology.remove_small_holes(mask, area_threshold=80)

distance = ndi.distance_transform_edt(mask)
markers = measure.label(morphology.local_maxima(distance))
labels = segmentation.watershed(-distance, markers, mask=mask)
labels = segmentation.clear_border(labels)

print("objects:", labels.max())

# %% [markdown]
# ## Measure channel intensities and shape

# %%
props_a = measure.regionprops_table(
    labels,
    intensity_image=channel_a,
    properties=("label", "area", "mean_intensity", "major_axis_length", "minor_axis_length"),
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
# ## Visual check

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

df.boxplot(column="ellipticity", by="population")
plt.suptitle("")
plt.ylabel("ellipticity")
plt.show()

# %% [markdown]
# ## Optional exercises
#
# 1. Replace the ratio rule with a threshold based on the median ratio.
# 2. Filter out objects smaller than the 10th percentile area.

# %%
# Answer sketch (optional, removable)
median_ratio = df["ratio_a_over_b"].median()
df["population_median_rule"] = np.where(df["ratio_a_over_b"] >= median_ratio, "high ratio", "low ratio")
area_cutoff = df["area"].quantile(0.10)
df_filtered = df[df["area"] >= area_cutoff]
print(df_filtered.shape)
