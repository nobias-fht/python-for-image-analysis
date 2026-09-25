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
# - Load, select and combine measurement tables.
# - Draw the plots you will use most: line plot, box plot, scatter plot.
# - Fit a curve to your data with `scipy`.

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
print(f"Is a directory: {measurement_path.is_dir()}")

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
#
#   <details>
#   <summary>
#   <strong>Hint</strong>
#   </summary>
#
#   Remember the `.glob` method.
#   </details>
# </div>


# %%
# --- Exercise
files = sorted(list(measurement_path.glob("*.csv")))
print(files)
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
#
#   Read the first file into a dataframe and show its first rows.
#
#   <b>Tip</b>: `pd.read_csv` takes a path, and every dataframe has a `.head()`.
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
#
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
#
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
#
#   Before trusting a table, look at it. How many objects? Which columns, and of
#   what type? What are the ranges of the measurements?
#
#   <b>Tip</b>: `shape`, `columns` and `dtypes` are attributes, `info()` and
#   `describe()` are methods.
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
#
#   Select two columns from the dataframe.
# </div>
#

# %%
# --- Exercise
table[["label", "area"]]
# ---

# %% [markdown]
# A more interesting operation is selecting conditionally certain rows. A condition on a column gives one `True` or `False` per row. Indexing the `.loc` property with the condition keeps the rows that are `True`.
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
#   Use the condition to select a subset of the table.
#
#   <b>Tip: </b>`.loc` uses square bracket indexing notation.
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
#
#   What percentage of objects are satisfying the condition?
# </div>

# %%
# condition
thresh = 150
is_large = table["area"] > thresh


# --- Exercise
large_objects = table.loc[is_large]
print(
    f"{len(large_objects)} objects out of {len(table)} are larger than {thresh} px "
    f"({len(large_objects)*100/len(table):.2f}%)"
)
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
#   Select the label and area of the objects larger than 150 pixels that do not
#   touch the border, sorted by decreasing area.
#
#   <b>Tip</b>:
#
#   1. Combine conditions with `&` (AND) and `~` (NOT), each condition surrounded by parenthesis.
#   2. Sort with `.sort_values(by=..., ascending=False)`.
# </div>

# %%
# Select and sort
# --- Exercise
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
#   Read the docs for `pd.concat`, what are its arguments?
#
#   <b>Tip: </b> Use the argument `ignore_index=True` to reset the indices from 0 to the length of the dataframe after concatenation.
# </div>

# %%
# Read every file and concatenate
# --- Exercise
tables = [pd.read_csv(file) for file in files]
df_measure = pd.concat(tables, ignore_index=True)
# ---

print(f"{len(df_measure)} objects in {len(files)} images\n")
# We can see how many rows are contributed from each frame.
print("Row count for each frame:")
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
#
#   Labels start again at 1 in every frame. After concatenating, what
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
#
#   Let's say we now want to add metadata from the images that were not in the original
#   result tables.
#
#   Merge the metadata into the measurements on `"frame_id"`. Use the function `pd.merge`, what are its arguments?
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

# Merge the new metadata into the df, call the resulting df `df_merged`
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
#
#   What has changed with the new dataframe?
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
#
#   What happens if there are columns with the same name in both dataframes (that we are not merging on)?
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
#
#   We can also create new columns similarly to new dictionary entries. Let's use the newly added metadata to convert areas
#   and perimeters into physical units (μm<sup>2</sup> and μm respectively).
# </div>

# %%
# Calculate and add to the dataframe the columns "area_um2" and "perimeter_um"
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
#
#   Add two columns to the dataframe:
#   - the "ellipticity" of each object (equation below), and
#   - the ratio of the mean marker intensity over the mean nuclear intensity.
# </div>
#
# The equation for ellipticity is: $$\epsilon = 1 - \frac{A_{minor}}{A_{major}}$$
#
# where $A_{minor}$ corresponds to `"axis_minor_lenth"`, and $A_{major}$ to its major counterpart.

# %%
# Add the columns "ellipticity" and "intensity_ratio".
# --- Exercise
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
# `groupby` splits the table into groups according to row's values in specific columns.
# This creates a `DataFrameGroupBy` object which has a few helpful methods to help us complete our analysis, one such method is `.agg`.
# The `.agg` method allows us to aggregate values in a group to create a new data frame, for example we could make a column of the mean area in each group. `.agg` is demonstrated below.

