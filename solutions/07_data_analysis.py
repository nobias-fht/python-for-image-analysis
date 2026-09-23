# %% [markdown]
# # Module 7: data analysis and visualization
#
# Time: 1 hour 45 minutes.
#
# `pandas` is the standard library for tabular data in Python. Its `DataFrame` object is
# a table with named columns, each column holding one type, and is often used when analyzing data.
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
# ## 1 - Intro
#
# Oftentimes, a pipeline will result in measurements, as we've seen during the practical. Here, we will assume that some measurements were created and saved to .csv files.

# %%
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from python_for_ia import get_measurements

measurement_path = get_measurements()

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
#   Let's list the files in the `measurement_path` and sort them.
# </div>


# %%
# --- Exercise
files = sorted(list(measurement_path.glob("*.csv")))
# ---

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
#   background: #e8f7ec;
#   border-left: 6px solid #2f9e44;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #1f5f2c;
# ">
#   <strong style="color: #1f5f2c;">Question</strong><br>
#   How were these measurements obtained?
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
print(f"Rows and columns: {table.shape}")
print(f"Columns: {list(table.columns)}")

table.info()
table.describe()
# ---

# %% [markdown]
# ## 3 - Selecting rows and columns
#
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

# %%
# --- Exercise
table[["label", "area"]]
# ---

# %% [markdown]
# A more interesting operation is selecting conditionally certain rows. A condition on a column gives one `True` or `False` per row. Passing it to
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
# <div style="
#   background: #e8f7ec;
#   border-left: 6px solid #2f9e44;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #1f5f2c;
# ">
#   <strong style="color: #1f5f2c;">Question</strong><br>
#   What percentage of objects are satisfying the condition?
# </div>

# %%
# condition
thresh = 150
is_large = table["area"] > thresh

# --- Exercise
large_objects = table.loc[is_large]
print(f"{len(large_objects)} objects out of {len(table)} are larger than {thresh} px")
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
#   Select the label and area of the objects larger than 150 pixels that do not
#   touch the border, sorted by decreasing area.
#
#   <b>Hint</b>: combine conditions with `&` (AND) and `~` (NOT), each condition surrounded by parenthesis. Sort with `sort_values(by=..., ascending=False)`.
# </div>

# %%
# --- Exercise
# Select and sort
selected = table.loc[
    (table["area"] > 150) & (~table["on_border"]),
    ["label", "area"],
]
selected = selected.sort_values(by="area", ascending=False)
selected.head()
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
#   We've used the logical AND (`&`) and NOT (`~`) operators, what is OR?
# </div>

# %% [markdown]
# ## 4 - Concatenation and merging
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
#
#   Read all the files and concatenate them into one dataframe called `df_measure`.
#
#   <b>Hint</b>: build a list of dataframes, then call
#   `pd.concat(tables, ignore_index=True)`.
# </div>

# %%
# --- Exercise
# Read every file and concatenate
tables = [pd.read_csv(file) for file in files]
df_measure = pd.concat(tables, ignore_index=True)
# ---

print(f"{len(df_measure)} objects in {len(files)} images")
print(df_measure["frame_id"].value_counts())

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
#   identifies an object in our dataframe uniquely?
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
#   Merge the metadata into the measurements on `"frame_id"`.
#
#   <b>Hint</b>: `pd.merge(left, right, on=...)`. An area is a length squared.
# </div>

# %%
n_frames = 6
minutes_elapsed = [5 * index for index in range(n_frames)]

metadata = pd.DataFrame(
    {
        "frame_id": [f"frame_{index:02d}" for index in range(n_frames)],
        "minutes_elapsed": minutes_elapsed,
        "pixel_size_um": 0.11,  # camera pixel size of this synthetic assay, in micrometers
    }
)

# --- Exercise
df_merged = pd.merge(df_measure, metadata, on="frame_id")
# ---

