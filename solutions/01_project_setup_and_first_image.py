# %% [markdown]
# # Module 1: virtual environments, Jupyter, and a first image
#
# Time: 1 hour.
#
# Essential idea: an analysis is easier to trust when the Python environment is
# explicit, isolated, and used consistently from the terminal, VSCode, and
# Jupyter. In this short module, students should leave with one working project
# and one tiny image-processing example.

# %% [markdown]
# ## Terminal setup with uv
#
# Run these commands in a terminal. The exact project name can change, but the
# logic should stay the same:
#
# ```bash
# uv init python-for-image-analysis
# cd python-for-image-analysis
# uv add numpy scipy pandas matplotlib scikit-image jupyter ipykernel
# uv run python -m ipykernel install --user --name python-image-analysis
# uv run jupyter lab
# ```
#
# Useful mental model:
#
# - `uv` creates and updates the project environment.
# - VSCode should use `.venv/bin/python` from that project.
# - Jupyter runs a kernel; the kernel should point to the same environment.
#
# Common pitfall: installing a package in one environment and running the
# notebook with another kernel. When imports mysteriously fail, first check the
# Python executable and kernel name.

# %%
import sys

import matplotlib.pyplot as plt
import numpy as np
from skimage import data, exposure, filters, img_as_float

print("Python executable:")
print(sys.executable)
print("NumPy version:", np.__version__)

# %% [markdown]
# ## A minimal scikit-image operation
#
# This is not yet a real analysis pipeline. It is an environment check:
#
# - load a small example image,
# - inspect its shape and dtype,
# - convert to float for processing,
# - smooth it,
# - display the result.
#
# When to use: at the start of a course or project, this kind of smoke test
# confirms that the scientific Python stack is available before students debug
# more complicated biology.

# %%
image = data.coins()
image_float = img_as_float(image)
smoothed = filters.gaussian(image_float, sigma=2)

print("shape:", image.shape)
print("dtype before:", image.dtype)
print("dtype after conversion:", image_float.dtype)
print("intensity range:", image_float.min(), image_float.max())

fig, axes = plt.subplots(1, 3, figsize=(10, 3))
axes[0].imshow(image, cmap="gray")
axes[0].set_title("Original")
axes[1].imshow(smoothed, cmap="gray")
axes[1].set_title("Gaussian sigma=2")
axes[2].hist(image.ravel(), bins=64)
axes[2].set_title("Histogram")
for ax in axes[:2]:
    ax.axis("off")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## A second tiny operation: contrast rescaling
#
# Contrast display and contrast transformation are different ideas. Here we
# actually change pixel values using percentiles. Later modules will discuss
# when this is appropriate.
#
# Pitfall: contrast enhancement may make figures easier to inspect, but it can
# bias measurements if performed before segmentation without a clear reason.

# %%
p2, p98 = np.percentile(image_float, (2, 98))
rescaled = exposure.rescale_intensity(image_float, in_range=(p2, p98))

fig, axes = plt.subplots(1, 2, figsize=(7, 3))
axes[0].imshow(image_float, cmap="gray")
axes[0].set_title("Original display")
axes[1].imshow(rescaled, cmap="gray")
axes[1].set_title("Rescaled values")
for ax in axes:
    ax.axis("off")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Optional exercises
#
# 1. Print the Python type, shape, dtype, minimum, and maximum of `image`.
# 2. Change `sigma` to 0.5, 2, and 5. What changes visually?
# 3. Compare displaying `image_float` with different `vmin` and `vmax` values
#    to changing the pixel values with `exposure.rescale_intensity`.

# %%
# Answer sketch (optional, removable)
print(type(image), image.shape, image.dtype, image.min(), image.max())

for sigma in [0.5, 2, 5]:
    blurred = filters.gaussian(image_float, sigma=sigma)
    print(f"sigma={sigma}", blurred.min(), blurred.max())

fig, axes = plt.subplots(1, 2, figsize=(7, 3))
axes[0].imshow(image_float, cmap="gray", vmin=0.2, vmax=0.8)
axes[0].set_title("Display contrast only")
axes[1].imshow(rescaled, cmap="gray", vmin=0, vmax=1)
axes[1].set_title("Values rescaled")
for ax in axes:
    ax.axis("off")
plt.tight_layout()
plt.show()