# %%
# Our new dataframe with values aggregated per group
per_frame = (
    df_merged.groupby(["frame_id", "minutes_elapsed"])
    .agg(
        # Each argument becomes a new column,
        # it takes a tuple (columumn to operate on, operation to use)
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
#
#   The `.agg` method is not limited to `mean` and `median`.
#   Can you find in the pandas documentation which functions it accepts?
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
#
#   Plot the mean intensity ratio versus time.
#
#   Look at the aggregated table we just calculated, which column contains the time data and which column contains the mean intensity ratio?
# </div>

# %%
fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)

# Make a simple line plot of mean intensity ratio vs time. Change the plot `marker`
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
#
#   There is some important information missing from this line plot that should be displayed. Can you think of what it might be?
#
#   <details>
#   <summary>
#   <strong>Hint</strong>
#   </summary>
#
#   Imagine this is a figure for a publication, what should a reviewer ask to see?
#
#   It can be derived from the data.
#   </details>
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
#
#   Based on your answer to the previous question, improve the plot with the additional information/data, you will need to calculate it first.
#
#   <details>
#   <summary>
#   <strong>Hint</strong>
#   </summary>
#
#   You should add a new column to the `per_frame` dataframe calculated from the `.agg` method.
#
#   Search the matplotlib docs for a function to display the information (we cannot use `plt.plot`).
#   </details>
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
#   The previous analysis (which produced the csv files) has identified some cell populations, "bright", "dim" and "artifact".
#
#   Let's use the `boxplot` function to compare their intensity ratio distributions.
#
#   <b>Tip</b>: `plt.boxplot` can take a list of dataframe columns (`Series` objects) to plot various boxes next to each other, alongside a list of labels (`tick_labels`).
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
#
#   On which dataframe should you work? What information do you need to select?
# </div>

# %%
fig, ax = plt.subplots(figsize=(7, 4), constrained_layout=True)

# Compare the intensity ratio distributions across the 3 populations with `boxplot`
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
#
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
#   changes over time (line plot). Let's look at how the different population distributions compare at three chosen time points. Do they evolve differently?
#
#   Make a boxplot comparing the populations' intensity ratio distribution for each time point.
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
#
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
#
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
#   Let's look at the **bright cell population** and check the relationship between `ellipticity`
#   and `intensity_ratio` using `plt.scatter`.
# </div>

# %%
fig, ax = plt.subplots(figsize=(6, 4.5), constrained_layout=True)

# For only the bright cell population,
# investigate the relationship between ellipticity and intensity_ratio
# --- Exercise
df_plot = df_merged.loc[df_merged["population"] == "bright"]

# levels, categories = pd.factorize(df_plot["minutes_elapsed"])
scatter = ax.scatter(
    df_plot["ellipticity"],
    df_plot["intensity_ratio"],
    # c=levels
)
# plt.legend(scatter.legend_elements()[0], categories, title="Time")
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
# Fitting estimates the parameters of a model we think might represent the data well.
#
# We can use `scipy.optimize.curve_fit`which takes a function whose first argument is the x data, and whose other arguments are the parameters to estimate.
# Let's examine power laws for our ellipticity-intensity ratio correlation.


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
#
#   Fit the model, and print the parameters with their uncertainty.
#
#   <b>Tip</b>: `curve_fit(model, x, y, p0=[...])` returns the parameters and
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
parameters, covariance = curve_fit(power_law, ellipt, intensity_r, p0=[1, 1])
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
#
#   Draw the fitted curve over the data.
#
#   <details>
#   <summary>
#   <strong>Hint</strong>
#   </summary>
#
#   Use `np.linspace` to generate a set of evenly spaced x coordinates over the range of the data. Then we can apply our power law function to these points using the fitted parameters.
#   </details>
# </div>

# %%
fig, ax = plt.subplots(figsize=(10, 4), constrained_layout=True)

# --- Exercise
smooth_x = np.linspace(ellipt.min(), ellipt.max(), 100)

ax.scatter(ellipt, intensity_r, s=20, alpha=0.6, label="Cells")
ax.plot(
    smooth_x,
    power_law(smooth_x, *parameters),
    color="crimson",
    label=f"fit: b = {parameters[1]:.2f}",
)
ax.legend()
# ---

ax.set_xlabel("Ellipticity")
ax.set_ylabel("Intensity ratio")

plt.show()

# %% [markdown]
# The residual for each data point is how far it is from the curve, i.e.:
# $$
# r_i = y_i - \hat{y}_i
# $$
# where $y_i$ in this case is the intensity ratio, and $\hat{y}_i$ is the curve prediction.
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
#   Calculate the residuals and plot them against $x_i$ (ellipticity). What do you expect to see? What is the sign of a good fit?
# </div>

# %%
fig, ax = plt.subplots(figsize=(10, 4), constrained_layout=True)

# --- Exercise
curve_predictions = power_law(ellipt, *parameters)
residuals = intensity_r - curve_predictions
ax.scatter(ellipt, residuals, c="r", s=20, alpha=0.6, label="Cells")
# ---

ax.set_title("Residuals")
ax.set_xlabel("Ellipticity")
ax.set_ylabel("Intensity ratio")

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
#   Maybe a power law doesn't quite capture the shape of the data, can you fit a better curve?
#
#   <details>
#   <summary>
#   <strong>Hint</strong>
#   </summary>
#
#   Does it look like the relationship exactly crosses the origin? Maybe we are missing a term in the equation.
#   </details>
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
#
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
#
#   How correlated are nuclear and marker intensities for the bright cell population?
#   Compute the Pearson and the Spearman coefficients with `scipy.stats`.
#
#   Plot the scatter of nuclear vs marker intensity to visually inspect the correlation result.
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
plt.xlabel("Marker intensity")
plt.xlabel("Nuclear intensity")
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
#
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
