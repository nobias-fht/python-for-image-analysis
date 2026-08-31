# %% [markdown]
# # Module 7: data analysis and visualization
#
# Time: 1 hour 45 minutes.
#
# An analysis pipeline ends on a table: one row per object, one column per
# measurement. That table is the raw material, not the result. In this module we
# turn it into an answer.
#
# <div style="display: flex; align-items: center; gap: 12px;">
#     <img src="https://raw.githubusercontent.com/pandas-dev/pandas/main/web/pandas/static/img/pandas.svg" alt="Logo" style="height: 40px; width: auto;">
# </div>
#
# `pandas` is the standard library for tabular data in Python. Its `DataFrame` is
# a table with named columns, each column holding one type, and it is the natural
# home for the output of a measurement step.
#
# ### Question
#
# How do we go from a table of measurements to a figure?
#
# ### Objective
#
# - Load, select and combine measurement tables
# - Draw the three plots you will use most: box plot, scatter plot, fitted curve
# - Fit a model to your data with `scipy`

# %% [markdown]
# ## 1 - From images to a table
#
# We work on `cells3d`, a two-channel acquisition from the scikit-image sample
# Segmenting a few of its z-slices and measuring both channels
# gives us the table for this module.


# %%
# --- Import what we need
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import ndimage as ndi
from skimage import data, feature, filters, measure, morphology, segmentation

# %%
image = data.cells3d()

print(f"Image shape: {image.shape}")

# %% [markdown]
# The pipeline below is the one from this morning: filter, threshold, clean up,
# separate, measure. Read it, but do not retype it.


# %%
def measure_slice(membrane, nuclei):
    """Segment the nuclei of one slice and measure both channels."""
    # segment, as in module 5
    smoothed = filters.gaussian(nuclei, sigma=2, preserve_range=True)
    mask = smoothed > filters.threshold_otsu(smoothed)
    mask = morphology.remove_small_objects(mask, min_size=200)
    mask = ndi.binary_fill_holes(mask)

    # separate touching nuclei with a watershed
    distance = ndi.distance_transform_edt(mask)
    peaks = feature.peak_local_max(distance, min_distance=20, labels=mask)
    markers = np.zeros(mask.shape, dtype=int)
    markers[tuple(peaks.T)] = np.arange(1, len(peaks) + 1)
    labels = segmentation.watershed(-distance, markers, mask=mask)
    labels = morphology.remove_small_objects(labels, min_size=200)

    # measure both channels at once, by stacking them along the last axis
    table = pd.DataFrame(
        measure.regionprops_table(
            labels,
            intensity_image=np.stack([membrane, nuclei], axis=-1),
            properties=(
                "label",
                "area",
                "perimeter",
                "eccentricity",
                "axis_major_length",
                "axis_minor_length",
                "intensity_mean",
            ),
        )
    )
    table = table.rename(
        columns={
            "intensity_mean-0": "mean_intensity_membrane",
            "intensity_mean-1": "mean_intensity_nuclei",
        }
    )

    # objects touching the image border are truncated, flag them
    interior = np.unique(segmentation.clear_border(labels))
    table["on_border"] = ~table["label"].isin(interior)

    return table


# %% [markdown]
# A pipeline saves its results to disk, one file per image. Let's do the same.

# %%
folder = Path("scratch_outputs/module_07")
folder.mkdir(parents=True, exist_ok=True)

z_slices = [24, 28, 32, 36, 40, 44]

for index, z in enumerate(z_slices):
    table = measure_slice(image[z, 0], image[z, 1])
    table.insert(0, "image_id", f"image_{index:02d}")
    table.to_csv(folder / f"image_{index:02d}.csv", index=False)

files = sorted(folder.glob("*.csv"))
print(f"{len(files)} files written")

# %% [markdown]
# ## 2 - Loading a table
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
#   Read the first file into a dataframe and show its first rows.
#
#   <b>Hint</b>: "pd.read_csv" takes a path, and every dataframe has a "head()".
# </div>

