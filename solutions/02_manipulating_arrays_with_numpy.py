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
# So, being able to manipulate multi-dimensional arrays is essential for bio-image analysis.
# We will be working with [NumPy](https://numpy.org/doc/stable/index.html), a very popular library used in many scientific fields for representating and manipulating of multi-dimensional arrays.
#
# ### Question
#
# How can we manipulate high-dimensional arrays that represent bio-images so that we can perform the operations required to analyse the data?
#
# ### Objective
# - Understand multi-dimensional bio-images, including the concepts of data types, axes and pixels.
# - Use NumPy to select data, manipulate axes, and use basic operations.

# %% [markdown]
# # 1 - Intro to NumPy
#
# NumPy is an open source library which is very commonly used in python for handling arrays.
# It provides many useful functions and mathematical operations, most of the underlying code is written in C, making it usually much faster than native python loops.
#
# NumPy provides a great user [guide](http://numpy.org/doc/stable/user/basics.html) that explains fundementals and usage.
# We will cover many of the concepts presented in their guide in this module, but we encourage looking through the guides in your own time.
#
# Also, check out the [API reference](https://numpy.org/doc/stable/reference/index.html) that lists every NumPy function, grouped by theme.

# %%
# Import numpy into the notebook so we can use it!
# it is common practice to use the alias `np`
import numpy as np

# %% [markdown]
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
#
#   Create a 3D array! Check it has the shape that you expected by accessing the `.shape` property.
# </div>

# %%
# Initialize a 3D array print it and check the `shape` and `ndim` properties
# --- Exercise
array_3D = np.array([[[10, 42], [99, 3]], [[1234, 100], [0, 7]]])

print(f"{array_3D.ndim}D Array Shape: {array_3D.shape}")
print(array_3D)
# ---

# %% [markdown]
# #### 2) Creational functions
#
# In most cases manually inputting array elements is not practical, so NumPy provides functions to create arrays.
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
#
#   Check out the [Array Creation Routines](https://numpy.org/doc/stable/reference/routines.array-creation.html) section of the API reference.
#   Find a creational function to create an array of zeros with the shape `(2, 3, 4)`. Print the array.
# </div>

# %%
shape = (2, 3, 4)

# Make an array of zeros using one of NumPy's creational functions
# --- Exercise
zeros_array = np.zeros(shape=shape)
print(zeros_array)
# ---

# %% [markdown]
# <div style="
#   background: #fff8db;
#   border-left: 6px solid #e2b200;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #8a6a00;
# ">
#   <strong style="color: #8a6a00;">Note</strong><br>
#
#   Another other useful creational function, which we will use throughout the module, is [`np.arange`](https://numpy.org/doc/stable/reference/generated/numpy.arange.html). It creates a 1D array of integers for a given range and step difference.
# </div>

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
# ## 2 - Intro to Bio-images and Example Data
#
# #### Pixels
#
# A pixel is the smallest sampled spatial unit in a digital image, and its intensity is usually proportional to the number of photons or electrons detected and converted into an electrical signal. How pixels are recorded depends on the imaging system: in most cameras, physical sensor pixels detect light falling on different areas of the detector, whereas in SEM, each image pixel records the signal from emitted or scattered electrons at a particular beam position. The physical area of the specimen represented by each image pixel can be determined through calibration and is usually recorded in the image metadata. Each element of our NumPy array is a pixel.
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
# - `S`: The sample dimension is often used to stack different fields of view or samples from the same experiment.
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
# - the physical size represented by each pixel is 0.29 micrometers in the Z axis and 0.26 micrometers in the X and Y axes, this means the data is ***anisotropic*** (physical pixel lengths are not equal),
# - the two channels record cell membranes and nuclei and
# - the data is stored as unsigned 16-bit integers.

# %%
# import scikit image to access the data
import skimage

