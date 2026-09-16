# %% [markdown]
# # Module 7: data analysis and visualization
#
# Time: 1 hour 45 minutes.
#
# `pandas` is the standard library for tabular data in Python. Its `DataFrame` is
# a table with named columns, each column holding one type, and it is usually the best
# choice for the output of a measurement step.
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
# ## 1 - From images to a table

# %%
from python_for_ia import make_two_channel_cells

image, _, _ = make_two_channel_cells(seed=100)
print(f"Field shape: {image.shape}")

# %% [markdown]
# The pipeline below is the one from this morning: threshold the combined
# signal, separate touching cells with a watershed, then measure both channels
# at once. Read it, but do not retype it.


# %%
import numpy as np
import pandas as pd
from scipy import ndimage as ndi
from skimage import feature, filters, measure, morphology, segmentation


def measure_frame(channel_a, channel_b):
    """Segment the cells of one field and measure both channels."""
    # segment on the combined signal, as in this morning's practical
    combined = channel_a + channel_b
    mask = combined > filters.threshold_otsu(combined)
    mask = morphology.remove_small_objects(mask, max_size=39)
    mask = ndi.binary_fill_holes(mask)

    # separate touching cells with a watershed
    distance = ndi.distance_transform_edt(mask)
    peaks = feature.peak_local_max(distance, min_distance=10, labels=mask)
    markers = np.zeros(mask.shape, dtype=int)
    markers[tuple(peaks.T)] = np.arange(1, len(peaks) + 1)
    labels = segmentation.watershed(-distance, markers, mask=mask)
    labels = morphology.remove_small_objects(labels, max_size=39)

    # measure both channels at once, by stacking them along the last axis
    table = pd.DataFrame(
        measure.regionprops_table(
            labels,
            intensity_image=np.stack([channel_a, channel_b], axis=-1),
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
            "intensity_mean-0": "mean_intensity_channel_a",
            "intensity_mean-1": "mean_intensity_channel_b",
        }
    )

    # objects touching the image border are truncated, flag them
    interior = np.unique(segmentation.clear_border(labels))
    table["on_border"] = ~table["label"].isin(interior)

    return table


# %% [markdown]
# A pipeline saves its results to disk, one file per field. Let's do the
# same.
#
# Each field is a fresh synthetic acquisition, scaled down to mimic
# photobleaching, then cropped tighter than it was generated so that a few
# cells sit right at the edge, like on a real slide.

# %%
from pathlib import Path

folder = Path("scratch_outputs/module_07")
folder.mkdir(parents=True, exist_ok=True)

n_frames = 6
minutes_elapsed = [5 * index for index in range(n_frames)]
bleaching = 0.92  # fraction of signal remaining at every next frame
crop = 12  # trimmed from every side, tighter than the field was built for

for index, minutes in enumerate(minutes_elapsed):
    frame, _, _ = make_two_channel_cells(seed=100 + index)
    frame = frame * bleaching**index
    frame = frame[crop:-crop, crop:-crop]

    table = measure_frame(frame[..., 0], frame[..., 1])
    table.insert(0, "frame_id", f"frame_{index:02d}")
    table.to_csv(folder / f"frame_{index:02d}.csv", index=False)

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
# Three ways of selecting:
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
# `.loc` keeps the rows that are `True`.

# %%
is_large = table["area"] > 300
print(is_large.head())

large_objects = table.loc[is_large]
print(f"{len(large_objects)} objects out of {len(table)} are larger than 300 px")

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
#   Select the label and area of the objects larger than 300 pixels that do not
#   touch the border, sorted by decreasing area.
#
#   <b>Hint</b>: combine conditions with "&" and "~", each in its own
#   parentheses. Sort with "sort_values(by=..., ascending=False)".
# </div>

