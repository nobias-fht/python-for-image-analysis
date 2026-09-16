# %% [markdown]
# # Module 7: data analysis and visualization
#
# Time: 1 hour 45 minutes.
#
# <div style="display: flex; align-items: center; gap: 12px;">
#     <img src="https://raw.githubusercontent.com/pandas-dev/pandas/main/web/pandas/static/img/pandas.svg" alt="Logo" style="height: 40px; width: auto;">
#     pandas
# </div>
#
# `pandas` is the standard library for tabular data in Python. Its `DataFrame` is
# a table with named columns, each column holding one type, and it is usually the best
# choice for the output of a measurement step.
#
# If in doubt, always check out the [user documentation](https://pandas.pydata.org/docs/user_guide/index.html#user-guide).
#
# ### Question
#
# How do we go from a table of measurements to a figure?
#
# ### Objective
#
# - Load, select and combine measurement tables
# - Draw the plots you will use most: line plot, box plot, scatter plot
# - Fit a curve to your data with `scipy`

# %% [markdown]
# ## 1 - Loading a table
#
# Oftentimes, a pipeline will result in measurements, as we've seen during the practical. Here,
# we will assume that some measurements were created and saved to .csv files.
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
#
#   Read the first file into a dataframe (`pd.read_csv`) and show its first rows (`dataframe.head()`).
# </div>

# %%
import pandas as pd
from python_for_ia import get_measurement_paths

files = get_measurement_paths()
print(files)

# --- Exercise
# Read the first CSV file and show the first rows
table = pd.read_csv(files[0])
table.head()
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
#   What does one row describe? And one column? How do you reckon these measurements were obtained?
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
#   Before trusting a table, look at it. How many objects? Which columns, and of
#   what type? What are the ranges of the measurements?
#
#   <b>Hint</b>: "shape", "columns" and "dtypes" are attributes, "info()" and
#   "describe()" are methods.
# </div>

# %%
# --- Exercise
# Inspect the table
print(f"Rows and columns: {table.shape}")
print(f"Columns: {list(table.columns)}")

table.info()
table.describe()
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
#   Look at the minimum and the maximum of each column. Does any of them look
#   impossible for an object you would want to keep?
# </div>

# %% [markdown]
# ## 2 - Selecting rows and columns
#
# As you can imagine, Dataframes can be very large and in order to explore them, we also need
# to select only certain elements. For instance, to select one or more columns you
# can pass their names as a list of string in `table[...]`.
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
#   Select two columns from the dataframe.
# </div>
#
#
#

# %%
# --- Exercise
table[["label", "area"]]
# ---

# %% [markdown]
# More interesting is to be able to select conditionally certain rows. A condition on a column gives one `True` or `False` per row. Passing it to
# the `.loc` method keeps the rows that are `True`.
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
#   Use the condition to select a subset of the table.
# </div>
#

# %%
# condition
is_large = table["area"] > 1000

# --- Exercise
large_objects = table.loc[is_large]
print(f"{len(large_objects)} objects out of {len(table)} are larger than 1000 px")
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
#   Select the label and area of the objects larger than 1000 pixels that do not
#   touch the border, sorted by decreasing area. Built it one condition at a time!
#
#   <b>Hint</b>: combine conditions with "&" (and) and "~" (not), each condition surrounded by parenthesis. Sort with "sort_values(by=..., ascending=False)".
# </div>

# %%
# --- Exercise
# Select and sort
selected = table.loc[
    (table["area"] > 1000) & (~table["on_border"]),
    ["label", "area"],
]
selected = selected.sort_values(by="area", ascending=False)
selected.head()
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
#   We've used the logical AND (&) and NOT (~), what is OR?
# </div>

# %% [markdown]
# ## 3 - Concatenation and merging
#
# In the case of our example, we have loaded a single file pertaining to a single image.
# But we actually have many frames and all these results should be gathered within the same
# dataframe. Among the operations we can perform on a dataframe, we can use `pd.concat`
# to stacks them into a single, larger table.
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
#   Read all the files and concatenate them into one dataframe called "measurements".
#
#   <b>Hint</b>: build a list of dataframes, then call
#   `pd.concat(tables, ignore_index=True)`.
# </div>