# %%
# access the example data
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
# ## 3 - Indexing and slicing
#
# We will need to select subsets of data. We can do this using slices and indexes. Indexing selects an element or sub-array at a specified position along one or more dimensions of an array. Slicing can select a range of elements along a dimension.
#
# NumPy also provides useful [documentation](https://numpy.org/doc/stable/user/basics.indexing.html) on how indexing and slices works, which you can use to see more examples.
#
# ### Simple indexing and slicing
#
# Indexing and slicing uses square bracket notation the same as python lists:
# - Indexing: `a[idx]` selects an element/row at position `idx`,
# - Slicing: `a[start:stop:step]` selects elements/rows between `start` and `stop` with stride `step`.
#
# As for python lists, omitting `start`, `stop` or `step` will default to the start and end of the array, and `step=1`.
#
# Negative numbers can be used to count back from the end of an array.
#
# ⚠️ **Remember**: Indexing starts at 0.
#
# #### Multi-dimensional data
#
# For multi-dimensional arrays, indices and slices can be combined, the index or slice for each dimension is separated by a comma.
#
# #### Displaying data
#
# We will also be using `matplotlib` to display the images. In the next module we will learn more about `matplotlib`, but for now we will mostly be using the `matplotlib.pyplot.imshow` function.
#
# We can display the images with the `matplotlib.pyplot.imshow` function, simply pass the 2D array that you want to display.

# %% [markdown]
# <div style="
#   background: #fff8db;
#   border-left: 6px solid #e2b200;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #8a6a00;
# ">
#   <strong style="color: #8a6a00;">Note:</strong> Ellipsis<br>
#
#   We can use the ***ellipsis*** `...` to expand dimensions selected with the empty slice `:`, for example if array `a` has 3 dimensions then the following indexing is equivalent:
#
#   - `a[..., 2]`
#   - `a[:, :, a]`
# </div>
# <div style="
#   background: #fff8db;
#   border-left: 6px solid #e2b200;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #8a6a00;
# ">
#   <strong style="color: #8a6a00;">Note:</strong> Integer array indexing<br>
#
#   We can use arrays of indexes as coordinates, e.g. in a 2D array the row coordinates and column coordinates are passed as 1D arrays separated by a comma. Broadcasting rules also apply to array indices. Check out the [documentation](https://numpy.org/doc/stable/user/basics.indexing.html#integer-array-indexing) if you want to learn more!
# </div>

# %%
# plt is a commonly used alias for matplotlib.pyplot for convenience
import matplotlib.pyplot as plt

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
#
#   Use slicing to select every other element in array `a` starting from the first element. Print the result.
# </div>

# %%
a = np.arange(12)
print("Array:")
print(a)

print("\nEvery other element:")
# --- Exercise
print(a[::2])
# ---

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
#   Can you use slicing to reverse the order of an array?
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
#
#   We want to view the `cells3d` data we downloaded from SciKit-Image but the function `plt.imshow` can only display 2D data.
#
#   Use indexing to select the 30th z-slice of the nuclei or membrane channel and display the result.
#
#   <details>
#   <summary>
#   <strong>Hint</strong>
#   </summary>
#
#   Remember the axes order of the `cells3d` data is `ZCYX`.
#   </details>
# </div>

# %%
# Display the 30th z-slice of one of the channels using plt.imshow(chosen_slice)
# --- Exercise
plt.imshow(data[30, 1])
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
#   <strong style="color: #21457f;">Exercise:</strong> Cropping<br>
#
#   NumPy slicing can be used to crop the data.
#
#   Can you find slices in the X and Y axes that crop one of the nuclei visible in the 30th z-slice? Display the cropped nuclei.
# </div>

# %%
# --- Exercise
plt.imshow(data[30, 1, 130:185, 85:140])
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
#
#   Instead of an XY-plane, can you display a ZY-plane?
# </div>

# %%
# --- Exercise
plt.imshow(data[:, 1, :, 128])
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
#
#   Does the shape of the cells seem different in the XY view vs the ZY view? Why is this?
#   <details>
#   <summary>
#   <strong>Hint</strong>
#   </summary>
#
#   Think about what the physical lengths of each pixel side are reported to be.
#   </details>
# </div>