# %%
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
#   What does one row describe? And one column?
# </div>
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
# ## 3 - Selecting rows and columns
#
# Three ways of asking for a piece of a table cover most of what we need:
#
# - `table["area"]` returns one column, as a `Series`,
# - `table[["label", "area"]]` returns several columns, as a dataframe,
# - `table.loc[<rows>, <columns>]` returns both, where `<rows>` is a condition.

# %%
print(type(table["area"]))
print(type(table[["label", "area"]]))

print(f"Mean area: {table['area'].mean():.1f} pixels")

# %% [markdown]
# A condition on a column gives one `True` or `False` per row. Passing it to
# `.loc` keeps the rows that are `True`, exactly like the boolean masks we used
# on NumPy arrays in module 2.

# %%
is_large = table["area"] > 1000
print(is_large.head())

large_objects = table.loc[is_large]
print(f"{len(large_objects)} objects out of {len(table)} are larger than 1000 px")

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
#   What did the comparison return, and how many entries does it have? Compare
#   that with the length of "large_objects".
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
#   Select the label and area of the objects larger than 1000 pixels that do not
#   touch the border, sorted by decreasing area.
#
#   <b>Hint</b>: combine conditions with "&" and "~", each in its own
#   parentheses. Sort with "sort_values(by=..., ascending=False)".
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
#   background: #fff8db;
#   border-left: 6px solid #e2b200;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #8a6a00;
# ">
#   <strong style="color: #8a6a00;">Note</strong><br>
#   The parentheses are not optional, "&" binds more tightly than ">". And on
#   columns you need "&", "|", "~", not "and", "or", "not".
# </div>

# %% [markdown]
# Creating a column works like assigning to a dictionary key, on the whole column
# at once and without a `for` loop.
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
#   Add two columns: the "ellipticity" of each object, and the ratio of its mean
#   membrane intensity over its mean nuclei intensity.
#
#   <b>Hint</b>: ellipticity is "1 - minor axis / major axis", so a circle gives
#   0. You need "axis_major_length", "axis_minor_length",
#   "mean_intensity_membrane" and "mean_intensity_nuclei".
# </div>

# %%
# --- Exercise
# Add the two columns
table["ellipticity"] = 1 - table["axis_minor_length"] / table["axis_major_length"]
table["intensity_ratio"] = (
    table["mean_intensity_membrane"] / table["mean_intensity_nuclei"]
)
# ---

table[["label", "ellipticity", "intensity_ratio"]].head()

# %% [markdown]
# ## 4 - Putting tables together
#
# One image is never enough. Our files share the same columns, so `pd.concat`
# stacks them into a single, longer table.
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
#   Read all the files and concatenate them into one dataframe, "measurements".
#
#   <b>Hint</b>: build a list of dataframes, then call
#   "pd.concat(tables, ignore_index=True)".
# </div>

# %%
# --- Exercise
# Read every file and concatenate
tables = [pd.read_csv(file) for file in files]
measurements = pd.concat(tables, ignore_index=True)
# ---

print(f"{len(measurements)} objects in {len(files)} images")
print(measurements["image_id"].value_counts())

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
# Everything the microscope knew and the pipeline did not lives in a separate
# table. `pd.merge` joins the two on a shared column: each object gets the
# metadata of the image it came from.

# %%
metadata = pd.DataFrame(
    {
        "image_id": [f"image_{index:02d}" for index in range(len(z_slices))],
        "z_slice": z_slices,
        "pixel_size_um": 0.26,  # voxel size of cells3d, in micrometers
    }
)
metadata

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
#   Merge the metadata into the measurements on "image_id", then convert areas
#   and perimeters into physical units.
#
#   <b>Hint</b>: "pd.merge(left, right, on=...)". An area is a length squared.
# </div>

# %%
# --- Exercise
# Merge, then convert to micrometers
measurements = pd.merge(measurements, metadata, on="image_id")