df_merged.head()

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
#   What has changed with the new dataframe?
# </div>
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
df_merged["area_um2"] = df_merged["area"] * df_merged["pixel_size_um"] ** 2
df_merged["perimeter_um"] = df_merged["perimeter"] * df_merged["pixel_size_um"]
# ---

df_merged[["frame_id", "label", "area", "area_um2"]].head()

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
#   A dataframe can mix pixels, micrometers and arbitrary units while looking
#   perfectly valid. Putting the unit in the column name, as in `"area_um2"`, costs
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
#   ratio of its mean marker intensity over its mean nuclear intensity.
# </div>
#
# $$\epsilon = 1 - \frac{A_{minor}}{A_{major}}$$
#
# where $A_{minor}$ corresponds to `"axis_minor_lenth"`, and $A_{major}$ to its major counterpart.

# %%
# --- Exercise
# Add the two columns
df_merged["ellipticity"] = (
    1 - df_merged["axis_minor_length"] / df_merged["axis_major_length"]
)
df_merged["intensity_ratio"] = (
    df_merged["marker_intensity"] / df_merged["nuclear_intensity"]
)
# ---

df_merged[["frame_id", "label", "ellipticity", "intensity_ratio"]].head()

# %% [markdown]
# ## 5 - Performing operations over values
#
# `groupby` splits the table into groups according to row's values in specific columns, allowing us to compute something on them (e.g. `.agg`) or filtering (`.filter`).