# %% [markdown]
# ### Boolean indexing
#
# Boolean arrays are arrays that only contain the values `True` and `False`.
# Boolean arrays can be used to index an array of the same shape, selecting elements in the array where the equivalent elements are `True`.
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
#
#   Experiment with boolean indexing, create a boolean array to index the array `a` below:
#
#   <details>
#   <summary>
#   <strong>Hint</strong>
#   </summary>
#
#   If `a` is the array to index, and `b` is the boolean array the syntax for boolean indexing is `a[b]`.
#   </details>
# </div>

# %%
a = np.arange(6)

# Create a boolean array to select values from the array `a`
# --- Exercise
b = np.array([True, False, False, True, False, False])
print(a[b])
# ---

# %% [markdown]
# ## 4 - Manipulating dimensions
#
# ### Reshaping
#
# Reshaping is an important concept, all the elements of an array can be rearranged so that the array has different dimensions.
#
# It is possible to reshape an array using either the numpy function `np.reshape`, or the `.reshape` method: e.g:
#
# ```python
# reshaped_array = np.reshape(array, (4, 3, 2))
# reshaped_array = array.reshape(4, 3, 2)
# ```
#
# <div style="
#   background: #fff8db;
#   border-left: 6px solid #e2b200;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #8a6a00;
# ">
#   <strong style="color: #8a6a00;">Note</strong><br>
#
# Sometimes we want to convert our array to a 1D array, for this we can use either the:
# - `np.ravel` function or the `.ravel` method or
# - the `.flatten` method.
#
# Make sure to check out the documentation!
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
#
#   Try reshaping the array below so that it has the shape `(2, 12)`, verify that the resulting array has the correct shape.
# </div>

# %%
print("Original array:")
a = np.arange(24)
print(a)
print(f"Shape: {a.shape}\n")

print("Reshaped array")
# Reshape the array
# --- Exercise
a = a.reshape(2, 12)
# ---
print(a)
print(f"Shape: {a.shape}\n")

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
#
#   What happens if you try to reshape the array above to the shape `(2, 5)`?
# </div>
# <div style="
#   background: #e8f7ec;
#   border-left: 6px solid #2f9e44;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #1f5f2c;
# ">
#   <strong style="color: #1f5f2c;">Question</strong><br>
#   How many 2D shapes are there that an array with a total of 24 elements could be reshaped into?
# </div>

# %% [markdown]
# ### Reshaping tip
#
# A useful shortcut is to use -1 in reshape and the remaining dimension will be inferred, for example:

# %%
a = np.arange(8).reshape(-1, 2)
print("np.arange(8).reshape(-1, 2)")
print(a)
print(f"Shape: {a.shape}, the first dimension was inferred to be {a.shape[0]}.")

# %% [markdown]
# ### Transposing
#
# Sometimes we need to switch the order of the dimensions, this is equivalent to mirroring the array along a diagonal.
# This can be achieved with the `np.transpose` function or the `.transpose` method. There are also the functions:
# - `np.moveaxis`: Moves a source axis to a destination location, and
# - `np.swapaxes`: Swaps the location of two axes.

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
#
#   Look at the documentation for [`np.transpose`](https://numpy.org/doc/stable/reference/generated/numpy.transpose.html#numpy.transpose),[`np.moveaxis`](https://numpy.org/doc/stable/reference/generated/numpy.moveaxis.html#numpy.moveaxis), or [`np.swapaxes`](https://numpy.org/doc/stable/reference/generated/numpy.swapaxes.html); choose one of them to achieve the transposition: axes `ZCYX -> CZYX` in the example image `data`.
# </div>

# %%
print(f"Original shape: {data.shape}")

# Use np.transpose, np.moveaxis or np.swapaxes so that the axis order is CZYX
# --- Exercise
data = np.transpose(data, (1, 0, 2, 3))  # Solution 1
# data = np.moveaxis(data, 1, 0)  # Solution 2
# data = np.swapaxes(data, 0, 1)  # Solution 3
# ---
print(f"Shape in CZYX order: {data.shape}")

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
#
#   Why would reshaping the array to have the shape `(2, 60, 256, 256)` not give the desired results?
# </div>

