# %% [markdown]
# # Module 6: Practical project
#
# Time: 2 hours.
#
# In this project, we are confronted to a real-world image analysis problem. We have data
# acquired by a collaborator who wants to know the distribution of intensity in the nucleus
# of their nucleosome target.

# %%
from python_for_ia import project_data
from pathlib import Path

# path where to save the data
parent_folder = Path("data")

# we download the data
image_folder = project_data(parent_folder)
print(f"Image path: {image_folder.absolute()}")

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
#   Every image analysis project starts  by having a look at the images:
#
#   - Load the images in a list
#   - Print their shape
#   - For every image, plot both channels next to each other
#
#   <b>Hint</b>: if `type(my_path)` is a `Path`, then you can call `.glob("*.tif")` on it
#   to obtain a list of files. e.g.: `list(my_path.glob("*.tif"))`.
# </div>

# %%
from tifffile import imread
import matplotlib.pyplot as plt

# --- Exercise
files = list(image_folder.glob("*.tif"))
images = [imread(f) for f in files]
for img in images:
    print(f"Image size: {img.shape}")

fig, axes = plt.subplots(
    len(images),
    3,
    figsize=(8, 16),
    gridspec_kw={"width_ratios": [1.4, 1.4, 1]},
    constrained_layout=True,
)

for i in range(len(images)):
    axes[i, 0].imshow(images[i][0])
    axes[i, 0].set_title("Channel 0")
    axes[i, 0].axis("off")

    axes[i, 1].imshow(images[i][1])
    axes[i, 1].set_title("Channel 1")
    axes[i, 1].axis("off")

    axes[i, 2].hist(images[i][0].ravel(), bins=64, alpha=0.5)
    axes[i, 2].hist(images[i][1].ravel(), bins=64, alpha=0.5)
    axes[i, 2].set_title("Histogram")
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
#   How would you proceed with the analysis? Which steps would you try?
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
#   Implement a full image analysis pipeline!
# </div>
