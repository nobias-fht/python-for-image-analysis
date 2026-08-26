# %% [markdown]
# # Module 2: working with bio-images
#
# Time: 1 hour 45 minutes.
#
# Essential ideas: microscopy images are arrays with axes, data types, and
# metadata. Good image analysis starts with knowing which axis is which, using
# safe numeric types, and replacing slow pixel loops with clear NumPy operations.

# %%
import time

import matplotlib.pyplot as plt
import numpy as np

from src.python_for_ia import make_blobs


def describe(name: str, array: np.ndarray) -> None:
    print(
        f"{name}: shape={array.shape}, dtype={array.dtype}, "
        f"min={array.min():.3f}, max={array.max():.3f}"
    )


# %% [markdown]
# ## Axis order: name axes before slicing
#
# In bio-image analysis you will often see arrays like:
#
# - `YX`: one 2D image,
# - `ZYX`: one 3D volume,
# - `TYX`: time series,
# - `CYX`: multichannel image,
# - `TCZYX`: time, channel, z, y, x.
#
# Pitfall: NumPy does not know axis names. It only sees positions. Keep a note
# of the axis order next to the array, or use libraries that preserve dimension
# metadata when that matters.

# %%
base_yx = make_blobs(shape=(96, 128), seed=1)

# Build a synthetic 5D array in TCZYX order.
time_points = []
for t in range(4):
    z_planes = []
    for z in range(3):
        channel_a = np.clip(base_yx + t * 0.03 + z * 0.02, 0, 1)
        channel_b = np.clip(1 - base_yx + t * 0.01 + z * 0.03, 0, 1)
        z_planes.append(np.stack([channel_a, channel_b], axis=0))  # C, Y, X
    time_points.append(np.stack(z_planes, axis=1))  # C, Z, Y, X

image_tczyx = np.stack(time_points, axis=0).astype(np.float32)

describe("base_yx", base_yx)
describe("image_tczyx", image_tczyx)
print("Axis order: T, C, Z, Y, X")

# %% [markdown]
# ## Basic and advanced multidimensional slicing
#
# Slicing answers questions such as:
#
# - Which channel do I want?
# - Which time point?
# - Which z-plane?
# - Which crop in y and x?
#
# When to use: slicing is the safest first step when you need a representative
# image for visualization or when processing one channel separately.

# %%
t0_c1_zyx = image_tczyx[0, 1]  # first time point, second channel, all z/y/x
middle_z_yx = image_tczyx[0, 0, 1]  # T=0, C=0, Z=1
crop_yx = image_tczyx[0, 0, 1, 20:70, 30:90]
every_other_pixel = image_tczyx[0, 0, 1, ::2, ::2]

describe("t0_c1_zyx", t0_c1_zyx)
describe("middle_z_yx", middle_z_yx)
describe("crop_yx", crop_yx)
describe("every_other_pixel", every_other_pixel)

# %% [markdown]
# `...` means "fill in the missing axes". It is useful when the number of
# leading dimensions may change.

# %%
last_20_columns = image_tczyx[..., -20:]
center_y_band = image_tczyx[..., 40:56, :]

describe("last_20_columns", last_20_columns)
describe("center_y_band", center_y_band)

# %% [markdown]
# `np.s_` lets you store a slice and reuse it. This is handy when several
# channels or time points must use exactly the same region of interest.

# %%
roi = np.s_[..., 25:75, 40:100]
roi_all_axes = image_tczyx[roi]
roi_channel_a = image_tczyx[:, 0][..., 25:75, 40:100]

describe("roi_all_axes", roi_all_axes)
describe("roi_channel_a", roi_channel_a)

# %% [markdown]
# ## Boolean masks, fancy indexing, and coordinates
#
# Boolean masks select pixels by condition. Fancy indexing selects positions by
# coordinate arrays. Both are powerful, but they can copy data and flatten the
# selected values, so check shapes after using them.

# %%
plane = image_tczyx[0, 0, 1]
bright_mask = plane > np.percentile(plane, 90)
bright_values = plane[bright_mask]

rows = np.array([20, 40, 60])
cols = np.array([30, 50, 70])
sampled_values = plane[rows, cols]

print("bright mask shape:", bright_mask.shape)
print("bright values shape:", bright_values.shape)
print("sampled coordinate values:", sampled_values)

# %% [markdown]
# ## Dtype, overflow, and safe arithmetic
#
# Integer images are common because cameras store limited bit depths efficiently.
# Operations on integer arrays can overflow or clip if you are not careful.
#
# Rule of thumb:
#
# - inspect dtype before processing,
# - convert to float for most filtering/normalization,
# - convert back only when saving or when a library requires it.

# %%
uint8_values = np.array([250, 251, 252], dtype=np.uint8)
print("uint8 + 10:", uint8_values + 10)
print("safe add:", uint8_values.astype(np.uint16) + 10)

uint16_like = (plane * 4095).astype(np.uint16)
float_plane = uint16_like.astype(np.float32) / np.iinfo(np.uint16).max

