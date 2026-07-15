# %% [markdown]
# # Module 7: data analysis and visualization
#
# Time: 1 hour 45 minutes.
#
# Essential ideas: measurements become useful when they are organized in tidy
# tables, checked for quality, summarized by meaningful groups, and visualized
# with plots that answer a concrete question.

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# %% [markdown]
# ## Create a synthetic measurement table
#
# In a real workflow this table would come from `regionprops_table` or another
# measurement step. Each row should describe one object, and each column should
# describe one variable.

# %%
rng = np.random.default_rng(7)
n = 120
df = pd.DataFrame(
    {
        "image_id": rng.choice(["img_001", "img_002", "img_003"], size=n),
        "label": np.arange(1, n + 1),
        "population": rng.choice(["A-high", "B-high"], size=n),
        "ratio_a_over_b": rng.lognormal(mean=0.0, sigma=0.45, size=n),
        "ellipticity": rng.beta(a=2, b=5, size=n),
        "area": rng.normal(loc=180, scale=45, size=n).clip(20, None),
    }
)
df.loc[df["population"] == "A-high", "ratio_a_over_b"] *= 1.5
df["population"] = pd.Categorical(df["population"], categories=["A-high", "B-high"])
print(df.head())

# %% [markdown]
# ## First checks
#
# Before plotting conclusions, check types, missing values, ranges, and obvious
# outliers.
#
# Pitfall: a dataframe can look valid while mixing pixels, micrometers, and
# arbitrary units. Units belong in column names, metadata, or documentation.

# %%
print(df.info())
print(df.describe(include="all"))
print("missing values:")
print(df.isna().sum())

outliers = df[df["ellipticity"] > 0.9]
print("very elongated objects:", len(outliers))

# %% [markdown]
# ## Filtering and assigning new columns
#
# Use `.copy()` after filtering when you plan to add columns. It avoids
# confusing chained-assignment warnings and makes intent explicit.

# %%
filtered = df[(df["ellipticity"] < 0.8) & (df["area"] >= 50)].copy()
filtered["log2_ratio"] = np.log2(filtered["ratio_a_over_b"])
filtered["shape_class"] = np.where(
    filtered["ellipticity"] > 0.5, "elongated", "rounder"
)
print(filtered.head())

# %% [markdown]
# ## Grouping and summarizing
#
# Choose grouping variables that match the experimental design. For microscopy,
# avoid treating thousands of cells as fully independent if they come from only
# a few images or biological replicates.

# %%
summary = (
    filtered.groupby(["image_id", "population"], observed=True)
    .agg(
        n_objects=("label", "count"),
        mean_ratio=("ratio_a_over_b", "mean"),
        median_ellipticity=("ellipticity", "median"),
        mean_area=("area", "mean"),
    )
    .reset_index()
)
print(summary)

# %% [markdown]
# ## Box, scatter, and multiline plots
#
# When to use:
#
# - box plot: compare distributions across groups,
# - scatter plot: inspect relationships between two variables,
# - line plot: show ordered measurements such as time, dose, or image index.

# %%
fig, axes = plt.subplots(1, 3, figsize=(12, 3))

filtered.boxplot(column="ratio_a_over_b", by="population", ax=axes[0])
axes[0].set_title("ratio by population")
axes[0].set_ylabel("A/B ratio")

for population, part in filtered.groupby("population", observed=True):
    axes[1].scatter(
        part["ratio_a_over_b"], part["ellipticity"], alpha=0.7, label=population
    )
axes[1].set_xlabel("A/B ratio")
axes[1].set_ylabel("ellipticity")
axes[1].legend()

for population, part in summary.groupby("population", observed=True):
    axes[2].plot(part["image_id"], part["mean_ratio"], marker="o", label=population)
axes[2].set_ylabel("mean ratio")
axes[2].legend()

plt.suptitle("")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Simple uncertainty display
#
# Error bars are not decoration. Decide whether they show standard deviation,
# standard error, confidence interval, or another quantity.

# %%
error_summary = (
    filtered.groupby("population", observed=True)
    .agg(mean_ratio=("ratio_a_over_b", "mean"), std_ratio=("ratio_a_over_b", "std"))
    .reset_index()
)

plt.errorbar(
    error_summary["population"].astype(str),
    error_summary["mean_ratio"],
    yerr=error_summary["std_ratio"],
    fmt="o",
    capsize=5,
)
plt.ylabel("A/B ratio, mean +/- SD")
plt.show()

# %% [markdown]
# ## SciPy curve fitting
#
# Curve fitting estimates parameters of a model. Use it when the model has a
# scientific or technical reason, not just because a curve can be drawn.
#
# Pitfalls:
#
# - bad initial guesses can fail,
# - parameters may be correlated,
# - a good-looking fit can still be the wrong model,
# - inspect residuals.

# %%
time = np.arange(0, 12)
true_curve = 0.2 + 1.8 * (1 - np.exp(-time / 3.0))
measurement = true_curve + rng.normal(0, 0.08, size=time.size)


def one_phase_association(t, baseline, amplitude, tau):
    return baseline + amplitude * (1 - np.exp(-t / tau))


params, covariance = curve_fit(one_phase_association, time, measurement, p0=[0, 2, 3])
fit = one_phase_association(time, *params)
residuals = measurement - fit

print("baseline, amplitude, tau:", params)
print("parameter standard errors:", np.sqrt(np.diag(covariance)))

fig, axes = plt.subplots(1, 2, figsize=(9, 3))
axes[0].scatter(time, measurement, label="measurements")
axes[0].plot(time, fit, label="fit")
axes[0].set_xlabel("time")
axes[0].set_ylabel("mean intensity")
axes[0].legend()
axes[1].axhline(0, color="black", linewidth=1)
axes[1].scatter(time, residuals)
axes[1].set_xlabel("time")
axes[1].set_ylabel("residual")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Optional exercises
#
# 1. Calculate mean ellipticity per population and per image.
# 2. Add a column that marks objects above the 90th percentile of area.
# 3. Make a scatter plot of area versus ratio, colored by population.
# 4. Fit a straight line to `time` and `measurement`, then compare residuals to
#    the exponential model.
# 5. Save the summary table to `scratch_outputs/module07_summary.csv`.

# %%
# Answer sketch (optional, removable)
print(filtered.groupby(["image_id", "population"], observed=True)["ellipticity"].mean())

area_cutoff = filtered["area"].quantile(0.9)
filtered["large_object"] = filtered["area"] > area_cutoff
print(filtered[["area", "large_object"]].head())

for population, part in filtered.groupby("population", observed=True):
    plt.scatter(part["area"], part["ratio_a_over_b"], label=population, alpha=0.7)
plt.xlabel("area")
plt.ylabel("A/B ratio")
plt.legend()
plt.show()

linear_params = np.polyfit(time, measurement, deg=1)
linear_fit = np.polyval(linear_params, time)
print("linear residual sum of squares:", np.sum((measurement - linear_fit) ** 2))
print("exponential residual sum of squares:", np.sum(residuals**2))

summary_path = Path("scratch_outputs/module07_summary.csv")
summary_path.parent.mkdir(parents=True, exist_ok=True)
summary.to_csv(summary_path, index=False)
