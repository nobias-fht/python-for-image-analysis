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
# In most cases manually inputting array elements is not practical, so NumPy provides functions to create arrays with a given shape and filled with a value, these functions are:
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

print("\nArray of ones:")
print(ones_array)

print("\nArray of 100s:")
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

beginning = 1
end = 2
N = 5
print(f"\nnp.linspace({beginning}, {end}, {N})")
print(np.linspace(beginning, end, N))

shape = (2, 3)
print(f"\nnp.random.random({shape})")
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
#     <summary>💡 <strong>Tip</strong></summary>
#
#     <p>Use the argument <code>endpoint=False</code> in <code>np.linspace</code> to not include the end value in the output.</p>
#   </details>
#   </div>

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
# Reshaping is an important concept, all the elements of an array can be rearranged so that the array has different dimensions.

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
# <div style="
#   background: #e8f7ec;
#   border-left: 6px solid #2f9e44;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #1f5f2c;
# ">
#   <strong style="color: #1f5f2c;">Question</strong><br>
#   How many 2D shapes are there that an array with a total of 12 elements could be reshaped into?
# </div>

# %% [markdown]
# A useful shortcut is to use -1 in reshape and the remaining dimension will be inferred, for example:

# %%
a = np.arange(8).reshape(-1, 2)
print("np.arange(8).reshape(-1, 2)")
print(a)
print(f"Shape: {a.shape}, the first dimension was inferred to be {a.shape[0]}.")

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
print(f"Shape: {a.shape}")

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
# The same ordering needs to be used when flattening to recover the original array

# %%
print("Flattened F-ordered array")
print(a.flatten(order="F"))

# %% [markdown]
# #### Transposing
#
# Sometimes we need to switch the order of the dimensions, this is equivalent to mirroring the array along a diagonal. The can be achieved with the `np.transpose` function. There also the functions:
# - `np.moveaxis`: Moves a source axis to a destination location, and
# - `np.swapaxis`: Swaps the location of two axes.
#
# For example:

# %%
a = np.arange(2 * 3 * 4).reshape(4, 3, 2)
print(f"Original shape: {a.shape}")

a = np.swapaxes(a, 1, 2)
print(f"Shape after np.swapaxes: {a.shape}\n")

print("New array: ")
print(a)


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
#   Look at the documentation for <a href="https://numpy.org/doc/stable/reference/generated/numpy.transpose.html#numpy.transpose"><code>np.transpose</code></a> and <a href="https://numpy.org/doc/stable/reference/generated/numpy.moveaxis.html#numpy.moveaxis"><code>np.moveaxis</code></a>, can you use them to achieve the same transposition as the example above? (e.g. shape <code>(4, 3, 2) -> (4, 2, 3)</code>).
# </div>

# %%
# Use np.transpose to change the order of dimensions to (4, 2, 3)
a = np.arange(2 * 3 * 4).reshape(4, 3, 2)
print(f"Original shape: {a.shape}")
# --- Exercise
a = np.transpose(a, (0, 2, 1))
# ---
print(f"Shape after np.transpose: {a.shape}\n")

# %%
# Use np.moveaxis to change the order of dimensions to (4, 2, 3)
a = np.arange(2 * 3 * 4).reshape(4, 3, 2)
print(f"Original shape: {a.shape}")
# --- Exercise
a = np.moveaxis(a, (1, 2), (2, 1))
# ---
print(f"Shape after np.moveaxis: {a.shape}\n")

# %% [markdown]
# #### Adding singleton dimensions
#
# Sometimes we need to add dimensions with a size of 1, these are called singleton dimensions, a particular use case is for mathematical operations, which we will see below.
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
# NumPy performs element-wise operations; meaning, for example, if we multiply together two arrays `a` and `b` of the same shape, then an element of the resulting array will be the product of the elements at the corresponding position in `a` and `b`.
#
# Element-wise operations apply to all the mathematical function which can be applied with the standard python mathematical operations, e.g. `+`, `-`, `*`, `/`, `**`, `//`, `%`, `>`, `>=`, `<`, `<=`.

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
# Multiplying two arrays of the same shape
a = np.array([[1, 2], [3, 4]])
b = np.array([[1, 10], [100, 1000]])
print_arrays_side_by_side(a, b, f" multiplied by ")
print(f"Shapes: {a.shape} multiplied by {b.shape}")
print("\nResult:")
print(a * b)