measurements["area_um2"] = measurements["area"] * measurements["pixel_size_um"] ** 2
measurements["perimeter_um"] = measurements["perimeter"] * measurements["pixel_size_um"]
# ---

measurements[["image_id", "label", "area", "area_um2"]].head()

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
# <div style="
#   background: #accffb;
#   border-left: 6px solid #2f80ed;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #21457f;
# ">
#   <strong style="color: #21457f;">Exercise</strong><br>
#   "measurements" was built from the files, so the two columns of section 3 are
#   gone. Add them again, this time to "measurements".
# </div>

# %%
# --- Exercise
# Add the columns to the concatenated table
measurements["ellipticity"] = (
    1 - measurements["axis_minor_length"] / measurements["axis_major_length"]
)
measurements["intensity_ratio"] = (
    measurements["mean_intensity_membrane"] / measurements["mean_intensity_nuclei"]
)
# ---

# %% [markdown]
# ## 5 - Summarizing per image
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
#   This summary has one row per image, all from a single acquisition. What
#   would you need before putting any of these numbers in a paper?
# </div>

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
import matplotlib.pyplot as plt

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
# <div style="
#   background: #e8f7ec;
#   border-left: 6px solid #2f9e44;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #1f5f2c;
# ">
#   <strong style="color: #1f5f2c;">Question</strong><br>
#   Can you tell, from the boxes alone, how many objects each one summarizes?
# </div>

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
# ".copy()" because we will add columns to this selection later on
objects = measurements.loc[~measurements["on_border"]].copy()

print(f"{len(objects)} objects kept out of {len(measurements)}")

# %% [markdown]
# ## 7 - Ordered measurements: the line plot
#
# A line plot is for measurements that have an order: a time course, a dose, or
# here a position in the stack. Each call to `plot` adds one line to the axes.
#
# Our two channels are ten times apart in absolute intensity, so sharing an axis
# would flatten one of them. Dividing each by its value in the first slice puts
# them on a common scale, and asks how much each one changed rather than how
# large it is.
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
#   Add a column per channel holding its mean intensity divided by the value in
#   the first slice, then plot both against "z_slice", with a marker on every
#   point.
#
#   <b>Hint</b>: ".iloc[0]" gives the first value of a column. Call "ax.plot"
#   twice, passing "label=" so that "ax.legend()" can name the lines, and
#   "marker="o"" to draw the points.
# </div>

# %%
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
#   The points follow a curve, not a line. What relation do you expect between
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
#     <li>A p-value on objects from one acquisition says nothing about
#     biological reproducibility.</li>
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

fig, ax = plt.subplots(figsize=(6, 4.5), constrained_layout=True)

points = ax.scatter(
    components[:, 0],
    components[:, 1],
    c=objects["area_um2"],
    cmap="viridis",
    s=20,
    alpha=0.8,
)

colorbar = fig.colorbar(points, ax=ax)
colorbar.set_label("Area (um2)")

ax.set_xlabel(f"PC1 ({100 * explained[0]:.0f}% of variance)")
ax.set_ylabel(f"PC2 ({100 * explained[1]:.0f}% of variance)")
plt.show()
# ---

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
#   An analysis you cannot share is not finished. Save the summary of section 5
#   as a CSV file, and the last figure as a PNG.
#
#   <b>Hint</b>: "to_csv(path, index=False)" and
#   "fig.savefig(path, dpi=200, bbox_inches="tight")".
# </div>

# %%
results = Path("scratch_outputs/results")

# --- Exercise
# Save the summary table and the figure
results.mkdir(parents=True, exist_ok=True)

per_image.to_csv(results / "per_image_summary.csv", index=False)
fig.savefig(results / "pca.png", dpi=200, bbox_inches="tight")
# ---

print(f"Saved to {results.resolve()}")

# %% [markdown]
# ## Summary
# what's the next module?
# Tying this module into data visualization which comes next
#
