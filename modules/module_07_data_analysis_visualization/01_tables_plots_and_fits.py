# %% [markdown]
# # Module 7: data analysis and visualization
#
# Essential ideas: collect measurements in a dataframe, filter/group/summarize
# them, and make plots that answer specific analysis questions.

# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

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
    }
)
df.loc[df["population"] == "A-high", "ratio_a_over_b"] *= 1.5
print(df.head())

# %% [markdown]
# ## Dataframe manipulation

# %%
filtered = df[df["ellipticity"] < 0.8].copy()
summary = (
    filtered.groupby(["image_id", "population"])
    .agg(
        n_objects=("label", "count"),
        mean_ratio=("ratio_a_over_b", "mean"),
        median_ellipticity=("ellipticity", "median"),
    )
    .reset_index()
)
print(summary)

# %% [markdown]
# ## Box, scatter, and multiline plots

# %%
fig, axes = plt.subplots(1, 3, figsize=(12, 3))

filtered.boxplot(column="ratio_a_over_b", by="population", ax=axes[0])
axes[0].set_title("ratio by population")
axes[0].set_ylabel("A/B ratio")

axes[1].scatter(filtered["ratio_a_over_b"], filtered["ellipticity"], alpha=0.7)
axes[1].set_xlabel("A/B ratio")
axes[1].set_ylabel("ellipticity")

for population, part in summary.groupby("population"):
    axes[2].plot(part["image_id"], part["mean_ratio"], marker="o", label=population)
axes[2].set_ylabel("mean ratio")
axes[2].legend()

plt.suptitle("")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## SciPy curve fitting

# %%
time = np.arange(0, 12)
true_curve = 0.2 + 1.8 * (1 - np.exp(-time / 3.0))
measurement = true_curve + rng.normal(0, 0.08, size=time.size)


def one_phase_association(t, baseline, amplitude, tau):
    return baseline + amplitude * (1 - np.exp(-t / tau))


params, _ = curve_fit(one_phase_association, time, measurement, p0=[0, 2, 3])
print("baseline, amplitude, tau:", params)

plt.scatter(time, measurement, label="measurements")
plt.plot(time, one_phase_association(time, *params), label="fit")
plt.xlabel("time")
plt.ylabel("mean intensity")
plt.legend()
plt.show()

# %% [markdown]
# ## Optional exercises
#
# 1. Calculate mean ellipticity per population.
# 2. Color the scatter plot by population.

# %%
# Answer sketch (optional, removable)
print(df.groupby("population")["ellipticity"].mean())
for population, part in df.groupby("population"):
    plt.scatter(part["ratio_a_over_b"], part["ellipticity"], label=population, alpha=0.7)
plt.legend()
plt.show()
