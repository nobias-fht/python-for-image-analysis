# %% [markdown]
# # Module 2: working with bioimages
#
# Time: 1 hour 45 minutes.
#
# Bio-image data often has more than two dimension, including 3 spatial dimensions, multiple channels, time, and multiple fields of view or samples. For example a bio-image might have the shape:
# ```
# Shape: (60, 2, 100, 1024, 1024), Axes: (Time, Channels, Z, Y, X)
# ```
# This is already a 5 dimensional array! 🤯
#
# So, being able to manipulate multi-dimensional arrays is essential for bio-image analysis. We will be working with [NumPy](https://numpy.org/doc/stable/index.html), a very popular library used in many scientific fields for representating and manipulating of multi-dimensional arrays.
#
# ### Objective
# - Understand multi-dimensional bio-images, including the concepts of data types, axes and pixels.
# - Use NumPy to select data, manipulate axes, and use basic operations.

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
#   Create a 3D array!
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
print("Array of 100s:")
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
#   Can you use both <code>np.linspace</code> and <code>np.arange</code> to make the array <code>[0.  0.1 0.2 0.3 0.4]</code>?
#   <details>
#   <summary>💡 <strong>Tip</strong></summary>
#
#   <p>Use the argument <code>endpoint=False</code> in <code>np.linspace</code> to not include the end value in the output.</p>
# </details>
# </div>

# %%
# --- Exercise
start = 0
end = 0.5
N = 5
step = 0.1
print("np.linspace")
print(np.linspace(start, end, N, endpoint=False))
print("np.arange")
print(np.arange(start, end, step))
# ---

# %% [markdown]
# ### Reshaping
#
# Reshaping is an important concept, all the elements of an array can be rearanged so that the array has different dimensions.

# %%
# NOTE: Calling np.arange(20) is equivalent to np.arange(0, 20, 1)
print("a = np.arange(20)")
a = np.arange(20)
print(a)
print(f"Shape: {a.shape}\n")

print("a.reshape(2, 10)")
a = a.reshape(2, 10)
print(a)
print(f"Shape: {a.shape}\n")

print("a.reshape(4, 5)")
a = a.reshape(4, 5)
print(a)
print(f"Shape: {a.shape}")

# %% [markdown]
# A useful shortcut is to use -1 in reshape and the remaining dimension will be infered, for example:

# %%
a = np.arange(8).reshape(-1, 2)
print("np.arange(8).reshape(-1, 2)")
print(a)
print(f"Shape: {a.shape}, the first dimension was infered to be {a.shape[0]}.")

# %% [markdown]
# #### Flattening
#
# Turning an array into a 1D array is called flattening, the method `flatten` can be used for convenience.

# %%
a = np.arange(9).reshape(3, 3)
print("Array")
print(a)
print(f"Shape: {a.shape}\n")
a = a.flatten()
print("Flattened")
print(a)
print(f"Shape: {a.shape}\n")

# %% [markdown]
# #### A note on element order
#
# Notice that if we reshape a 1D array into 2D or 3D to get the original order we read the elements along the last dimension followed by the second last etc. This is because NumPy is has row major ordering also known as being C-ordered because it is the order that the language C uses. However, it is not the only way to reshape an array, if an array is Fortran-ordered (F-ordered) the first dimension is traversed first, followed by the second etc.

# %%
print("C-ordered reshaping")
a = np.arange(24).reshape(2, 3, 4)
print(a)

# %%
print("F-ordered reshaping")
a = np.arange(24).reshape(2, 3, 4, order="F")
print(a)

# %% [markdown]
# The same ordering needs to be used when flattening to recover the orginal array

# %%
print("Flattened F-ordered array")
print(a.flatten(order="F"))

# %% [markdown]
# #### Adding singleton dimensions
#
# Sometimes we need to add dimensions with a size of 1, these are called singleton dimensions, a paricular use case is for mathematical operations, which we will see below.
#
# Of course we can use the `reshape` method to add dimensions but there are two alternatives:
# - `np.newaxis` notation
# - `np.expand_dims` function

# %%
a = np.arange(9).reshape(3, 3)
print(f"Original array shape: {a.shape}")

# Add singleton leading dimensions with np.newaxis
a = a[np.newaxis, np.newaxis]
print(f"Shape with two additional leading dimensions: {a.shape}")