# %% [markdown]
# ### Adding singleton dimensions
#
# Sometimes we need to add dimensions with a size of 1, these are called singleton dimensions, a particular use case is for mathematical operations, which we will see below.
#
# Of course we can use the `reshape` method to add dimensions but there are two alternatives:
# - `np.newaxis` notation: useful for adding new leading or trailing singleton dimensions.
# - `np.expand_dims` function: useful for adding singleton dimensions anywhere. Make sure to check the documentation!

# %%
a = np.arange(9).reshape(3, 3)
print(f"Original array shape: {a.shape}")

# Add singleton leading dimensions with np.newaxis
a = a[np.newaxis, np.newaxis]
print(f"Shape with two additional leading dimensions: {a.shape}")

# Add singleton trailing dimensions with np.newaxis
# We use the ellipsis "..." to add trailing singleton dimensions
# We encountered the ellipsis in the indexing and slicing section above
a = a[..., np.newaxis, np.newaxis]
print(f"Shape with two additional trailing dimensions: {a.shape}")

# %% [markdown]
# ### Removing singleton dimensions
#
# To remove singleton dimensions we can use the `squeeze` method. Without any arguments, `squeeze` will remove every singleton dimension, or we can choose specific dimensions to remove.

# %%
a = np.arange(9).reshape(1, 3, 1, 3, 1)

print(f"Current shape: {a.shape}")
print("Removing the middle singleton dimension with a.squeeze(2)")
a = a.squeeze(2)
print(f"Shape after squeeze: {a.shape}")
print("Removing the remaining singleton dimensions with a.squeeze()")
a = a.squeeze()
print(f"Shape after squeeze: {a.shape}")
# %% [markdown]
# <div style="
#   background: #fff8db;
#   border-left: 6px solid #e2b200;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #8a6a00;
# ">
#   <strong style="color: #8a6a00;">Note: </strong>Element order<br>
#
# Notice that if we reshape a 1D array into 2D or 3D to get the original order we read the elements along the last dimension followed by the second last etc. This is because NumPy has row major ordering also known as being C-ordered because it is the order that the language C uses. However, it is not the only way to reshape an array, if an array is Fortran-ordered (F-ordered) the first dimension is traversed first, followed by the second etc.
# </div>
# <div style="
#   background: #f3f4f6;
#   border-left: 6px solid #6b7280;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #374151;
# ">
#   <strong>Optional Exercise</strong><br>
#
#   Experiment with the `order` argument in `reshape`.
# </div>

# %% [markdown]
# ## 5 - Mathematical operations & Broadcasting
#
# NumPy performs element-wise operations; meaning, for example, if we multiply together two arrays `a` and `b` of the same shape, then an element of the resulting array will be the product of the elements at the corresponding position in `a` and `b`.
#
# Element-wise operations apply to all the mathematical function which can be applied with the standard python mathematical operations, e.g. `+`, `-`, `*`, `/`, `**`, `//`, `%`, `>`, `>=`, `<`, `<=`.
#
# Operations can also be applied along a dimension or multiple dimensions, for example, multiplying each row of an array by a value, this can be achieved with *broadcasting*.
# This also includes scalar operations where a single value operates on all the elements in an array.
#
# For example multiplying two arrays together:

# %%
a = np.array([[1, 2], [3, 4]])
b = np.array([[1, 10], [100, 1000]])

# Multiply the arrays `a` and `b` together and print the results
print("Result:")
result = a * b
print(result)

# %% [markdown]
# #### Broadcasting
#
# If two arrays are not the same shape, NumPy will attempt to do what is known as *broadcasting*. Broadcasting is a way to make differently shaped arrays compatible for arithmetic operations, under certain constraints. For example if we have a 2D array `a`, NumPy allows us to multiply it with a 1D array `b` that has the same number of elements as `a` has columns; the operation will be applied across the columns of `a`.
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
#
# #### Examples
#
# Below is a demonstration showing that missing dimensions are treated as 1 and that we start with the final (trailing) dimension.
# We can see that the operation is applied column-wise.

# %%
a = np.arange(6).reshape(2, 3)
b = np.arange(3)
print(f"Shapes: {a.shape} multiplied by {b.shape}")
print("Result:")
print(a * b)

