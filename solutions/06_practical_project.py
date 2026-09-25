# %% [markdown]
# # Module 6: Practical project
#
# Time: 2 hours.
#
# In this project, we are confronted to a real-world image analysis problem. We have data
# acquired by a collaborator who wants to know the distribution of intensity in the nucleus
# of their nucleosome target.
#
# ### Question
#
# - What does it take to extract meaningful insights from images?
#
# ### Objective
#
# - Get comfortable exploring data.
# - Apply image analysis operations that we have learned about to real data.
# - Extract the statistics we are interested in.

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
#   Every image analysis project starts  by having a look at the images:
#
#   - Load the images in a list and print their shape,
#   - For each image display the data.
#
#   <details>
#   <summary>
#   <strong>Hint</strong>
#   </summary>
#
#   A `Path` object has a `.glob` method that can be used match file name patterns inside a directory, e.g. `.glob(*.txt)` will generate all the files ending in `.txt`.
# </div>

# %%
from python_for_ia import project_data

from pathlib import Path
from skimage.io import imread
import matplotlib.pyplot as plt

# downloading the data we will work on
data_path = project_data(Path("../data"))

# Load the files in a list, print their shapes
# --- Exercise
files = list(Path(data_path).glob("*.tif"))
images = [imread(f) for f in files]
for img in images:
    print(f"Image size: {img.shape}")
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
#   What do you the axes are?
#
#   Note that these images do not have their metadata saved correctly. This will happen 🤷‍♀️.
# </div>

# %%
# Display the data in each image
# --- Exercise
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
#
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
#
#   Implement a full image analysis pipeline!
# </div>

# %% [markdown]
#
