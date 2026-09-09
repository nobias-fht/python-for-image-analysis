# %% [markdown]
# # Module 12: image segmentation with Cellpose
#
# https://cellpose.readthedocs.io/en/latest/
# https://cellpose.readthedocs.io/en/latest/settings.html#settings
# %%
from pathlib import Path

import matplotlib.pyplot as plt
from tifffile import imread, imwrite

from cellpose import models, io
from cellpose.io import imread

# %%
# Load data
files = list(Path("../data/practical_project/noisy").glob("*.tif"))
images = [imread(f)[0] for f in files]
for img in images:
    print(f"Image size: {img.shape}")

# %%

io.logger_setup()

model = models.CellposeModel(gpu=True)
nimg = len(images)
masks, flows, styles = model.eval(images)

# %%
# Compare raw and prediction
fig, axes = plt.subplots(len(images), 2, figsize=(6, 14), constrained_layout=True)

for i in range(len(images)):
    axes[i, 0].imshow(images[i])
    axes[i, 0].set_title(f"Image {i}")
    axes[i, 0].axis("off")

    axes[i, 1].imshow(masks[i])
    axes[i, 1].set_title("Mask")
    axes[i, 1].axis("off")

# %%
