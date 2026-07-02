# %% [markdown]
# # Module 2: working with bio-images
#
# Essential ideas: images are NumPy arrays; axis order matters; dtype controls
# range and arithmetic behavior; vectorized operations are usually clearer and
# faster than pixel loops.

# %%
import time

import matplotlib.pyplot as plt
import numpy as np

from course_utils import make_blobs

# %% [markdown]
# ## Dimensionality and axis order

# %%
image_yx = make_blobs(shape=(96, 128), seed=1)
stack_tzyx = np.stack([image_yx + t * 0.02 for t in range(5)], axis=0)
stack_tzyx = stack_tzyx[:, np.newaxis, :, :]  # T, Z, Y, X

print("2D:", image_yx.shape)
print("T-Z-Y-X:", stack_tzyx.shape)
print("First time point, first z plane:", stack_tzyx[0, 0].shape)

# %% [markdown]
# ## Dtype and overflow

# %%
uint8_values = np.array([250, 251, 252], dtype=np.uint8)
print("uint8 + 10:", uint8_values + 10)
print("safe add:", uint8_values.astype(np.uint16) + 10)

float_image = image_yx.astype(np.float32)
print(float_image.dtype, float_image.min(), float_image.max())

# %% [markdown]
# ## Slicing and indexing

# %%
crop = image_yx[20:70, 30:90]
bright_pixels = image_yx > 0.5
print("crop shape:", crop.shape)
print("bright fraction:", bright_pixels.mean())

fig, axes = plt.subplots(1, 3, figsize=(9, 3))
axes[0].imshow(image_yx, cmap="gray")
axes[0].set_title("image")
axes[1].imshow(crop, cmap="gray")
axes[1].set_title("crop")
axes[2].imshow(bright_pixels, cmap="gray")
axes[2].set_title("mask")
for ax in axes:
    ax.axis("off")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Vectorization vs loops

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
# 1. Extract the middle 40 x 40 crop from `image_yx`.
# 2. Normalize `image_yx` to the range 0-1 using vectorized operations.

# %%
# Answer sketch (optional, removable)
cy, cx = np.array(image_yx.shape) // 2
middle_crop = image_yx[cy - 20 : cy + 20, cx - 20 : cx + 20]
normalized = (image_yx - image_yx.min()) / (image_yx.max() - image_yx.min())
print(middle_crop.shape, normalized.min(), normalized.max())
