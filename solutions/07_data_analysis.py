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
#   Select the label and area of the objects larger than 300 pixels that do not
#   touch the border, sorted by decreasing area.
#
#   <b>Hint</b>: combine conditions with "&" (and) and "~" (not), each condition surrounded by parenthesis. Sort with "sort_values(by=..., ascending=False)".
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
#   Read all the files and concatenate them into one dataframe called "df_measure".
#
#   <b>Hint</b>: build a list of dataframes, then call
#   "pd.concat(tables, ignore_index=True)".
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
#   Merge the metadata into the measurements on "frame_id".
#
#   <b>Hint</b>: "pd.merge(left, right, on=...)". An area is a length squared.
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
#   <b>Hint</b>: `plt.boxplot` can take a list of dataframes to plot various boxes next to each other, alongside a list of labels (`tick_labels`).
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
#   What statistical measures of the distribution are shown in a box plot?
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
parameters, covariance = curve_fit(power_law, ellipt, intensity_r, p0=[0.5, 2])
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
fig, ax = plt.subplots(figsize=(10, 4), constrained_layout=True)

# --- Exercise
# Left: data and fitted curve. Right: residuals.
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