describe("uint16_like", uint16_like)
describe("float_plane", float_plane)

# %% [markdown]
# ## Useful NumPy operations for image analysis
#
# These operations appear constantly in real workflows:
#
# - `mean` and `std` along selected axes,
# - `max` projections for quick volume inspection,
# - `reshape`, `ravel`, and `flatten` for tabular summaries,
# - `clip`, `where`, and broadcasting for conditional operations.

# %%
# Mean intensity per time point and channel, averaging over Z/Y/X.
mean_tc = image_tczyx.mean(axis=(2, 3, 4))
std_tc = image_tczyx.std(axis=(2, 3, 4))
print("mean_tc shape:", mean_tc.shape)
print(mean_tc)
print("std_tc shape:", std_tc.shape)

# Max projection over Z gives a TCYX array.
max_projection_tcyx = image_tczyx.max(axis=2)
describe("max_projection_tcyx", max_projection_tcyx)

# Flattening for histograms and summaries.
values_view = plane.ravel()
values_copy = plane.flatten()
print("ravel shape:", values_view.shape)
print("flatten shape:", values_copy.shape)

# Reshape each 2D plane into rows of pixels: T*C*Z planes by Y*X pixels.
planes_by_pixels = image_tczyx.reshape(
    -1, image_tczyx.shape[-2] * image_tczyx.shape[-1]
)
print("planes_by_pixels:", planes_by_pixels.shape)

# %% [markdown]
# `ravel` often returns a view when possible; `flatten` always returns a copy.
# That difference matters for memory when images are large.

# %%
low, high = np.percentile(plane, (1, 99))
normalized = np.clip((plane - low) / (high - low), 0, 1)
thresholded_display = np.where(plane > 0.5, plane, 0)

fig, axes = plt.subplots(1, 3, figsize=(9, 3))
for ax, img, title in zip(
    axes,
    [plane, normalized, thresholded_display],
    ["raw plane", "percentile normalized", "values below threshold set to 0"],
):
    ax.imshow(img, cmap="gray")
    ax.set_title(title)
    ax.axis("off")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Broadcasting
#
# Broadcasting lets NumPy combine arrays with compatible shapes. It is useful
# for channel normalization, background correction, and per-frame scaling.
#
# Pitfall: broadcasting that "works" can still use the wrong axis if you place
# singleton dimensions in the wrong position.

# %%
channel_scale = np.array([1.0, 0.7], dtype=np.float32)
scaled = image_tczyx * channel_scale[None, :, None, None, None]
describe("scaled", scaled)

background_per_tcz = np.median(image_tczyx, axis=(3, 4), keepdims=True)
background_corrected = image_tczyx - background_per_tcz
describe("background_corrected", background_corrected)

# %% [markdown]
# ## Vectorization vs loops
#
# Loops are not forbidden, but pixel-by-pixel loops are usually slow and noisy
# to read. Prefer vectorized operations unless the algorithm truly needs state
# that changes one pixel at a time.

# %%
large = make_blobs(shape=(512, 512), seed=4)

start = time.perf_counter()
loop_result = np.zeros_like(large)
for row in range(large.shape[0]):
    for col in range(large.shape[1]):
        loop_result[row, col] = large[row, col] * 2 + 0.1
loop_seconds = time.perf_counter() - start

start = time.perf_counter()
vector_result = large * 2 + 0.1
vector_seconds = time.perf_counter() - start

print(f"loop: {loop_seconds:.3f} s")
print(f"vectorized: {vector_seconds:.6f} s")
print("same result:", np.allclose(loop_result, vector_result))

# %% [markdown]
# ## Optional exercises
#
# 1. Extract channel 0, time point 2, all z-planes, and a centered 40 x 40 crop.
# 2. Compute the mean intensity per z-plane for time point 0 and channel 0.
# 3. Make a max projection over z for channel 1 at all time points.
# 4. Normalize each channel independently using its own 1st and 99th percentile.
# 5. Convert a 2D plane into a table with columns `y`, `x`, and `intensity`.

# %%
# Answer sketch (optional, removable)
center_y, center_x = np.array(image_tczyx.shape[-2:]) // 2
crop = image_tczyx[
    2, 0, :, center_y - 20 : center_y + 20, center_x - 20 : center_x + 20
]
describe("exercise crop", crop)

mean_per_z = image_tczyx[0, 0].mean(axis=(1, 2))
print("mean per z:", mean_per_z)

channel_1_projection = image_tczyx[:, 1].max(axis=1)
describe("channel_1_projection", channel_1_projection)

percentiles = np.percentile(image_tczyx, (1, 99), axis=(0, 2, 3, 4), keepdims=True)
channel_normalized = np.clip(
    (image_tczyx - percentiles[0]) / (percentiles[1] - percentiles[0]), 0, 1
)
describe("channel_normalized", channel_normalized)

y_coords, x_coords = np.indices(plane.shape)
pixel_table = np.column_stack([y_coords.ravel(), x_coords.ravel(), plane.ravel()])
print(pixel_table[:5])