# %%
# --- Exercise
# Read every file and concatenate
tables = [pd.read_csv(file) for file in files]
measurements = pd.concat(tables, ignore_index=True)
# ---

print(f"{len(measurements)} objects in {len(files)} images")
measurements.head()

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
#   Labels start again at 1 in every image. After concatenating, what identifies
#   an object uniquely?
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
#   Let's say we now want to add metadata from the images that were not in the original
#   result tables.
#
#   Merge the metadata into the measurements on "image_id".
#
#   <b>Hint</b>: "pd.merge(left, right, on=...)". An area is a length squared.
# </div>

# %%
# add metadata to the dataframe
z_slices = [24, 28, 32, 36, 40, 44]
metadata = pd.DataFrame(
    {
        "image_id": [f"image_{index:02d}" for index in range(len(z_slices))],
        "z_slice": z_slices,
        "pixel_size_um": 0.26,  # voxel size of cells3d, in micrometers
    }
)

# --- Exercise
# Merge, then convert to micrometers
measurements = pd.merge(measurements, metadata, on="image_id")
# ---

measurements.head()


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
#   How many rows does "measurements" have now? Should merging metadata ever
#   change that number?
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
#   We can also create new columns similarly to new dictionary entries. Let's use the newly added metadata to convert areas
#   and perimeters into physical units.
# </div>

# %%
# --- Exercise
measurements["area_um2"] = measurements["area"] * measurements["pixel_size_um"] ** 2
measurements["perimeter_um"] = measurements["perimeter"] * measurements["pixel_size_um"]
# ---

measurements[["image_id", "label", "area", "area_um2"]].head()

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
#   A dataframe can mix pixels, micrometers and arbitrary units while looking
#   perfectly valid. Putting the unit in the column name, as in "area_um2", costs
#   nothing.
# </div>

# %% [markdown]
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
#   Add two columns to "measurements": the "ellipticity" of each object, and the
#   ratio of its mean membrane intensity over its mean nuclei intensity.
# </div>
#
# $$\epsilon = 1 - \frac{A_{minor}}{A_{major}}$$
#
# where $A_{minor} corresponds to `"axis_minor_lenth"`, and $A_{major}$ to its major counterpart.

# %%
# --- Exercise
# Add the two columns
measurements["ellipticity"] = (
    1 - measurements["axis_minor_length"] / measurements["axis_major_length"]
)
measurements["intensity_ratio"] = (
    measurements["mean_intensity_membrane"] / measurements["mean_intensity_nuclei"]
)
# ---

measurements[["image_id", "label", "ellipticity", "intensity_ratio"]].head()

# %% [markdown]
# ## 4 - Summarizing per image
#
# `groupby` splits the table into groups, computes something on each, and puts
# the results back together. It answers "one number per image", or per condition.

# %%
per_image = (
    measurements.groupby(["image_id", "z_slice"])
    .agg(
        n_objects=("label", "count"),
        mean_area_um2=("area_um2", "mean"),
        median_ellipticity=("ellipticity", "median"),
        mean_membrane=("mean_intensity_membrane", "mean"),
        mean_nuclei=("mean_intensity_nuclei", "mean"),
    )
    .reset_index()
)
per_image

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
#   "agg" is not limited to "mean" and "median". Can you find in the pandas
#   documentation which functions it accepts?
# </div>
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
#   This summary has one row per image. What
#   would you need before putting any of these numbers in a paper?
# </div>

# %% [markdown]
# ## 5 - Ordered measurements: the line plot
#
# We can use the dataframe to plot particular aspects of the measurements.
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
#   Let's plot mean intensity of each channel over the Z slice. If we are not interested in
#   comparing absolute intensities but rate of changes, what is the issue with this plot?
# </div>

# %%
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)

ax.plot(
    per_image["z_slice"],
    per_image["membrane_relative"],
    marker="o",
    label="membrane",
)
ax.plot(
    per_image["z_slice"],
    per_image["nuclei_relative"],
    marker="o",
    label="nuclei",
)
ax.legend()
ax.set_xlabel("z slice")
ax.set_ylabel("Mean intensity, relative to the first slice")
ax.set_title("Signal with depth")
plt.show()