# %% [markdown]
# #### Broadcasting
#
# If two arrays are not the same shape, NumPy will attempt to do what is known as *broadcasting*. Broadcasting is a way to make differently shaped arrays compatible for arithmetic operations, under certain constraints. For example if we have a 2D array `a`, NumPy allows us to multiply it with a 1D array `b` that has has the same number of elements as `a` has columns; the operation will be applied across the columns of `a`.
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
print("\nResult:")
print(a * b)
print()

a = np.arange(9).reshape(3, 3)
b = np.arange(3)[np.newaxis]
print_arrays_side_by_side(a, b, f" multiplied by ")
print(f"Shapes: {a.shape} multiplied by {b.shape}")
print("\nResult:")
print(a * b)
print()

a = np.arange(9).reshape(3, 3)
b = np.arange(3)[..., np.newaxis]
print(f"Shapes: {a.shape} multiplied by {b.shape}")
print_arrays_side_by_side(a, b, f" multiplied by ")
print("\nResult:")
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
# Inequalities work in a similar way, for example we can find where an array is less than or equal to 4:

# %%
a = np.arange(9).reshape(3, 3)
print("Array:")
print(a)

result = a <= 4
print("\nLess than or equal to 4:")
print(result)

# %% [markdown]
# Another useful operation is the element-wise not operator `~`, use this on bool arrays:

# %%
a = np.array([False, True, True, False, True])
b = ~a

print("Original array:")
print(a)

print("\nNot array:")
print(b)

# %% [markdown]
# ### Mathematical functions
#
# NumPy provides many [mathematical functions](https://numpy.org/doc/stable/reference/routines.math.html). Some useful examples are:
#
# - `np.mean`
# - `np.max`
# - `np.std`
# - `np.median`
#
# Often it is possible to apply them along a single axis, for example:

# %%
a = np.random.random((100, 3)) * np.arange(1, 4).reshape([1, 3])

mean = np.mean(a, axis=0)
max = np.max(a, axis=0)
std = np.std(a, axis=0)
median = np.median(a, axis=0)

print(f"Operations along axis 0 with of array with shape: {a.shape}")
print(f"\nMean: {mean}")
print(f"Max: {max}")
print(f"Standard deviation: {std}")
print(f"Median: {median}")

print("\nTotal mean:")
# without specifying an axis, the mean is calculated over the whole array.
print(a.mean())

# %% [markdown]
# ### Indexing and slicing
#
# We will need to select subsets of data. We can do this using slices and indexes. Indexing selects an element or sub-array at a specified position along one or more dimensions of an array. Slicing can select a range of elements along a dimension.
#
# NumPy also provides useful [documentation](https://numpy.org/doc/stable/user/basics.indexing.html) on how indexing and slices works, which you can use to see more examples.
#
# Indexing and slicing uses square bracket notation the same as python lists:
# - Indexing: `a[idx]` selects an element/row at position `idx,
# - Slicing: `a[start:stop:step]` selects elements/rows between `start` and `stop` with stride `step`.
#
# As for python lists, omitting `start`, `stop` or `step` will default to the start and end of the array, and `step=1`.

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
# #### Boolean indexing
#
# We can use a boolean array to select elements where the array is `True`

# %%
a = np.array([[42, 0], [1, 13]])

boolean_idx = np.array([[True, False], [False, True]])

print("Elements selected with a boolean array:")
print(a[boolean_idx])

# %% [markdown]
# #### Integer array indexing
#
# We can use arrays of indexes as coordinates, broadcasting rules also apply to array indices.

# %%
a = np.array([[42, 0], [1, 13]])

row_indices = np.array([0, 0, 1])
col_indices = np.array([0, 1, 1])

print("Elements selected with integer arrays:")
print(a[row_indices, col_indices])

# %% [markdown]
# ### Setting values
#
# Indexing can be used to both retrieve elements and also set the value of array elements. Broadcasting rules work in a very similar way. For example:

# %%
print("Zero array:")
a = np.zeros((4, 5))
print(a)

# Set every indexed element to the same value:
print("Set middle column to 1:")
a[:, 2] = 1
print(a)

# Set 2 rows to two different values
print("Set the middle two rows to 2 and 3:")
a[(1, 2), :] = np.array([2, 3]).reshape(2, 1)
print(a)

# Set each selected element to a unique value
print("Set the right bottom 4x4 elements to unique values:")
a[-2:, -2:] = np.array([10, 20, 30, 40]).reshape(2, 2)
print(a)

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
#   What happens if you try to set indexed elements with a shape that is not compatible?
# </div>

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
#   Make a 5×5×5 that has zeros on the edges and a central 3×3×3 array with the values 1 through to 27.
# </div>

