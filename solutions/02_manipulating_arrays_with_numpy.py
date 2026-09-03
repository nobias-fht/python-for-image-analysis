# %% [markdown]
# # Module 2: working with bioimages
#
# Time: 1 hour 45 minutes.
#
# Bio-image data often has more than two dimension, including 3 spatial dimensions, multiple channels, time, and multiple fields of view or samples. So, being able to manipulate multi-dimensional arrays is essential for bio-image analysis. We will be working with [NumPy](https://numpy.org/doc/stable/index.html), a very useful library in many scientific fields for representation and manipulation of multi-dimensional arrays.
#
# ### Objective
# - Understand multi-dimensional bio-images, including the concepts of data types, axes and pixels.
# - Use NumPy to select data, manipulate axes, and use basic operations,

# %%
# Import numpy into the notebook so we can use it!
# it is common practice to use the alias `np`
import numpy as np

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
# #### 1) From a python list, or list of lists for 2D:

# %%
array_1D = np.array([10, 42, 99, 3])

# NOTE: you can find the shape of an array with the .shape property
#   and list the number of dimensions with .ndim
print(f"{array_1D.ndim}D Array Shape: {array_1D.shape}")
print(array_1D)

# %%
array_2D = np.array(
    [
        [10, 42],
        [99, 3],
    ]
)

print(f"{array_2D.ndim}D Array Shape: {array_2D.shape}")
print(array_2D)

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
#   Can you create a 3D array?
# </div>

# %%
# Initialize a 3D array print it and check the `shape` and `ndim` properties
# --- Exercise
array_3D = np.array([[[10, 42], [99, 3]], [[1234, 100], [0, 7]]])

print(f"{array_3D.ndim}D Array Shape: {array_3D.shape}")
print(array_3D)
# ---

# %% [markdown]
# #### 2) Initialize arrays filled with a single value
#
# In most cases manually inputing array elements is not practical, so NumPy provides functions to create arrays with a given shape and filled with a value, these functions are:
#
# - `np.zeros`: creates and array filled with zeros.
# - `np.ones`: creates and array filled with ones.
# - `np.full`: creates and array filled with a given value.

# %%
shape = (2, 3, 4)
zeros_array = np.zeros(shape=shape)
ones_array = np.ones(shape=shape)
full_array = np.full(shape=shape, fill_value=100)

print("Array of zeros:")
print(zeros_array)
print()
print("Array of ones:")
print(ones_array)
print()
print("Array of 100:")
print(full_array)

# %% [markdown]
# #### 3) Other useful functions
#
# Some other useful functions to create arrays include
#
# - `np.arange`: create a 1D array of integers between for a given range and step difference.
# - `np.linspace`: create a 1D array of `N` evenly spaced numbers for a given range.
# - `np.random.random`: create an array of a given shape with random numbers between [0, 1].
#
# You can find many other ways to create arrays in the NumPy [documentation](https://numpy.org/doc/stable/reference/routines.array-creation.html)!

# %%
start = 2
stop = 13
step = 2
print(f"np.arange({start}, {stop}, {step})")
print(np.arange(start, stop, step))
print()

beginning = 1
end = 2
N = 5
print(f"np.linspace({beginning}, {end}, {N})")
print(np.linspace(beginning, end, N))
print()

shape = (2, 3)
print(f"np.random.random({shape})")
print(np.random.random(shape))

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
#   Can you use <code>np.linspace</code> to make the array <code>[2.5, 5., 7.5, 10.]</code>?
#
# </div>

# %%
# --- Exercise
np.linspace(2.5, 10, 4)
# ---

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