# Add singleton trailing dimensions with np.newaxis
# We use the ellipsis "..." to add trailing singleton dimensions
# We will encounter the ellipsis again in the slicing and indexing section below
a = a[..., np.newaxis, np.newaxis]
print(f"Shape with two additional trailing dimensions: {a.shape}")

# %% [markdown]
# We can also use the `np.expand_dims` to add singleton dimensions by passing a tuple of dimensions to expand. The tuple of dimensions is the dimensions that will be singletons after the array is transformed, this can be a little unintuitive sometimes.

# %%
a = np.arange(9).reshape(3, 3)
print(f"Original array shape: {a.shape}")

singleton_dims = (0, 2, 4)
a = np.expand_dims(a, singleton_dims)
print(f"Shape after expanding the dimensions {singleton_dims}: {a.shape}")

# %% [markdown]
# #### Removing singleton dimensions
#
# To remove singleton dimensions we can use the `squeeze` method. Without any arguments, `squeeze` will remove every singleton dimension, or we can choose specific dimensions to remove.

# %%
print(f"Current shape: {a.shape}")
print("Removing the middle singleton dimension with a.squeeze(2)")
a = a.squeeze(2)
print(f"Shape after squeeze: {a.shape}")
print("Removing the remaining singleton dimensions with a.squeeze()")
a = a.squeeze()
print(f"Shape after squeeze: {a.shape}")

# %% [markdown]
# ### Mathematical operations
#
# NumPy performs elementwise operations; meaning, for example, if we multiply together two arrays `a` and `b` of the same shape, then an element of the resulting array will be the product of the elements at the corresponding position in `a` and `b`.
#
# Elementwise operations apply to all the mathematical function which can be applied with the standard python mathematical operations, e.g. `+`, `-`, `*`, `/`, `**`, `//`, `%`.

# %%
# a function for printing arrays side by side
from itertools import zip_longest


def print_arrays_side_by_side(a: np.ndarray, b: np.ndarray, middle_text: str) -> None:
    left = np.array2string(a).splitlines()
    right = np.array2string(b).splitlines()

    width = max(map(len, left))

    for row, (l, r) in enumerate(zip_longest(left, right, fillvalue="")):
        separator = middle_text if row == 0 else " " * len(middle_text)
        print(f"{l:<{width}}{separator}{r}")


# %%
# Multipling two arrays of the same shape
a = np.array([[1, 2], [3, 4]])
b = np.array([[1, 10], [100, 1000]])
print_arrays_side_by_side(a, b, f" multiplied by ")
print(f"Shapes: {a.shape} multiplied by {b.shape}")
print("Result:")
print(a * b)

# %% [markdown]
# #### Broadcasting
#
# If two arrays are not the same shape, NumPy will attempt to do what is known as *broadcasting*. Broadcasting is a way to make differently shaped arrays compatible for arithemetic operations, under certain constraints. For example if we have a 2D array `a`, NumPy allows us to multiply it with a 1D array `b` that has has the same number of elements as `a` has columns; the operation will be applied across the columns of `a`.
#
# The following text comes directly from the NumPy [documentation](https://numpy.org/doc/stable/user/basics.broadcasting.html) where broadcasting is explained in more detail. It states that the general rules of broadcasting are:
#
# > When operating on two arrays, NumPy compares their shapes element-wise. It starts with the trailing (i.e. rightmost) dimension and works its way left. Two dimensions are compatible when
# > - they are equal, or
# > - one of them is 1.
# >
# > If these conditions are not met, a `ValueError: operands could not be broadcast together` exception is thrown, indicating that the arrays have incompatible shapes.
# >
# > Input arrays do not need to have the same number of dimensions. The resulting array will have the same number of dimensions as the input array with the greatest number of dimensions, where the size of each dimension is the largest size of the corresponding dimension among the input arrays. Note that missing dimensions are assumed to have size one.

# %%
a = np.arange(9).reshape(3, 3)
b = np.arange(3)
print_arrays_side_by_side(a, b, f" multiplied by ")
print(f"Shapes: {a.shape} multiplied by {b.shape}")
print("Result:")
print(a * b)
print()