# %%
# --- Exercise
a = np.zeros((5, 5, 5))
a[1:-1, 1:-1, 1:-1] = np.arange(1, 28).reshape(3, 3, 3)
print(a)
# ---

# %% [markdown]
# ### Combining and splitting arrays
#
# The main functions for combining arrays are:
# - `np.concatenate` and
# - `np.stack`.
#
# The difference between these functions is that `concatenate` will try to combine the arrays along an existing axis and `stack` will combine array on a new axis. Therefore, when concatenating all the dimensions except the concatenation dimension need to match, and stacking arrays requires all of the dimensions to match.

# %%
a = np.arange(4).reshape(2, 2)
b = np.arange(6).reshape(2, 3) * 10
c = np.arange(4).reshape(2, 2) * 100

print("concatenating two arrays along the columns.")
concat = np.concatenate([a, b], axis=1)
print(concat)
print(f"Shape: {concat.shape}")

print("\nStacking two arrays on a new first axis")
stack = np.stack([a, c], axis=0)
print(stack)
print(f"Shape: {stack.shape}")

# %% [markdown]
# The easiest way to split arrays is `np.split`. It can be used to split arrays evenly along an axis, it will return a list of arrays.

# %%
a = np.arange(18).reshape(6, 3)
print("Full array:")
print(a)
print(f"Shape: {a.shape}")

# Split `a`` into 3, evenly along the first axis
splits = np.split(a, 3, axis=0)
for i, s in enumerate(splits):
    print(f"\nSplit {i}")
    print(s)
    print(f"Shape: {s.shape}")

# %% [markdown]
# ### Copies and Views
#
# The NumPy [documentation](https://numpy.org/doc/stable/user/basics.copies.html) on copies vs views is also very nice.
#
# The main thing to watch out for is some NumPy operations will return a copy and some operations will return a view. If you set the elements in a view, then they will also be changed in the original array that is showing the view.
#
# #### Reshape
#
# Reshape will always return a view if possible, for example

# %%
a = np.arange(9)
b = a.reshape(3, 3)

# We only set the value in `b` but it will also be changed in `a`,
# because `b` is a view on `a`
b[1, 1] = 100

print("Original array:")
print(b)
print("\nReshaped array:")
print(a)

# %% [markdown]
# #### Indexing
#
# Basic indexing will return views, but advanced indexing (boolean and index arrays) will return copies.

# %%
a = np.arange(9).reshape(3, 3)

# keep a reference of the middle row
middle_row = a[1]
# Note the multiply in place operation
middle_row *= 10

print(a)

# %% [markdown]
# #### How to tell if an array is a copy or a view?
#
# The `base` property can be used, if an array is a view it will return the original array, if it is a copy is will return `None`.

# %%
a = np.arange(9)
b = a.reshape(3, 3)

print("Array b is a view of: ")
print(b.base)

d = a[np.array([3, 4, 5])]
print("\nArray d:")
print(d)
print(f"Array d is a copy: {d.base is not None}")

# %% [markdown]
# ### Data Types
#
# NumPy’s standard numerical data types are `bool`, `int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`, `float16`, `float32`, `float64`, `complex64`, and `complex128`. Data types determine how much physical memory each element of an array takes up, and what it can represent, e.g. integers or fractional numbers.
#
# Most relevant for working with bio-images are:
# - `uint8`: unsigned integers (whole numbers) from 0 to 255. (1 byte of memory)
# - `uint16`: unsigned integers from 0 to 65,535. (2 bytes of memory)
# - `int64`: signed integers from −9,223,372,036,854,775,808 to 9,223,372,036,854,775,807. (8 bytes of memory)
# - `float32`: approximately ±3.4 × 10³⁸, with about 7 decimal digits of precision. (4 bytes of memory)
# - `float64`: approximately ±1.8 × 10³⁰⁸, with about 15–16 decimal digits of precision. (8 bytes of memory)
#
# Most NumPy creational functions will allow you to specify the datatype with a `dtype` argument. You can also call `.astype` method on arrays to get a copy cast as a different type. The `dtype` property of an array can be used to find the data type of the current array.

# %%
# The default type for np.zeros is float64
a = np.zeros((2, 2))
print(f"Datatype: {a.dtype}")

# Set the type to int64
a = np.zeros((2, 2), dtype=np.int64)
print(f"Datatype: {a.dtype}")

# %%
# The default type for `np.arange` is int64
a = np.arange(4)
print(f"Datatype: {a.dtype}")

# Use astype to get a copy as float64
a = a.astype(np.float64)
print(f"Datatype: {a.dtype}")