# %%
per_frame = (
    df_merged.groupby(["frame_id", "minutes_elapsed"])
    .agg(
        n_objects=("label", "count"),
        mean_area_um2=("area_um2", "mean"),
        median_ellipticity=("ellipticity", "median"),
        mean_nuclear_intensity=("nuclear_intensity", "mean"),
        mean_marker_intensity=("marker_intensity", "mean"),
        mean_intensity_r=("intensity_ratio", "mean"),
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

# %% [markdown]
# ## 6 - Line plot
#
# A line plot is one of the most common way of representing data.
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
#   Plot the mean intensity ratio (channel B/ A) versus time ("minutes_elapsed").
# </div>

# %%
fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)

# --- Exercise
ax.plot(
    per_frame["minutes_elapsed"],
    per_frame["mean_intensity_r"],
    marker="o",
)
# ---

ax.set_xlabel("Minutes elapsed")
ax.set_ylabel("Mean intensity ratio")
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
#   What is missing from the plot? How to compute and add it?
# </div>
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
#   Based on your answer to the previous question, improve the plot with the additional information/data.
#
#   <b>Hint</b>: you need to use a different function from `plt.plot`.
# </div>

# %% [markdown]
# ## 7 - Distributions: the box plot
#
# Box plots and violin plots are great way of comparing not only the mean of a distribution
# but the distribution itself.
#
# In the previous plot, we have seen that intensity ratio is in average increasing then saturating
# throughout time. Let's see what drives this increase.
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
#   The previous analysis (which produced the csv files) has identified some cell populations, bright, dim and artifact.
#   Let's compare their distribution of intensity using `boxplot`.
#
#   <b>Hint</b>: `plt.boxplot` can take a list of dataframe columns (`Serie`) to plot various boxes next to each other, alongside a list of labels (`tick_labels`).
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
#   On which dataframe should you work?
# </div>

# %%
fig, ax = plt.subplots(figsize=(7, 4), constrained_layout=True)

# --- Exercise
groups = [
    df_merged.loc[df_merged["population"] == "artifact", "intensity_ratio"],
    df_merged.loc[df_merged["population"] == "dim", "intensity_ratio"],
    df_merged.loc[df_merged["population"] == "bright", "intensity_ratio"],
]

ax.boxplot(groups, tick_labels=["artifact", "dim", "bright"])
# ---

ax.set_ylabel("Intensity ratio")
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
#   What statistical measures of the distributions are shown in a box plot?
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
#   There is a difference between the populations, but we know that the intensity also
#   changes over time (line plot). Let's pick three time frame and look at how the various
#   population intensity ratio evolves with time.
#
#   Plot the same box plots but with the additional condition on `minutes_elapsed`.
#
# </div>

# %%
time = [0, 10, 20]
fig, ax = plt.subplots(3, 1, figsize=(7, 8), constrained_layout=True)

# --- Exercise
for i, t in enumerate(time):
    groups = [
        df_merged.loc[
            (df_merged["population"] == "artifact")
            & (df_merged["minutes_elapsed"] == t),
            "intensity_ratio",
        ],
        df_merged.loc[
            (df_merged["population"] == "dim") & (df_merged["minutes_elapsed"] == t),
            "intensity_ratio",
        ],
        df_merged.loc[
            (df_merged["population"] == "bright") & (df_merged["minutes_elapsed"] == t),
            "intensity_ratio",
        ],
    ]

    ax[i].boxplot(groups, tick_labels=["artifact", "dim", "bright"])
    ax[i].set_ylabel("Intensity ratio")
    ax[i].set_title(f"{t} min")
# ---

plt.show()

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
#   Draw the same data using a violin plot.
# </div>
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
#   Investigate the ellipticity distribution rather than the intensity ratio using box plots.
#
#   <b>Hint</b>: Negative ellipticity is an artefact of a potentially failed measurement. Use `set_ylim` to change the y-axis limits.
# </div>

# %% [markdown]
# ## 8 - Relationships: the scatter plot
#
# If you've done the optional exercises, you should have noticed that intensity ratio between
# channels is not the only measured parameter that increases with time. To investigate
# correlations between parameters, we may want to look at a scatter plot.
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
#   Let's look at the bright cell population and check the relationship between `ellipticity`
#   and `intensity_ratio` using `plt.scatter`.
# </div>

# %%
fig, ax = plt.subplots(figsize=(6, 4.5), constrained_layout=True)

# --- Exercise
df_plot = df_merged.loc[df_merged["population"] == "bright"]

ax.scatter(
    df_plot["ellipticity"],
    df_plot["intensity_ratio"],
)
# ---

ax.set_xlabel("Ellipticity")
ax.set_ylabel("Intensity ratio")
ax.set_xlim([0, None])
plt.show()

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
#
#   By using `levels, categories = pd.factorize(...)` on a column, one can use `levels` in
#   `plt.scatter(..., c=levels)` to color code the categories of the column. This is useful
#   when the column only has a few values.
#
#   You'd need to then use `scatter = ax.scatter(..., c=levels)` and `plt.legend(scatter.legend_elements()[0], categories, title='Time')`.
#
#   Color code the previous scatter plot with `minutes_elapsed`.
#
# </div>

# %% [markdown]
# ## 9 - Fitting a curve
#
# Fitting estimates the parameters of a model we think might represent the data well. `curve_fit` takes a function whose first argument is the x data, and whose
# other arguments are the parameters to estimate. Let's examine power laws for our ellipticity-intensity ratio correlation.


# %%
def power_law(ellipticity, a, b):
    return a * ellipticity**b


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
#   <b>Hint</b>: `curve_fit(model, x, y, p0=[...])` returns the parameters and
#   their covariance matrix. The standard errors are
#   `np.sqrt(np.diag(covariance))`.
# </div>

# %%
from scipy.optimize import curve_fit

df_analyse = df_merged.loc[
    (df_merged["population"] == "bright") & (df_merged["ellipticity"] > 0)
].copy()

intensity_r = df_analyse["intensity_ratio"].to_numpy()
ellipt = df_analyse["ellipticity"].to_numpy()

# --- Exercise
# Fit the model and report the parameters
parameters, covariance = curve_fit(power_law, ellipt, intensity_r, p0=[0.2, 2])
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
#   <b>Hint</b>: to evaluate the fit on a the data range we are interested on, we can create a new set of x-axis values using `np.linspace(min, max, n_points)` and apply our power law function to it using the fitted parameters.
# </div>

# %%
fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)