a = np.arange(6).reshape(2, 3)
b = np.arange(3)[np.newaxis]
print(f"\nShapes: {a.shape} multiplied by {b.shape}")
print("Result:")
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
#
#   Add a singleton dimension to the array `b` below so that it can be used to multiply each row of the array `a`. Print the result of the multiplication.
# </div>

# %%
a = np.arange(6).reshape(2, 3)
b = np.array([2, 10])

print("\nResult:")
# --- Exercise
b = b[..., np.newaxis]  # Solution 1
# b = b.reshape(2, 1)  # Solution 2
# b = np.expand_dims(a, 0) # Solution 3

print(a * b)
# ---


# %% [markdown]
# ### Mathematical functions
#
# NumPy provides many [mathematical functions](https://numpy.org/doc/stable/reference/routines.math.html). Some useful examples are:
#
# - `np.mean`
# - `np.max`
# - `np.min`
# - `np.std`
# - `np.median`
#
# It is possible to apply them along a single or muliple axes with `axis` argument.
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
#
#   Find the maximum intensity of each channel in `data` (the SciKit-Image `cells3d` data). Print the results.
#
#   <details>
#   <summary>
#   <strong>Hint</strong>
#   </summary>
#
#   This means the operation needs to be applied over the `Z`, `Y` and `X` axes, you can pass a `tuple` to the `axis` argument.
#   </details>
# </div>

# %%
# Find the mean of each channel independently
# --- Exercise
channel_maximums = data.mean(axis=(1, 2, 3))
print(f"Channel means: {channel_maximums}")
# ---

# %% [markdown]
# A dataset can be normalized so that it has a mean of zero and a standard deviation of one, this can be achieved with the following formula:
# $$
# z = \frac{x - \mu}{\sigma}
# $$
# where
# $$
# z: \text{Normalised data point}, \\
# x: \text{Input data point}, \\
# \mu: \text{Dataset mean}, \\
# \sigma: \text{Dataset standard deviation}. \\
# $$
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
#
#   Apply this normalization to each channel of the image data.
#   Verify that the mean and standard deviation of each channel is 0 and 1 respectively.
#   Print the new maximums of the channels.
#
#   <strong>Tip:</strong> Try using the `keepdims` argument to retain singlton dimensions.
# </div>

# %%
# Normalize each channel independently
# --- Exercise
channel_means = data.mean(axis=(1, 2, 3), keepdims=True)
channel_stds = data.std(axis=(1, 2, 3), keepdims=True)
normalized = (data - channel_means) / channel_stds
print(f"Normalized Means: {normalized.mean(axis=(1, 2, 3))}")
print(f"Normalized Std Dev: {normalized.std(axis=(1, 2, 3))}")
print(f"Normalized Maximum: {normalized.max(axis=(1, 2, 3))}")
# ---

# %% [markdown]
# <div style="
#   background: #fff8db;
#   border-left: 6px solid #e2b200;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #8a6a00;
# ">
#   <strong style="color: #8a6a00;">Note</strong><br>
#
#   If the mean of the normalized data is not exactly zero, this will be due to rounding errors in floating point operations (floating point numbers are how fractional numbers are represented in the computer).
# </div>
# %% [markdown]
# #### Projections
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
# #### Creating boolean arrays with inequalities
#
# All the same broadcasting rules apply to inequalities, they will produce a boolean array with elements are `True` where the condition is met and `False` where it is not.
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
#
#   Find where the elements of the array `a` are less than or equal to 4, this is a "scalar operation". Print the results.
# </div>

# %%
a = np.arange(9).reshape(3, 3)
print("Array:")
print(a)

print("\nLess than or equal to 4:")
# Where is `a` less than or equal to 4, print the results
# --- Exercise
result = a <= 4
print(result)
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
#
#   Another useful operation is the element-wise "not" operator `~`, use this on boolean arrays.
#
#   Apply the `~` operator to your result from the previous exercise, print the result.
# </div>

# %%
# --- Exercise
print(~result)
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
#
#   In the 30th z-slice of the nuclei channel of `data`, can you use boolean indexing to select all the pixel values which are greater than the median of that slice? Display the array with `plt.imshow`
# </div>

# %%
a = data[1, 30]