# %% [markdown]
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
#   Create two new columns in the dataframe that would allow us to plot the relative rates of changes
#   and plot them for each channel.
# </div>

# %%
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)

# --- Exercise
# Normalize each channel, then draw one line per channel
per_image["membrane_relative"] = (
    per_image["mean_membrane"] / per_image["mean_membrane"].iloc[0]
)
per_image["nuclei_relative"] = (
    per_image["mean_nuclei"] / per_image["mean_nuclei"].iloc[0]
)

ax.plot(
    per_image["z_slice"],
    per_image["membrane_relative"],
    marker="o",
    label="membrane",
)
ax.plot(
    per_image["z_slice"],
    per_image["nuclei_relative"],
    marker="o",
    label="nuclei",
)
ax.legend()
# ---

ax.set_xlabel("z slice")
ax.set_ylabel("Mean intensity, relative to the first slice")
ax.set_title("Signal with depth")
plt.show()

# %% [markdown]
# ## 6 - Distributions: the box plot
#
# The box spans the first to the third quartile, the line is the median, the
# whiskers reach the points within 1.5 interquartile ranges, and the rest is
# drawn as individual points.
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
#   Plot the distribution of nuclear area, one box per image.
#
#   <b>Hint</b>: "ax.boxplot" takes a list of arrays, one per box. Looping over
#   "measurements.groupby("image_id")" gives pairs of (name, sub-dataframe).
# </div>

# %%
fig, ax = plt.subplots(figsize=(7, 4), constrained_layout=True)

# --- Exercise
# Build one group of values per image, then plot the boxes
names = []
groups = []
for name, group in measurements.groupby("image_id"):
    names.append(name)
    groups.append(group["area_um2"])

ax.boxplot(groups, tick_labels=names)
# ---

ax.set_ylabel("Nuclear area (um2)")
ax.set_title("Area distribution per image")
plt.show()

# %% [markdown]
# The same plot, grouped by a property of the objects instead. Objects touching
# the border are cut off by the field of view, and the pipeline flagged them.
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
#   Compare the area of the border objects with the others, and overlay the
#   individual points.
#
#   <b>Hint</b>: the boxes sit at x = 1 and x = 2. Add jitter so the points do
#   not pile up: "rng.normal(1, 0.04, size=len(values))".
# </div>

# %%
import numpy as np

rng = np.random.default_rng(42)

border = measurements.loc[measurements["on_border"], "area_um2"]
interior = measurements.loc[~measurements["on_border"], "area_um2"]

fig, ax = plt.subplots(figsize=(5, 4), constrained_layout=True)

# --- Exercise
# Box plot with the individual points on top
ax.boxplot([border, interior], tick_labels=["on border", "interior"])

for position, values in enumerate([border, interior], start=1):
    jitter = rng.normal(position, 0.04, size=len(values))
    ax.scatter(jitter, values, s=10, alpha=0.5, color="black", zorder=3)
# ---

ax.set_ylabel("Nuclear area (um2)")
ax.set_title("Border and interior objects")
plt.show()

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
#   The border objects sit a little lower, but the distributions overlap a lot.
#   Is that shift the reason to drop them?
# </div>

# %%
# --- We keep the interior objects for the rest of the module
# ".copy()" because we will add columns to this selection later.
objects = measurements.loc[~measurements["on_border"]].copy()

print(f"{len(objects)} objects kept out of {len(measurements)}")

# %% [markdown]
# ## 8 - Relationships: the scatter plot
#
# A box plot shows one variable, a scatter plot two, and a color code adds a
# third.
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
#   Plot the perimeter of each nucleus against its area, colored by ellipticity,
#   with a colorbar.
#
#   <b>Hint</b>: "ax.scatter(x, y, c=..., cmap="viridis")" returns the points,
#   which "fig.colorbar(...)" needs.
# </div>

# %%
fig, ax = plt.subplots(figsize=(6, 4.5), constrained_layout=True)

