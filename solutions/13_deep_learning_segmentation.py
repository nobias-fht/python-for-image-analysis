# %% [markdown]
# # Module 13: image segmentation with Cellpose
#
# Cellpose is one of the most useful deep-learning segmentation algorithm in our microscopy
# image segmentation. There is multiple reasons for that:
#
# - Originally trained on a diverse biological datasets, it is very robust to different samples
# - It deals well with touching objects
# - The authors keep adding new highly performant models, e.g. SAM-Cellpose
# - There is a GUI that allows you to correct the predictions, and fine-tune the model
#
# Here is the [docs](https://cellpose.readthedocs.io/en/latest/), and the various [settings](https://cellpose.readthedocs.io/en/latest/settings.html#settings)
# that can be used.
#
#
# ## 1 - Installing Cellpose
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
# Add `cellpose` to the project and restart the kernel.
# </div>
# %%
from pathlib import Path

import matplotlib.pyplot as plt
from tifffile import imread, imwrite

from cellpose import models

# %% [markdown]
# ## 2 - Running Cellpose programmatically
#
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
# Remember our practical images? One channel was particularly noisy with a strong
# background fluorescence.
#
# Import all the images and retain only the first channel.
#
# </div>

# %%
# --- Exercise
files = list(Path("../data/practical_project/noisy").glob("*.tif"))
images = [imread(f)[0] for f in files]
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
# Checkout the "Settings" section on the Cellpose docs (see link in the introduction). Run
# Cellpose on the list of images.
#
# </div>

# %%
# --- Exercise
model = models.CellposeModel(gpu=True)
masks, flows, _ = model.eval(images)
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
# Did it work? Let's plot the resulting masks next their corresponding input image.
#
# </div>

# %%
# --- Exercise
fig, axes = plt.subplots(len(images), 2, figsize=(6, 14), constrained_layout=True)

for i in range(len(images)):
    axes[i, 0].imshow(images[i])
    axes[i, 0].set_title(f"Image {i}")
    axes[i, 0].axis("off")

    axes[i, 1].imshow(masks[i])
    axes[i, 1].set_title("Mask")
    axes[i, 1].axis("off")
# ---

# %% [markdown]
# ## 3 - Integrating Cellpose in our pipeline
#
# The Cellpose result should convince you that it can replace several steps of our pipeline.
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
# Modify your pipeline to integrate Cellpose.
#
# </div>