print("Elements greater than the median:")
# --- Exercise
median = np.median(a)
plt.imshow(a > median)
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
#
#   In the display of the boolean array, in what colors are the `True` and `False` values displayed?
# </div>

# %% [markdown]
# ## 6 - Data Types
#
# NumPy’s arrays have data types such as `bool`, `int64`, `float64`, this is a consequence of the underling implementation in the C language.
# Data types determine how much physical memory each element of an array takes up, and what it can represent, e.g. integers or fractional numbers.
#
# Most relevant for working with bio-images are:
# - `uint8`: unsigned integers (whole numbers) from 0 to 255. (1 byte of memory)
# - `uint16`: unsigned integers from 0 to 65,535. (2 bytes of memory)
# - `int64`: signed integers from −9,223,372,036,854,775,808 to 9,223,372,036,854,775,807. (8 bytes of memory)
# - `float32`: approximately ±3.4 × 10³⁸, with about 7 decimal digits of precision. (4 bytes of memory)
# - `float64`: approximately ±1.8 × 10³⁰⁸, with about 15–16 decimal digits of precision. (8 bytes of memory)
# - `bool`: either `True` or `False`.
#
# Most NumPy creational functions will allow you to specify the datatype with a `dtype` argument. You can also call `.astype` method on arrays to get a copy cast as a different type. The `dtype` property of an array can be used to find the data type of the current array.

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
#
#   Use the `dtype` argument to make an array of zeros with the data type `int64`. Print the resulting data type.
# </div>

# %%
# --- Exercise
a = np.zeros((2, 2), dtype=np.int64)
print(f"Datatype: {a.dtype}")
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
#
#   Use the `.astype` method to get a copy of the array `a` with the data type `float64`. Print the data type.
# </div>

# %%
# The default type for `np.arange` is int64
a = np.arange(4)
print(f"Original data type: {a.dtype}")

# --- Exercise
a = a.astype(np.float64)
print(f"New data type: {a.dtype}")
# ---

# %% [markdown]
# Sometimes NumPy will automatically make the result of a mathematical operation have the data type float64.
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
#
#   Divide the array `a` below by 2 and print the data type of the resulting array.
# </div>

# %%
a = np.arange(4, dtype=np.uint16)

print("Original array:")
print(a)
print(f"Data type: {a.dtype}")

# --- Exercise
result = a / 2
print(f"Data type: {result.dtype}")
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
#
#   Now add 2 to the array `a` below, what do you think will be the data type of the result?
# </div>

# %%
a = np.arange(4, dtype=np.uint16)

# --- Exercise
result = a + 2
print(f"Data type: {result.dtype}")
# ---

# %% [markdown]
# ### Watch out! Data overflow ⚠️
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
#
#   Multiply the nuclei channel by 3 and display the result.
# </div>

# %%
nuclei_channel = data[1, 30]

# --- Exercise
result = nuclei_channel * 3
plt.imshow(result)
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
#   Do the results look correct? What do you think has happened?
# </div>

# %% [markdown]
# Something to be careful of is ***data overflow***. Often bio-images will be stored as `uint8` or `uint16`, if you perform mathematical operations on these arrays that cause the values to flow over the maximum range of the data type (255 for `uint8` and 65,535 for `uint16`). Values over the maximum range will wrap around to 0, giving unexpected results. Therefore it is often safest to convert data to floats before doing any analysis.
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
#   Multiply the array below by 3, print the resulting array and the data type. Are all the elements in the resulting array the expected result? If not, which ones and why?
# </div>

# %%
# The maximum value uint8 can store is 255
a = np.array([30, 90, 120], dtype=np.uint8)
print("Original array:")
print(a)

print("\nMultiply by 3:")
# --- Exercise
result = a * 3
print(f"Data type: {result.dtype}")
print(result)
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
#
#   Multiply the nuclei channel by 3, taking steps to prevent data overflow, and display the result.
# </div>

# %%
nuclei_channel = data[1, 30]

# --- Exercise
result = nuclei_channel.astype(np.float64) * 3
plt.imshow(result)
# ---