# --- Exercise
# Scatter plot, color coded by a third column
points = ax.scatter(
    objects["area_um2"],
    objects["perimeter_um"],
    c=objects["ellipticity"],
    cmap="viridis",
    s=20,
    alpha=0.8,
)

colorbar = fig.colorbar(points, ax=ax)
colorbar.set_label("Ellipticity")
# ---

ax.set_xlabel("Area (um2)")
ax.set_ylabel("Perimeter (um)")
plt.show()

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
#   The points follow a curve, not a line. What relationship do you expect between
#   the area and the perimeter of a compact shape?
# </div>

# %% [markdown]
# ## 9 - Fitting a curve
#
# Fitting estimates the parameters of a model we have a reason to believe in. For
# shapes that are all roughly similar, doubling every length multiplies the
# perimeter by 2 and the area by 4, so we expect
#
# $$ P = a \cdot A^{b} \quad \text{with} \quad b = 0.5 $$
#
# `curve_fit` takes a function whose first argument is the x data, and whose
# other arguments are the parameters to estimate.


# %%
def power_law(area, a, b):
    return a * area**b


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
#   Fit the model, and print the parameters with their uncertainty.
#
#   <b>Hint</b>: "curve_fit(model, x, y, p0=[...])" returns the parameters and
#   their covariance matrix. The standard errors are
#   "np.sqrt(np.diag(covariance))".
# </div>

# %%
from scipy.optimize import curve_fit

area = objects["area_um2"].to_numpy()
perimeter = objects["perimeter_um"].to_numpy()

# --- Exercise
# Fit the model and report the parameters
parameters, covariance = curve_fit(power_law, area, perimeter, p0=[3.5, 0.5])
errors = np.sqrt(np.diag(covariance))

print(f"a = {parameters[0]:.2f} +/- {errors[0]:.2f}")
print(f"b = {parameters[1]:.3f} +/- {errors[1]:.3f}")
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
#   Draw the fitted curve over the data, and the residuals next to it.
#
#   <b>Hint</b>: evaluate the model on
#   "np.linspace(area.min(), area.max(), 200)". A residual is a measurement minus
#   the model at the same point.
# </div>

# %%
fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)

# --- Exercise
# Left: data and fitted curve. Right: residuals.
smooth_area = np.linspace(area.min(), area.max(), 200)

axes[0].scatter(area, perimeter, s=20, alpha=0.6, label="objects")
axes[0].plot(
    smooth_area,
    power_law(smooth_area, *parameters),
    color="crimson",
    label=f"fit: b = {parameters[1]:.2f}",
)
axes[0].legend()

residuals = perimeter - power_law(area, *parameters)

axes[1].axhline(0, color="black", linewidth=1)
axes[1].scatter(area, residuals, s=20, alpha=0.6)
# ---

axes[0].set_xlabel("Area (um2)")
axes[0].set_ylabel("Perimeter (um)")
axes[1].set_xlabel("Area (um2)")
axes[1].set_ylabel("Residual (um)")

plt.show()

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
#   Is the exponent compatible with 0.5? Do the residuals drift with the area, or
#   scatter around zero?
# </div>
#
# ### Conclusion
#
# <details>
#   <summary>What does the fit tell us?</summary>
#
#   <ul>
#     <li>An exponent near 0.5 means the nuclei are one family of shapes seen at
#     different sizes, not shapes that grow more convoluted.</li>
#     <li>Ours lands just below 0.5, by more than its uncertainty. A pixelated
#     boundary overestimates the perimeter, relatively more for small objects,
#     which flattens the curve. The measurement sets that limit, not the
#     biology.</li>
#     <li>The residuals do not drift, but a few sit far above the rest: the
#     elongated objects, already visible in the color code of section 8.</li>
#   </ul>
# </details>
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
#   "curve_fit" walks downhill from the initial guess "p0", and a bad guess can
#   settle on a meaningless minimum. Always plot the fit: a convincing curve can
#   still be the wrong model.
# </div>

# %% [markdown]
# ## Optional exercises

# %% [markdown]
# ### Correlations
#
# <div style="
#   background: #f3f4f6;
#   border-left: 6px solid #6b7280;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #374151;
# ">
#   <strong>Optional Exercise</strong><br>
#   How correlated are the area and the mean nuclei intensity? Compute the
#   Pearson and the Spearman coefficients with "scipy.stats". What do they tell us?
# </div>