# --- Exercise
smooth_area = np.linspace(ellipt.min(), ellipt.max(), 100)

ax.scatter(ellipt, intensity_r, s=20, alpha=0.6, label="Cells")
ax.plot(
    smooth_area,
    power_law(smooth_area, *parameters),
    color="crimson",
    label=f"fit: b = {parameters[1]:.2f}",
)
ax.legend()

# ---

ax.set_xlabel("Ellipticity")
ax.set_ylabel("Intensity ratio")

plt.show()

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
#   Since we are often working on the dataframe (producing additional columns, measurements,
#   quantifications, etc.), we need to be able to save them.
#
#   Check out the pandas documentation for the `dataframe.to_csv` method and save a
#   dataframe containing only the bright cell population to disk.
# </div>

# %%
results = Path("results")
results.mkdir(parents=True, exist_ok=True)

# --- Exercise
df_analyse = df_merged.loc[(df_merged["population"] == "bright")].copy()
df_analyse.to_csv(results / "bright_cells.csv", index=False)
# ---


# %% [markdown]
# ## Optional exercises
#
# ### Correlations
#
# After comparing dependencies between variables, there are many statistical measurements
# that can be performed, for instance statistical tests or correlations measurements. Keep in
# mind that each have their underlying assumptions. They might give you the answer you were
# hoping for, but if the hypothesis are not validated (e.g. normalized data, normal distribution, etc.)
# then the result is worthless.
#
# In these optional exercises, we run correlation measurements.

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
#   How correlated are nuclear and marker intensities for the bright cell population?
#   Compute the Pearson and the Spearman coefficients with "scipy.stats".
#
#   Also plot the scatter of nuclear vs marker intensity.
# </div>

# %%
from scipy import stats

df_analyse = df_merged.loc[(df_merged["population"] == "bright")].copy()

# --- Exercise
# Pearson and Spearman correlations
pearson = stats.pearsonr(
    df_analyse["nuclear_intensity"], df_analyse["marker_intensity"]
)
spearman = stats.spearmanr(
    df_analyse["nuclear_intensity"], df_analyse["marker_intensity"]
)

print(f"Pearson:  r = {pearson.statistic:.3f}, p = {pearson.pvalue:.3g}")
print(f"Spearman: r = {spearman.statistic:.3f}, p = {spearman.pvalue:.3g}")

plt.scatter(df_analyse["marker_intensity"], df_analyse["nuclear_intensity"])
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
#   What about the dim cells? Plot the two channels against each other.
# </div>

# %%
from scipy import stats

df_analyse = df_merged.loc[(df_merged["population"] == "dim")].copy()

# --- Exercise
# Pearson and Spearman correlations
pearson = stats.pearsonr(
    df_analyse["nuclear_intensity"], df_analyse["marker_intensity"]
)
spearman = stats.spearmanr(
    df_analyse["nuclear_intensity"], df_analyse["marker_intensity"]
)

print(f"Pearson:  r = {pearson.statistic:.3f}, p = {pearson.pvalue:.3g}")
print(f"Spearman: r = {spearman.statistic:.3f}, p = {spearman.pvalue:.3g}")

plt.scatter(df_analyse["marker_intensity"], df_analyse["nuclear_intensity"])
# ---

# %% [markdown]
# <details>
#   <summary>Pearson or Spearman?</summary>
#
#   <ul>
#     <li><strong>Pearson</strong> measures how well a straight line fits, and is
#     sensitive to outliers.</li>
#     <li><strong>Spearman</strong> works on the ranks, so it only asks whether
#     one variable increases with the other, and it is resistant to outliers.</li>
#     <li>Here that difference is not significant.</li>
#   </ul>
# </details>