# %% [markdown]
# ## 7 - Copies and Views
#
# We recommend reading the NumPy [documentation](https://numpy.org/doc/stable/user/basics.copies.html) on copies vs views to see some more examples.
#
# The main thing to watch out for is some NumPy operations will return a copy, and some operations will return a view. If you set the elements in a view, then they will also be changed in the original array that is showing the view.
#
# **Indexing**: Basic indexing will return views, but advanced indexing (boolean and index arrays) will return copies.
#
# **Reshape:** Reshape will always return a view if possible.
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
#
#   In the cell below, set one of the elements in `b` to a new value, what do you think will happen to the equivalent element in `a`?
# </div>

# %%
a = np.arange(9)
b = a.reshape(3, 3)

# --- Exercise
b[1, 1] = 100
# ---

print("\nReshaped array:")
print(b)
print("Original array:")
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
#
#   Again, in the cell below, set one of the elements in `b` to a new value, notice that we use the `.copy` method.
#   Now what do you think will happen to the equivalent element in `a`?
# </div>

# %%
a = np.arange(9)
b = a.reshape(3, 3).copy()

# --- Exercise
b[1, 1] = 100
# ---

print("\nReshaped array:")
print(b)
print("Original array:")
print(a)

# %% [markdown]
# <div style="
#   background: #fff8db;
#   border-left: 6px solid #e2b200;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #8a6a00;
# ">
#   <strong style="color: #8a6a00;">Note:</strong> How can we tell if an array is a copy or a view?<br>
#
# The `base` property can be used, if an array is a view it will return the original array, if it is a copy is will return `None`. Check out NumPy's [documentation](https://numpy.org/doc/stable/user/basics.copies.html#how-to-tell-if-the-array-is-a-view-or-a-copy).
# </div>

# %% [markdown]
# ## 8 - Optional exercises

# %% [markdown]
# ### Line profile
#
# If we select data along a row of an image, we can plot it as a line profile, which can sometimes help us to interpret the data.

# %%
row_idx = 128  # Try changing the row index!
row_data = data[1, 30, row_idx, :]

plt.imshow(data[1, 30])
# plotting the location of the line profile with plt.plot(x, y)
plt.plot([0, 255], [row_idx, row_idx], c="r")

# New figure
plt.figure()
plt.plot(row_data, c="r")
plt.ylim(0, None)  # make sure y-axis starts at zero
plt.title(f"Line profile of row: {row_idx}")

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
#   Extract a column from the 30th z-slice and plot the line profile.
# </div>

# %%
# --- Exercise
column_idx = 128  # Try changing the row index!
row_data = data[1, 30, :, column_idx]

plt.imshow(data[1, 30])
# plotting the location of the line profile with plt.plot(x, y)
plt.plot([column_idx, column_idx], [0, 255], c="r")

# New figure
plt.figure()
plt.plot(row_data, c="r")
plt.ylim(0, None)  # make sure y-axis starts at zero
plt.title(f"Line profile of column: {column_idx}")
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
#   From the line profiles above, can you estimate the intensity value of the background?
# </div>
#

# %% [markdown]
# ### Meshgrid (Optional)
#
# We can use indexing notation on `np.mgrid` to produce the row and column (or higher dimension) coordinates for each element.
# We can then use the coordinates to calculate inequalities based on the coordinate position, for example:

# %%
# ii is the row coordinates with values between [-128, 128)
# jj is the column coordinates with values between [-128, 128)
# both ii and jj have the shapes (256, 256)
ii, jj = np.mgrid[-128:128, -128:128]

fig, axes = plt.subplots(1, 2)
axes[0].imshow(ii)
axes[1].imshow(jj)
axes[0].set_title("Row coordinates")
axes[1].set_title("Column coordinates")

# %% [markdown]
# We can create a boolean mask of a circle by using the circle equation:
# $$
# x^2 + y^2 \leq R
# $$
# Where $R$ is the radius

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
#   Create a circular mask centered on one of the nuclei in the 30th z-slice, and set all of the pixels outside the circle to zero.
#   <details>
#   <summary>❓ <strong>Hint</strong></summary>
#     You can use the coordinates (row=156, column=112), and a diameter of 52. What is the equation of a circle with the center at the coordinates (a, b)?
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
