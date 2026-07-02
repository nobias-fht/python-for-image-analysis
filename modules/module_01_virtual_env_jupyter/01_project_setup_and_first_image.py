# %% [markdown]
# # Module 1: virtual environments, Jupyter, and a first image
#
# Essential idea: keep project dependencies isolated, run the same Python from
# VSCode/Jupyter/terminal, and confirm the image-analysis stack works.

# %% [markdown]
# ## Terminal setup with uv
#
# Example commands, run in a terminal:
#
# ```bash
# uv init python-for-image-analysis
# cd python-for-image-analysis
# uv add numpy scipy pandas matplotlib scikit-image jupyter ipykernel
# uv run python -m ipykernel install --user --name python-image-analysis
# uv run jupyter lab
# ```
#
# In VSCode, choose the interpreter from `.venv/bin/python`.
# Useful mental model: `uv` manages the environment, and Jupyter runs a kernel
# from that environment.

# %%
import matplotlib.pyplot as plt
import numpy as np
from skimage import data, filters

# %% [markdown]
# ## A minimal scikit-image operation

# %%
image = data.coins()
smoothed = filters.gaussian(image, sigma=2)

fig, axes = plt.subplots(1, 2, figsize=(8, 3))
axes[0].imshow(image, cmap="gray")
axes[0].set_title("Original")
axes[1].imshow(smoothed, cmap="gray")
axes[1].set_title("Gaussian sigma=2")
for ax in axes:
    ax.axis("off")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Optional exercises
#
# 1. Print the Python type, shape, and dtype of `image`.
# 2. Change `sigma` and observe the effect.

# %%
# Answer sketch (optional, removable)
print(type(image), image.shape, image.dtype)
for sigma in [0.5, 2, 5]:
    blurred = filters.gaussian(image, sigma=sigma)
    print(sigma, blurred.min(), blurred.max())