# %%
from scipy import stats

# --- Exercise
# Pearson and Spearman correlations
pearson = stats.pearsonr(objects["area_um2"], objects["mean_intensity_nuclei"])
spearman = stats.spearmanr(objects["area_um2"], objects["mean_intensity_nuclei"])

print(f"Pearson:  r = {pearson.statistic:.3f}, p = {pearson.pvalue:.3g}")
print(f"Spearman: r = {spearman.statistic:.3f}, p = {spearman.pvalue:.3g}")
# ---

# %% [markdown]
# <details>
#   <summary>Pearson or Spearman?</summary>
#
#   <ul>
#     <li><strong>Pearson</strong> measures how well a straight line fits, and is
#     sensitive to outliers.</li>
#     <li><strong>Spearman</strong> works on the ranks, so it only asks whether
#     one variable increases with the other.</li>
#   </ul>
# </details>

# %% [markdown]
# ### Principal component analysis
#
# <div style="
#   background: #f3f4f6;
#   border-left: 6px solid #6b7280;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #374151;
# ">
#   <strong>Optional Exercise</strong><br>
#   A principal component analysis projects the objects onto the directions
#   carrying the most variance, which is a quick way to look at every column at
#   once. Standardize the columns below, run a PCA, and plot the first two
#   components.
#
#   <b>Hint</b>: a PCA is a singular value decomposition of the standardized
#   table, "u, s, vt = np.linalg.svd(standardized, full_matrices=False)". The
#   coordinates are "u * s", and the variance of each component is proportional
#   to "s ** 2".
# </div>

# %%
features = [
    "area_um2",
    "perimeter_um",
    "ellipticity",
    "eccentricity",
    "mean_intensity_nuclei",
    "intensity_ratio",
]
values = objects[features].to_numpy()

# --- Exercise
# Standardize, decompose, and plot the first two components
standardized = (values - values.mean(axis=0)) / values.std(axis=0)

u, s, vt = np.linalg.svd(standardized, full_matrices=False)
components = u * s
explained = s**2 / np.sum(s**2)

pca_fig, ax = plt.subplots(figsize=(6, 4.5), constrained_layout=True)

points = ax.scatter(
    components[:, 0],
    components[:, 1],
    c=objects["area_um2"],
    cmap="viridis",
    s=20,
    alpha=0.8,
)

colorbar = pca_fig.colorbar(points, ax=ax)
colorbar.set_label("Area (um2)")

ax.set_xlabel(f"PC1 ({100 * explained[0]:.0f}% of variance)")
ax.set_ylabel(f"PC2 ({100 * explained[1]:.0f}% of variance)")
plt.show()
# ---

# %% [markdown]
# ### Finding groups without labels
#
# PCA spread the objects along the directions in which they differ most, but it
# did not say which objects belong together. Clustering does.
#
# "scipy.cluster.hierarchy" builds a tree by repeatedly merging the two closest
# groups, then cuts that tree into as many groups as we ask for.
#
# <div style="
#   background: #f3f4f6;
#   border-left: 6px solid #6b7280;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #374151;
# ">
#   <strong>Optional Exercise</strong><br>
#   Build the tree on the standardized features with "linkage", then cut it into
#   three groups with "fcluster".<br>
#
#   <b>Hint</b>: "linkage(standardized, method="ward")" and
#   "fcluster(link, n, criterion="maxclust")".
# </div>

# %%
from scipy.cluster import hierarchy

# --- Exercise
# Build the tree and cut it into three groups
link = hierarchy.linkage(standardized, method="ward")
objects["cluster"] = hierarchy.fcluster(link, 3, criterion="maxclust")
# ---

print(objects["cluster"].value_counts().to_string())

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
#   Why do we cluster "standardized" rather than the raw columns?
# </div>
#
# Ward groups objects that are close together, and it measures closeness by
# adding up the difference in every column. Our columns are not on the same
# scale: area is around 100 um2, mean intensity around 15000. A difference in
# intensity is therefore about a hundred times bigger than a difference in
# area, so on the raw table intensity would decide the groups on its own.
#
# Standardizing rescales each column to a mean of 0 and a standard deviation of
# 1. A difference of 1 then means the same thing in every column.