# %% [markdown]
# Sometimes NumPy will automatically cast the result of a mathematical operation to float64, for example:

# %%
a = np.arange(4, dtype=np.uint16)

print("Original array:")
print(a)
print(f"Data type: {a.dtype}")

result = a / 2
print("\nArray divided by 2:")
print(result)
print(f"Data type: {result.dtype}")

# %% [markdown]
# #### Data overflow
#
# Something to be careful of is data overflow. Often bio-images will be stored as `uint8` or `uint16`, if you perform mathematical operations on these arrays that cause the values to flow over the maximum range of the data type the values will wrap around to 0, giving unexpected results. Therefore it is often safest to convert data to floats before doing any analysis.
#
# For example:

# %%
# The maximum value uint8 can store is 255
a = np.array([30, 90, 120], dtype=np.uint8)
print("Original array:")
print(a)

print("\nMultiply by 3:")
print(a * 3)

print(
    "\nThe values of 90 and 120 multiplied by 3 are greater than 255 and so have overflowed, they should be equal to:"
)
print(f"90 * 3 = {90 * 3}")
print(f"120 * 3 = {120 * 3}")

# %% [markdown]
# ### Useful array properties
#
# - `ndim`: tells you the number of dimensions,
# - `shape`: tells you the shape of the array,
# - `size`: tells you the total number of elements in the array
# - `dtype`: tells you the data type,
# - `itemsize`: tells you the number of bytes of memory each element takes up

# %%
a = np.array([[42, 0], [1, 13]], dtype=np.uint16)
print("Array:")
print(a)
print(f"\nndim: {a.ndim}")
print(f"shape: {a.shape}")
print(f"size: {a.size}")
print(f"dtype: {a.dtype}")
print(f"itemsize: {a.itemsize}")

# %% [markdown]
# ## Working with bio-images
#
# #### Pixels
#
# A pixel is the smallest sampled spatial unit in a digital image, and its intensity is usually proportional to the number of photons or electrons detected and converted into an electrical signal. How pixels are recorded depends on the imaging system: in most cameras, physical sensor pixels detect light falling on different areas of the detector, whereas in SEM, each image pixel records the signal from emitted or scattered electrons at a particular beam position. The physical area of the specimen represented by each image pixel can be determined through calibration and is usually recorded in the image metadata. Each element of our NumPy array is a pixel.
#
# <div style="
#   background: #fdecec;
#   border-left: 6px solid #d64545;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #7f1d1d;
# ">
#   <strong style="color: #7f1d1d;">TODO</strong><br>
#   A note on anisotropy?
#   </div>
#
# #### Axes
#
# As we have already mentioned bio-images are usually multi-dimensional with different types of information stored along each axis. The most common axes are:
#
# - `X`: Horizontal spatial extent.
# - `Y`: Vertical spatial extent.
# - `Z`: In many imaging modalities it is possible to record a volume, so we can record the depth in a 3rd spatial axis.
# - `C`: The channel axis separates different signals, such as different wavelengths of light. For example, the red, green, and blue channels in a colour camera or channels tuned to the emission wavelengths of particular fluorophores.
# - `T`: An axis to store samples in time, for example if we image a live sample every 10 seconds the resulting images are stored stacked along the `T` axis.
# - `S`: The sample dimension is often used sto stack different fields of view or samples from the same experiment.
#
# NumPy doesn't store the axes in its metadata so we have to make sure to keep track of the meaning of all the dimensions ourselves.
#
# #### Example data
#
# For this next section we will be using some example data from scikit-image. We will explore scikit-image in more depth in later modules but for now we will simply access their [`cells3d`](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.cells3d) example data.
#
# Looking at the documentation we see that:
# - it has the axis order `ZCYX`,
# - a shape of `(60, 2, 256, 256)`,
# - the physical size represented by each pixel is 0.29 micrometers in the Z axis and 0.26 micrometers in the X and Y axes,
# - the two channels record cell membranes and nuclei and
# - the data is stored as unsigned 16-bit integers.
#
# We will also be using `matplotlib` to display the images. In the next module we will learn more about `matplotlib`, but for now we will mostly be using the `matplotlib.pyplot.imshow` function.

# %%
# import scikit image to access the data
import skimage

# %%
data = skimage.data.cells3d()

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
#   Confirm the shape and data type of the image.
# </div>

# %%
# Print the shape and data type of the data
# --- Exercise
print(f"Shape: {data.shape}")
print(f"Data type: {data.dtype}")
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
#   Transpose the axes so that the order is CZYX, instead of ZCYX.
# </div>