a = np.arange(9).reshape(3, 3)
b = np.arange(3)[np.newaxis]
print_arrays_side_by_side(a, b, f" multiplied by ")
print(f"Shapes: {a.shape} multiplied by {b.shape}")
print("Result:")
print(a * b)
print()

a = np.arange(9).reshape(3, 3)
b = np.arange(3)[..., np.newaxis]
print("Result:")
print(f"Shapes: {a.shape} multiplied by {b.shape}")
print_arrays_side_by_side(a, b, f" multiplied by ")
print(a * b)

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
#   In the following cell, add singleton dimensions to array <code>b</code> so that arrays <code>a</code> and <code>b</code> can be multiplied together.
# </div>

# %%
a = np.arange(18).reshape(2, 3, 3)
b = np.array([10, 100])
# --- Exercise
b = b.reshape(2, 1, 1)  # Solution 1
# b = b[..., np.newaxis, np.newaxis]  # Solution 2
# b = np.expand_dims(b, (-1, -2))  # Solution 3
# ---
print(a * b)

# %% [markdown]
# ### Indexing and slicing
#
# We will need to select subsets of data. We can do this using slices and indexes. Indexing selects an element or subarray at a specified position along one or more dimensions of an array. Slicing can select a range of elements along a dimension.
#
# Indexing and slicing uses square bracket notation the same as python lists:
# - Indexing: `a[idx]` selects an element/row at position `idx,
# - Slicing: `a[start:stop:step]` selects elements/rows between `start` and `stop` with stride `step`.
#
# As for python lists, ommiting `start`, `stop` or `step` will default to the start and end of the array, and `step=1`.

# %%
a = np.arange(12)
print(f"Array: a={a}")

print(f"a[4] = {a[4]}")
print(f"a[3:10:2] = {a[3:10:2]}")
print(f"a[4:] = {a[4:]}")
print(f"a[:-4] = {a[:-4]}")
print(f"a[::2] = {a[::2]}")
print(f"a[:] = {a[:]}")

# %% [markdown]
# For ***multi-dimensional arrays***, indices and slices can be combined. For example if we have an array with shape `(2, 5, 5)`, we can imagine it has the axes `(Channels, Y, X)`, then we can select the first channel and trim the border elements in `Y` and `X` by doing:

# %%
a = np.arange(2 * 5 * 5).reshape(2, 5, 5)
print("Array:")
print(a)
print()
print("a[0, 1:-1, 1:-1]")
print(a[0, 1:-1, 1:-1])

# %% [markdown]
# <div style="
#   background: #accffb;
#   border-left: 6px solid #2f80ed;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #21457f;
# ">
#   <strong>Exercise</strong><br>
#   Select the final row for both channels from the array <code>a</code> above,
#   i.e. you should end up with the values:
#
#   <pre style="
#     background: #accffb;
#     padding: 10px;
#     border-radius: 5px;
#     color: #222;
#   "><code>
#   [[20 21 22 23 24]
#    [45 46 47 48 49]] </code></pre>
#
#   <strong>Note</strong>: you can use an empty slice <code>:</code> to select all of a dimension.
#
# </div>

# %%
# --- Exercise
print(a[:, -1])
# ---

# %% [markdown]
# We can use the ***ellipsis*** `...` to expand dimensions selected with the empty slice `:`, for example we can select the middle columns of the previous array by doing:

# %%
a[..., 2]

# %% [markdown]
# This is equivalent to using the empty slice `:`, e.g.:

# %%
a[:, :, 2]

# %% [markdown]
# ### Setting values

# %%
a = np.zeros((2, 5, 5))
a[0, 1:-1, 1:-1] = np.arange(10, 40, 10)
a

# %% [markdown]
# #### Boolean indexing

# %%

# %% [markdown]
# #### Integer array indexing

# %%

# %% [markdown]
# ### Combining and spliting arrays

# %%

# %% [markdown]
# ### Copies and Views
#
# #### slicing vs fancy indexing
#
# #### flatten vs ravel

# %%

# %% [markdown]
# ### Data Types

# %%

# %% [markdown]
# ### Data overflow

# %%

# %% [markdown]
# ### Useful array properties
#
# - `ndims`
# - `shape`
# - `size`
# - `dtype`
# - `itemsize`

# %%

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