# %% [markdown]
# A cluster label on its own is just a number. To find out what separates the
# two groups, summarize the measurements per cluster, exactly as we summarized
# per image in section 5.

# %%
objects.groupby("cluster")[
    ["area_um2", "perimeter_um", "ellipticity", "mean_intensity_nuclei"]
].mean().round(2)

# %% [markdown]
# The three groups are readable. Cluster 3 is large and round, cluster 2 is
# medium and elongated, and cluster 1 is a tight group of ten small, unusually
# bright objects: 29 to 61 um2 against a median of 108.
#
# We can see the same three groups on the PCA projection, by reusing the scatter
# of the previous exercise and coloring by cluster instead of by area.

# %%
fig, ax = plt.subplots(figsize=(6, 5), constrained_layout=True)
for label, group in objects.groupby("cluster"):
    ax.scatter(
        components[objects["cluster"] == label, 0],
        components[objects["cluster"] == label, 1],
        label=f"cluster {label}",
        alpha=0.8,
    )
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_title("Clusters on the principal components")
ax.legend()

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
#   Cluster 1 is ten small, bright objects. What are they?
# </div>
#
# Two explanations fit. Chromatin condenses during mitosis, so a dividing
# nucleus really is smaller and brighter. But a watershed that splits one
# nucleus down the middle also leaves small, bright pieces.
#
# Both produce the same numbers, so the table cannot choose between them. What
# it can do is tell us where to look: select the rows, then use "image_id" and
# "label" to find these ten objects in the images.

# %%
suspects = objects.loc[objects["cluster"] == 1, ["image_id", "label", "area_um2"]]
suspects.sort_values("area_um2").head()

# %% [markdown]
# One thing the table can settle on its own is whether cluster 1 is an artifact
# of how we acquired the data. "pd.crosstab" counts the objects in every
# combination of two columns, here cluster against depth.

# %%
pd.crosstab(objects["z_slice"], objects["cluster"])

# %% [markdown]
# All three clusters appear at every depth, so cluster 1 is not an effect of
# where we stopped slicing.
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
#   "fcluster" returns the number of groups you ask for, whether or not the data
#   contains them. Nothing here proves there are three. Ask for two and you get
#   the ten small objects against everything else; ask for four and the large
#   round group splits in two. Always look at what the groups contain, as we did
#   above, before believing in them.
# </div>

# %% [markdown]
# ### Saving your results
#
# <div style="
#   background: #f3f4f6;
#   border-left: 6px solid #6b7280;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #374151;
# ">
#   <strong>Optional Exercise</strong><br>
#   Save the per-image summary as a CSV and the PCA figure as a PNG, both into a
#   "results" folder.
#
#   <b>Hint</b>: "to_csv(path, index=False)" and
#   "savefig(path, dpi=200, bbox_inches="tight")".
# </div>

# %%
from pathlib import Path

results = Path("scratch_outputs/results")

# --- Exercise
# Save the summary table and the PCA figure
results.mkdir(parents=True, exist_ok=True)

per_image.to_csv(results / "per_image_summary.csv", index=False)
pca_fig.savefig(results / "pca.png", dpi=200, bbox_inches="tight")
# ---

print(f"Saved to {results.resolve()}")

# %% [markdown]
# ## Summary
#
# In this module we turned a folder of per-image measurements into a single
# table, and the table into figures. We loaded and inspected it, selected rows
# and columns, concatenated the images and merged in the metadata the pipeline
# did not know, derived new columns, and summarized per image with "groupby".
#
# We then created 4 useful plots which help us to answer different
# questions: a line plot for measurements that have an order, a box
# plot for a distribution, a scatter plot for two variables at once with a third
# in the color, and a fitted curve when a model is worth testing against the
# data.
#
# The optional exercises help us to describe the objects and look for
# for structure among them with correlations, as well as PCA and a clustering.
#
# More interesting ways to analyse and visualize data:
#