# %%
# transpose the axes to CZYX
# --- Exercise
data = np.moveaxis(data, 1, 0)
print(f"Shape in CZYX order: {data.shape}")
# ---

# %% [markdown]
# #### Displaying data
#
# We can display the images with the `matplotlib.pyplot.imshow` function.

# %%
# plt is a commonly used alias for matplotlib.pyplot for convenience
import matplotlib.pyplot as plt

# %% [markdown]
# We will display the 30th z-slice of the cell membranes channel.

# %%
plt.imshow(data[0, 30])

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
#   Display the 30th z-slice of the nuclei channel.
# </div>

# %%
# --- Exercise
plt.imshow(data[1, 30])
# ---

# %% [markdown]
# ### Try indexing and slicing
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
#   Can you find slices in the X and Y axes that crop one of the nuclei visible in the 30th z-slice? Display the cropped nuclei.
# </div>

# %%
# --- Exercise
plt.imshow(data[1, 30, 130:185, 85:140])
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
#   Instead of an XY-plane, can you display a ZY-plane?
# </div>

# %%
# --- Exercise
plt.imshow(data[1, :, :, 128])
# ---

# %% [markdown]
# ### Line profile example
#
# If we select data along a row of an image, we can plot it as a line profile, which can sometimes help us to interpret the data.

# %%
row_idx = 128  # Try chaning the row index!
row_data = data[1, 30, row_idx, :]

# Making a matplotlib figure with two plots
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].imshow(data[1, 30])
axes[0].plot([0, 256], [row_idx, row_idx], c="r")
axes[0].set_xlim(0, 256)

axes[1].plot(row_data, c="r")
axes[1].set_ylim(0, None)

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
#   Plot the line profile of a column.
# </div>

# %%
column_idx = 128  # Try changing the column index!
z_idx = 30
channel_idx = 1

# --- Exercise
column_data = data[channel_idx, z_idx, :, column_idx]
# ---

# Making a matplotlib figure with two plots
fig, axes = plt.subplots(channel_idx, 2, figsize=(12, 6))
axes[0].imshow(data[channel_idx, z_idx])
axes[0].plot([row_idx, row_idx], [0, 256], c="r")
axes[0].set_ylim(255, 0)

axes[1].plot(column_data, c="r")
axes[1].set_ylim(0, None)

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
#   From the line profiles above, can you estimate the intensity value of the background?
# </div>
#

# %% [markdown]
# ### Projections
#
# We call functions that can project the image to a lower dimension "projections", it can help us visualize 3D data in 2D. Common ways to project a 3D volume to 2D is to either:
# - take the maximum value along the Z-axis (a max projection), or
# - take the mean along the Z-axis (a mean projection).
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
#   Can you display a mean projection of the membranes channel?
# </div>

# %%
# Display a mean projection of the membranes channel.
# --- Exercise
mean_proj = data[0].mean(axis=0)
plt.imshow(mean_proj)
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
#   How would a mean projection be different from a sum projection (taking the sum along the Z-axis)?
# </div>

# %% [markdown]
# ### Watch out!
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
#   What is wrong with the following image, what has happened?
# </div>

# %%
result = data[1, 30] * 3
plt.imshow(result)

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
#   Fix the result above so we get the expected values when multiplying the data by 3.
# </div>

# %%
# --- Exercise
result = data[1, 30].astype(np.float64) * 3
plt.imshow(result)
# ---

# %% [markdown]
# ### Meshgrid (Optional)

# %%
ii, jj = np.mgrid[-128:128, -128:128]

fig, axes = plt.subplots(1, 2)
axes[0].imshow(ii)
axes[1].imshow(jj)

# %%
R = 120
circle_mask = ii**2 + jj**2 <= R**2
plt.imshow(circle_mask)

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
#   Create a circular mask centered on of one of of the nuclei in the 30th z-slice, and set all of the pixels outside the circle to zero.
#   <details>
#   <summary>❓ <strong>Hint</strong></summary>
#     You can use the coorindates (row=156, column=112), and a diameter of 52.
#   </details>
#   </div>
# </div>

# %%
ii, jj = np.mgrid[:256, :256]
z30 = data[1, 30].copy()

# In the array `z30`, set all the values outside the selected nucleus to zero
# --- Exercise
mask = (ii - 156) ** 2 + (jj - 112) ** 2 > (52 / 2) ** 2
z30[mask] = 0
# ---

plt.imshow(z30)

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
#   Use the mask from the previous exercise to find the mean intensity of the masked region.
# </div>

# %%
# --- Exercise
mean = z30[~mask].mean()
print(mean)
# ---