# %%
# --- Exercise
# Select and sort
selected = table.loc[
    (table["area"] > 300) & (~table["on_border"]),
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
# ## 4 - Putting tables together
#
# One field is never enough. Our files share the same columns, so `pd.concat`
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
#   Read all the files and concatenate them into one dataframe called "measurements".
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

print(f"{len(measurements)} objects in {len(files)} fields")
print(measurements["frame_id"].value_counts())

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
#   Labels start again at 1 in every field. After concatenating, what
#   identifies an object uniquely?
# </div>

# %% [markdown]
# Everything the acquisition knew and the pipeline did not lives in a separate
# table. `pd.merge` joins the two on a shared column: each object gets the
# metadata of the field it came from.

# %%
metadata = pd.DataFrame(
    {
        "frame_id": [f"frame_{index:02d}" for index in range(n_frames)],
        "minutes_elapsed": minutes_elapsed,
        "pixel_size_um": 0.11,  # camera pixel size of this synthetic assay, in micrometers
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
#   Merge the metadata into the measurements on "frame_id", then convert areas
#   and perimeters into physical units.
#
#   <b>Hint</b>: "pd.merge(left, right, on=...)". An area is a length squared.
# </div>

# %%
# --- Exercise
# Merge, then convert to micrometers
measurements = pd.merge(measurements, metadata, on="frame_id")

measurements["area_um2"] = measurements["area"] * measurements["pixel_size_um"] ** 2
measurements["perimeter_um"] = measurements["perimeter"] * measurements["pixel_size_um"]
# ---

measurements[["frame_id", "label", "area", "area_um2"]].head()

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
# The table is complete, so we can derive from it. Creating a column works like
# assigning to a dictionary key, on the whole column at once and without a
# `for` loop.
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
#   ratio of its mean channel A intensity over its mean channel B intensity.
#
#   <b>Hint</b>: ellipticity is "1 - minor axis / major axis", so a circle gives
#   0. You need "axis_major_length", "axis_minor_length",
#   "mean_intensity_channel_a" and "mean_intensity_channel_b".
# </div>

# %%
# --- Exercise
# Add the two columns
measurements["ellipticity"] = (
    1 - measurements["axis_minor_length"] / measurements["axis_major_length"]
)
measurements["intensity_ratio"] = (
    measurements["mean_intensity_channel_a"] / measurements["mean_intensity_channel_b"]
)
# ---

measurements[["frame_id", "label", "ellipticity", "intensity_ratio"]].head()

# %% [markdown]
# ## 5 - Summarizing per field
#
# `groupby` splits the table into groups, computes something on each, and puts
# the results back together. It answers "one number per field", or per condition.

# %%
per_frame = (
    measurements.groupby(["frame_id", "minutes_elapsed"])
    .agg(
        n_objects=("label", "count"),
        mean_area_um2=("area_um2", "mean"),
        median_ellipticity=("ellipticity", "median"),
        mean_channel_a=("mean_intensity_channel_a", "mean"),
        mean_channel_b=("mean_intensity_channel_b", "mean"),
    )
    .reset_index()
)
per_frame

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
#   This summary has one row per field, all from a single time-course run. What
#   would you need before putting any of these numbers in a paper?
# </div>

# %% [markdown]
# ## 6 - Ordered measurements: the line plot
#
# A line plot is for measurements that have an order: a dose, a depth, or here
# elapsed time. Each call to `plot` adds one line to the axes.
#
# Both channels sit in a similar intensity range here, so the question isn't
# which one is brighter, but how much each one fades. Dividing each by its
# value in the first frame puts them on a common scale and asks exactly that:
# how much has each channel changed, not how large it currently is.
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
#   the first frame, then plot both against "minutes_elapsed", with a marker on
#   every point.
#
#   <b>Hint</b>: ".iloc[0]" gives the first value of a column. Call "ax.plot"
#   twice, passing "label=" so that "ax.legend()" can name the lines, and
#   "marker="o"" to draw the points.
# </div>

# %%
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)

# --- Exercise
# Normalize each channel, then draw one line per channel
per_frame["channel_a_relative"] = (
    per_frame["mean_channel_a"] / per_frame["mean_channel_a"].iloc[0]
)
per_frame["channel_b_relative"] = (
    per_frame["mean_channel_b"] / per_frame["mean_channel_b"].iloc[0]
)

ax.plot(
    per_frame["minutes_elapsed"],
    per_frame["channel_a_relative"],
    marker="o",
    label="channel A",
)
ax.plot(
    per_frame["minutes_elapsed"],
    per_frame["channel_b_relative"],
    marker="o",
    label="channel B",
)
ax.legend()
# ---

ax.set_xlabel("Minutes elapsed")
ax.set_ylabel("Mean intensity, relative to the first frame")
ax.set_title("Photobleaching over the time-course")
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
#   Each frame is a different field of cells, not the same ones imaged twice,
#   so some of the up-and-down is which cells happened to be sampled, not the
#   bleaching itself. Does the overall direction still look like decay?
# </div>

# %% [markdown]
# ## 7 - Distributions: the box plot
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
#   Plot the distribution of cell area, one box per field.
#
#   <b>Hint</b>: "ax.boxplot" takes a list of arrays, one per box. Looping over
#   "measurements.groupby("frame_id")" gives pairs of (name, sub-dataframe).
# </div>

# %%
fig, ax = plt.subplots(figsize=(7, 4), constrained_layout=True)

# --- Exercise
# Build one group of values per field, then plot the boxes
names = []
groups = []
for name, group in measurements.groupby("frame_id"):
    names.append(name)
    groups.append(group["area_um2"])

ax.boxplot(groups, tick_labels=names)
# ---

ax.set_ylabel("Cell area (um2)")
ax.set_title("Area distribution per field")
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

ax.set_ylabel("Cell area (um2)")
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
#   Border objects sit a little higher here, not lower - the opposite of what
#   truncation alone would suggest. What could cause that?
# </div>
#
# <details>
#   <summary>Where the shift comes from</summary>
#
#   Cutting an object off should shrink its measured area, not grow it. But
#   "remove_small_objects" ran before this table ever existed: any fragment
#   that a crop reduced to almost nothing was already discarded as noise,
#   alongside genuinely small interior objects. What survives labeled "on
#   border" made it through only because enough of it was still standing after
#   the crop - a size-selection bias introduced by the filter, not a
#   truncation effect. It is a reminder to ask *why* a filter changed a
#   distribution, not only whether it did.
# </details>

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
#   Plot the perimeter of each cell against its area, colored by ellipticity,
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
#   Is the exponent compatible with 0.5? Do the residuals drift with the area,
#   or do they line up with how elongated an object is instead?
# </div>
#
# ### Conclusion
#
# <details>
#   <summary>What does the fit tell us?</summary>
#
#   <ul>
#     <li>An exponent near 0.5 means the cells are one family of shapes seen at
#     different sizes, not shapes that grow more convoluted as they grow.</li>
#     <li>Ours lands above 0.5, by many times its uncertainty. The residuals
#     barely drift with area, but they correlate with ellipticity: the objects
#     with the most extra perimeter for their size are the more elongated
#     ones.</li>
#     <li>That fits how this assay was built. Each cell's two axis lengths are
#     drawn independently of one another, so elongation does not stay fixed as
#     objects get bigger or smaller - unlike a family of shapes that really are
#     "the same shape, just larger". The gap comes from shape variability the
#     power law was never told about, not from a measurement artefact.</li>
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
#   How correlated are the area and the channel A / channel B intensity ratio?
#   Compute the Pearson and the Spearman coefficients with "scipy.stats". What
#   do they tell us?
# </div>

# %%
from scipy import stats

# --- Exercise
# Pearson and Spearman correlations
pearson = stats.pearsonr(objects["area_um2"], objects["intensity_ratio"])
spearman = stats.spearmanr(objects["area_um2"], objects["intensity_ratio"])

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
#     <li>Here neither is significant: this assay was built with cell size and
#     the channel A / channel B ratio drawn independently of one another, and
#     both tests correctly find nothing.</li>
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
    "mean_intensity_channel_b",
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
# <div style="
#   background: #e8f7ec;
#   border-left: 6px solid #2f9e44;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #1f5f2c;
# ">
#   <strong style="color: #1f5f2c;">Question</strong><br>
#   Do the three leading components carry most of the variance between them, or
#   is it spread out fairly evenly? What would that mean for finding a single
#   "most important" direction in this table?
# </div>

# %% [markdown]
# ### Finding groups without labels
#
# PCA spread the objects along the directions in which they differ most, but it
# did not say which objects belong together. Clustering does.
#
# This assay was built with two marker populations: for every cell, either
# channel A or channel B dominates. "intensity_ratio" already tells us which -
# so for once we have a known answer to check a clustering against.
#
# A ratio hides that symmetry: values below 1 are squeezed into "(0, 1)" while
# values above 1 spread out to infinity, so "channel B is twice as strong"
# and "channel A is twice as strong" do not look like mirror images of each
# other. "log2" fixes that - the same standard trick as a log-fold-change -
# turning both into equal-sized steps in opposite directions.

# %%
fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
ax.hist(np.log2(objects["intensity_ratio"]), bins=20)
ax.axvline(0, color="black", linewidth=1, linestyle="--")
ax.set_xlabel("log2(intensity_ratio)")
ax.set_ylabel("Number of cells")
ax.set_title("Two marker populations")
plt.show()

# %% [markdown]
# Two modes, one on each side of zero, with a real dip between them: the
# population split is visibly there, not something we have to take on faith.
# The question for clustering is whether it can find it too.
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
#   Build the tree on the standardized features with "linkage", then cut it
#   into two groups with "fcluster" - one for each population.<br>
#
#   <b>Hint</b>: "linkage(standardized, method="ward")" and
#   "fcluster(link, 2, criterion="maxclust")".
# </div>

# %%
from scipy.cluster import hierarchy

# --- Exercise
# Build the tree and cut it into two groups
link = hierarchy.linkage(standardized, method="ward")
objects["cluster"] = hierarchy.fcluster(link, 2, criterion="maxclust")
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
#   Does cluster membership line up with the population you already know?
#   Cross-tabulate "cluster" against whether "intensity_ratio" is at least 1.
# </div>

# %%
objects["population"] = np.where(
    objects["intensity_ratio"] >= 1, "channel A-high", "channel B-high"
)
pd.crosstab(objects["cluster"], objects["population"])

# %% [markdown]
# The match is poor. Ward groups objects that are close together by adding up
# the difference in every column, and all six columns count equally once
# standardized. "intensity_ratio" is only one of those six, and the PCA above
# already showed that no single direction dominates the variance - the five
# shape columns move just as much. With that much competing shape
# variability, the one column carrying the population signal gets outvoted.
#
# If we already know which variable defines the groups we care about, we can
# cluster on it directly instead of everything at once.

# %%
intensity_features = [
    "mean_intensity_channel_a",
    "mean_intensity_channel_b",
    "intensity_ratio",
]
intensity_values = objects[intensity_features].to_numpy()
intensity_standardized = (
    intensity_values - intensity_values.mean(axis=0)
) / intensity_values.std(axis=0)

intensity_link = hierarchy.linkage(intensity_standardized, method="ward")
objects["cluster_intensity"] = hierarchy.fcluster(
    intensity_link, 2, criterion="maxclust"
)

pd.crosstab(objects["cluster_intensity"], objects["population"])

# %% [markdown]
# Restricted to the three intensity columns, the same algorithm recovers the
# two populations almost perfectly. The population was in the data the whole
# time; mixing in five unrelated shape measurements was enough to bury it.
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
#   "fcluster" does not know what a "population" is - it returns whichever
#   partition minimizes within-group variance for however many groups you ask
#   for, on whatever columns you hand it. Here that partition matched biology
#   only once the feature space made the population the dominant source of
#   variance. Always ask what a clustering is actually optimizing before
#   trusting what it finds.
# </div>

# %% [markdown]
# We can see the improvement on the same PCA projection as before, by
# reusing the components and coloring by the intensity-based cluster instead
# of by area.

# %%
fig, ax = plt.subplots(figsize=(6, 5), constrained_layout=True)
for label, group in objects.groupby("cluster_intensity"):
    ax.scatter(
        components[objects["cluster_intensity"] == label, 0],
        components[objects["cluster_intensity"] == label, 1],
        label=f"cluster {label}",
        alpha=0.8,
    )
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_title("Intensity-based clusters on the shape + intensity PCA")
ax.legend()

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
#   Save the per-field summary as a CSV and the PCA figure as a PNG, both into a
#   "results" folder.
#
#   <b>Hint</b>: "to_csv(path, index=False)" and
#   "savefig(path, dpi=200, bbox_inches="tight")".
# </div>

# %%
results = Path("scratch_outputs/results")

# --- Exercise
# Save the summary table and the PCA figure
results.mkdir(parents=True, exist_ok=True)

per_frame.to_csv(results / "per_frame_summary.csv", index=False)
pca_fig.savefig(results / "pca.png", dpi=200, bbox_inches="tight")
# ---

print(f"Saved to {results.resolve()}")

# %% [markdown]
# ## Summary
#
# In this module we turned a folder of per-field measurements into a single
# table, and the table into figures. We loaded and inspected it, selected rows
# and columns, concatenated the fields and merged in the metadata the pipeline
# did not know, derived new columns, and summarized per field with "groupby".
#
# We then created 4 useful plots which help us to answer different
# questions: a line plot for measurements that have an order, a box
# plot for a distribution, a scatter plot for two variables at once with a third
# in the color, and a fitted curve when a model is worth testing against the
# data.
#
# The optional exercises help us to describe the objects and look for
# structure among them with correlations, as well as PCA and a clustering -
# and to see that an unsupervised method can miss a signal that was there all
# along, depending on what else you ask it to weigh against it.
#
# More interesting ways to analyse and visualize data:
#
