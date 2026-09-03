# %% [markdown]
# # Module 2: working with bioimages
#
# Time: 1 hour 45 minutes.
#
# Bioimages can be represented as multi-dimensional arrays. We will be working with [NumPy](https://numpy.org/doc/stable/index.html), which is the most common package for multi-dimensional array manipulation.

# %%
import time

import matplotlib.pyplot as plt
import numpy as np
import skimage

# %% [markdown]
# ## Intro to NumPy
#
# NumPy is an open source library which is very commonly used in python for handling arrays.
# It provides many useful functions and mathematical operations, most of the underlying code is written in C, making it usually much faster than native python loops.
#
# Here, we will introduce some essential concepts for creating and manipulating NumPy arrays.
#
# Note: We imported the `numpy` library into the notebook at the start using `import numpy as np`.
#
# ### Creating Arrays
#
# There are many ways to create arrays in NumPy, for example:
# 1) From a python list, or list of lists for 2D:

# %%
array_1D = np.array([10, 42, 99, 3])

# NOTE: you can find the shape of an array with the .shape property !
print(f"Array shape: {array_1D.shape}")
print(array_1D)

# %%
array_2D = np.array(
    [
        [10, 42],
        [99, 3],
    ]
)

print(f"Array shape: {array_2D.shape}")
print(array_2D)

# %% [markdown]
# 2) Initialize arrays filled with a single value, some useful functions are:
#
# - `np.zeros`
# - `np.ones`
# - `np.full`
#
# They initialize an array with a given shape, filled with zeros, ones, or a chosen fill value respectively.

# %%
shape = (2, 3, 4)
zeros_array = np.zeros(shape=shape)
ones_array = np.ones(shape=shape)
full_array = np.full(shape=shape, fill_value=100)

print("Array full of zeros:")
print(zeros_array)
print()
print("Array full of ones:")
print(ones_array)
print()
print("Array full with a value:")
print(full_array)

# %% [markdown]
# 3) Other useful functions
#
# - `np.arange`
# - `np.linspace`
# - `np.random.random`

# %% [markdown]
# ### Reshaping

# %%

# %% [markdown]
# ### Indexing and slicing

# %%

# %% [markdown]
# ### Mathematical operations

# %%

# %% [markdown]
# ### Data Types

# %%

# %% [markdown]
# ### Useful array properties
#
# - `ndims`
# - `shape`
# - `size`
# - `dtype`
# - `itemsize`

# %% [markdown]
# ## Working with bio-images
#
# #### Pixels
#
# #### Axes
#
# #### Example data

# %%

# %% [markdown]
# ### Try indexing and slicing

# %%

# %% [markdown]
# ### Manipulating dimensions
#
# - Transposing
# - Squeezing / Adding singleton dims
# - Reshaping

# %%

# %% [markdown]
# ### Projections

# %%

# %% [markdown]
# ### Line profile example

# %%

# %% [markdown]
# ## Watch out!
#
# - Data overflow

# %%

# %% [markdown]
# ## Vectorization versus loops
#
# A Python loop is fine when it expresses a small number of biological objects
# or files. Pixel-by-pixel loops are usually slow and harder to read. NumPy is
# fast because it performs many operations in compiled code.

# %%
large = make_blobs(shape=(512, 512), n_blobs=60, seed=12)

start = time.perf_counter()
loop_result = np.zeros_like(large)
for row in range(large.shape[0]):
    for col in range(large.shape[1]):
        loop_result[row, col] = large[row, col] * 1.5 + 0.2
loop_seconds = time.perf_counter() - start

start = time.perf_counter()
vector_result = large * 1.5 + 0.2
vector_seconds = time.perf_counter() - start

print(f"loop seconds: {loop_seconds:.3f}")
print(f"vectorized seconds: {vector_seconds:.6f}")
print("same values:", np.allclose(loop_result, vector_result))

# %% [markdown]
# Dot products are weighted sums. In image analysis they appear in color
# conversion, linear filters, projections, and many measurement pipelines.

# %%
rgb_pixel = np.array([0.8, 0.3, 0.1])
rgb_to_gray_weights = np.array([0.2126, 0.7152, 0.0722])
gray_value = np.dot(rgb_pixel, rgb_to_gray_weights)

print("RGB pixel:", rgb_pixel)
print("weighted grayscale value:", gray_value)

# %% [markdown]
# An outer product combines two 1D arrays into a 2D pattern. This is a compact
# way to make separable gradients, profiles, or simple simulated illumination
# fields.

# %%
y_profile = np.linspace(0.5, 1.0, 80)
x_profile = np.linspace(1.0, 0.6, 120)
illumination_yx = np.outer(y_profile, x_profile)

print("outer product shape:", illumination_yx.shape)

plt.figure(figsize=(5, 3))
plt.imshow(illumination_yx, cmap="magma")
plt.title("outer product illumination")
plt.axis("off")
plt.colorbar()
plt.tight_layout()
plt.show()

# %% [markdown]
# Tiling and repeating can be useful for building arrays with matching shapes.
# Broadcasting is often even cleaner because it avoids materializing repeated
# copies, but `tile` and `repeat` are worth recognizing when you see them.

# %%
row_pattern = np.array([[0, 1, 2, 3]])
tiled_rows = np.tile(row_pattern, (5, 1))
repeated_columns = np.repeat(row_pattern, repeats=3, axis=0)

print("tiled rows:")
print(tiled_rows)
print("repeated columns:")
print(repeated_columns)

# %%
start = time.perf_counter()
loop_gradient = np.zeros((700, 700), dtype=float)
for row in range(loop_gradient.shape[0]):
    for col in range(loop_gradient.shape[1]):
        loop_gradient[row, col] = row + col
loop_gradient_seconds = time.perf_counter() - start

start = time.perf_counter()
rows = np.arange(700)[:, None]
cols = np.arange(700)[None, :]
broadcast_gradient = rows + cols
broadcast_seconds = time.perf_counter() - start

print(f"loop gradient seconds: {loop_gradient_seconds:.3f}")
print(f"broadcast gradient seconds: {broadcast_seconds:.6f}")
print("same gradient:", np.array_equal(loop_gradient, broadcast_gradient))
