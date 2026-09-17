# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.4
#   kernelspec:
#     display_name: python-for-image-analysis (3.13.5)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Module 8: a reusable image-analysis pipeline
#
# Your collaborator wants to use your pipeline and analyse another image with a different background removal radius.
#
# Start from your module 6 notebook and make that step reusable.
#
# Then organise your full analysis into reusable Python modules.

# %% [markdown]
# ## 1 - From a notebook cell to a function
#
# Time: 10 minutes.
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
#   Open your module 6 notebook. Find the background-removal step and copy the
#   code needed to run it on <strong>one image</strong> into the cell below.
#   Bring over imports and loading code as needed, and adapt the file path.
#   Use radius <code>16</code>. Keep the loaded image as <code>image</code> and
#   the corrected nucleus channel as <code>original_result</code>.<br>
#   Run it here. Which other variables or cells did you need to bring along?
# </div>

# %%
# --- Exercise
from pathlib import Path

import matplotlib.pyplot as plt
from skimage import morphology
from tifffile import imread

project_root = Path.cwd()
if project_root.name in {"solutions", "exercises"}:
    project_root = project_root.parent
image_folder = project_root / "data/practical_project/noisy"
image_paths = sorted(image_folder.glob("*.tif"))
if not image_paths:
    raise FileNotFoundError(f"Place the module 6 TIFF images in {image_folder}.")
image = imread(image_paths[0])
channel = image[0]
radius = 16
original_result = morphology.white_tophat(channel, footprint=morphology.disk(radius))
plt.imshow(original_result, cmap="gray")
plt.title("Background removed")
plt.axis("off")
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
#   Which variables must exist before your copied code can run?
#   What would you copy or change to process a second image while keeping the first result?
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
#   Extract the computation into <code>remove_background(channel, radius)</code>.
#   Take a 2D channel and a radius in pixels, and return the corrected image.
#   Receive both inputs through arguments. Keep loading and plotting outside
#   the function, and preserve the original computation.
# </div>
#
# ```python
# def remove_background(channel, radius):
#     # Compute the corrected image here.
#     return corrected
# ```


# %%
# --- Exercise
# Write remove_background here.
def remove_background(channel, radius):
    footprint = morphology.disk(radius)
    return morphology.white_tophat(channel, footprint=footprint)


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
#   Call your function twice on <code>image[0]</code>, with radii
#   <code>16</code> and <code>8</code>. Keep both outputs as
#   <code>result_16</code> and <code>result_8</code>.
#   Plot them side by side with titles identifying the radii.
# </div>

# %%
# --- Exercise
# Run your function and plot the result.
result_16 = remove_background(image[0], 16)
result_8 = remove_background(image[0], 8)

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
vmax = max(result_16.max(), result_8.max())
axes[0].imshow(result_16, cmap="gray", vmin=0, vmax=vmax)
axes[0].set_title("Radius: 16 pixels")
axes[1].imshow(result_8, cmap="gray", vmin=0, vmax=vmax)
axes[1].set_title("Radius: 8 pixels")
for ax in axes:
    ax.set_axis_off()
plt.tight_layout()
plt.show()
# ---

# %% [markdown]
# Check that extracting the function preserved the result. This assertion
# passes silently if the two arrays match; otherwise it raises an error.

# %%
import numpy as np

np.testing.assert_array_equal(result_16, original_result)

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
#   Did changing the radius require editing the function?
#   How would you call it on a second image? What stays the same?
# </div>

# %% [markdown]
# ## 2 - Move the function into a module
#
# Time: 10 minutes.
#
# A module is a Python file that we can import. Keep reusable computation in
# that file, and keep image loading, experiments, and plots in the notebook.
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
#   Create <code>analysis.py</code> beside your notebook in VS Code.
#   Move <code>remove_background</code> into it, together with the
#   <code>morphology</code> import it needs. Do not copy the image loading or plots.<br>
#   Replace your earlier function-definition cell with
#   <code>from analysis import remove_background</code>.
#   Save the file, restart the kernel, and run from the top through the
#   two-radius comparison. The plots and equality check should still work.
# </div>

# %% [markdown]
# Confirm that we can also call the function through its module name.
# This makes it visible which file provides the computation.

# %%
# --- Exercise
import analysis

module_result_16 = analysis.remove_background(image[0], 16)
module_result_8 = analysis.remove_background(image[0], 8)
# ---

# %%
np.testing.assert_array_equal(module_result_16, result_16)
np.testing.assert_array_equal(module_result_8, result_8)

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
#   Why does <code>analysis.py</code> need its own import, even though the notebook
#   already imports <code>morphology</code>? Could a second notebook use this file?
# </div>
#
# Python caches imported modules. After editing <code>analysis.py</code>, save
# it, restart the kernel, and rerun the notebook to load the updated code.

# %% [markdown]
# ## 3 - Make parameters explicit
#
# Time: 10 minutes.
#
# A settings object gives names and defaults to the parameters of an analysis.
# We start with one parameter; later the same object can hold smoothing and
# segmentation parameters too. The dataclass syntax is supplied below.
# `frozen=True` prevents changing fields on an existing settings object.
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
#   Copy this scaffold into the next cell. Replace <code>pass</code> with a
#   field named <code>tophat_radius</code>, with type <code>int</code> and
#   default <code>16</code>. The radius is measured in pixels.
# </div>
#
# ```python
# from dataclasses import dataclass
#
# @dataclass(frozen=True)
# class Settings:
#     pass  # field syntax: name: type = default
# ```

# %%
# --- Exercise
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    tophat_radius: int = 16


# ---

# %% [markdown]
# Create a separate settings object for each configuration. Use the defaults
# with `Settings()`, or supply a named value with `Settings(tophat_radius=8)`.
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
#   Create <code>settings_16 = Settings()</code> and
#   <code>settings_8 = Settings(tophat_radius=8)</code>.<br>
#   Print each object, then call <code>analysis.remove_background</code> with its
#   <code>tophat_radius</code>. Keep the outputs as <code>configured_16</code>
#   and <code>configured_8</code>, and plot them side by side.
#   Leave the function in <code>analysis.py</code> unchanged.
# </div>

# %%
# --- Exercise
settings_16 = Settings()
settings_8 = Settings(tophat_radius=8)
print(settings_16)
print(settings_8)

configured_16 = analysis.remove_background(image[0], settings_16.tophat_radius)
configured_8 = analysis.remove_background(image[0], settings_8.tophat_radius)

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
vmax = max(configured_16.max(), configured_8.max())
for ax, corrected, config in zip(
    axes, [configured_16, configured_8], [settings_16, settings_8]
):
    ax.imshow(corrected, cmap="gray", vmin=0, vmax=vmax)
    ax.set_title(f"Radius: {config.tophat_radius} pixels")
    ax.set_axis_off()
plt.tight_layout()
plt.show()
# ---

# %% [markdown]
# Check that both configurations reproduce the previous results and that
# creating the second settings object left the first unchanged.

# %%
assert settings_16.tophat_radius == 16
assert settings_8.tophat_radius == 8
np.testing.assert_array_equal(configured_16, result_16)
np.testing.assert_array_equal(configured_8, result_8)

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
#   Which object describes each analysis? Where would you add a smoothing
#   parameter when the pipeline grows? Why keep both settings objects?
# </div>
#
# A printed settings object is a record of how a result was made. Store that line
# beside the result, and you can reproduce it. A loose variable named
# <code>radius</code> does not tell you that.
#
# Your analysis has one parameter here, so passing
# <code>settings_16.tophat_radius</code> is longer than passing <code>16</code>.
# It pays off once there are eight parameters. In section 4 you write one entry
# point that receives the whole settings object, and that call stops growing when
# you add a parameter.

# %% [markdown]
# ## 4 - Build a reusable analysis project
#
# Time: 1 hour of independent work.
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
#   Organise your module 6 analysis into importable Python modules.
#   Another researcher should be able to run a second image with different
#   settings without editing your analysis code.<br>
#   Choose how to group your functions. Keep this notebook for loading images,
#   calling your code, and inspecting results.
# </div>
#
# Work through the checklist in order. Keep your existing algorithm unchanged.
#
# ### 1. Keep a result to compare against
#
# - [ ] Run your module 6 notebook on one image.
# - [ ] Keep its labels, measurement table, and parameter values for comparison.
#
# ### 2. Move the computations into modules
#
# - [ ] Group related functions into `.py` files beside your notebook.
# - [ ] Extract segmentation and measurement functions, with explicit arguments and return values.
# - [ ] Keep image loading, saving, and plotting outside these functions.
#
# Each module needs its own imports. Update the notebook imports when you move
# functions, including the ones used in the warmups.
#
# **20-minute checkpoint:** call one newly extracted function from the notebook
# and check that it matches the original result.
#
# ### 3. Connect the steps
#
# - [ ] Move `Settings` into a module and add your analysis parameters.
# - [ ] Create one entry point that receives an image and settings and calls your functions.
# - [ ] Return the label image and measurement table.
# - [ ] Add a short docstring describing the input image, settings, and returned results.
#
# For example, `labels, table = run_image(image, settings)`.
# You can use a function or a class; choose the approach you can explain.
#
# A docstring is a triple-quoted string immediately inside a function or method.
# It tells someone how to use your code without reading its implementation.
# Describe the image shape and channel order, parameter units, and what each
# returned value contains. For example, adapt this to your own analysis:
#
# ```python
# def run_image(image, settings):
#     """Analyse an image of shape (channel, y, x).
#
#     Channel 0 contains nuclei; channel 1 contains the target signal.
#     Settings specify filter radii in pixels and size thresholds in pixel counts.
#     Return a 2D label image (0 is background) and a table with one row per nucleus.
#     """
#     # Your analysis steps go here.
# ```
#
# **40-minute checkpoint:** run one image through all steps with one call.
#
# ### 4. Check the result and reuse it
#
# - [ ] Import your code here, display the labels, and inspect the table.
# - [ ] Restart the kernel and run from the top with the original parameters.
# - [ ] Compare labels and measurements with your saved module 6 result.
# - [ ] Run a second image with different settings and keep both results.
#
# **60-minute checkpoint:** show that the second analysis required no edits
# inside your analysis modules.
#
# <div style="
#   background: #f3f4f6;
#   border-left: 6px solid #6b7280;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #374151;
# ">
#   <strong>Optional Exercise 1</strong><br>
#   If time remains, add folder processing or compare several parameter values.
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
#   <strong>Optional Exercise 2</strong><br>
#   Explore the <a href="../src/nuclei_pipeline/">reference pipeline</a>, starting
#   with <a href="../src/nuclei_pipeline/pipeline.py">pipeline.py</a>.
#   Compare it with your implementation. What differs in the organisation of
#   files, function inputs and outputs, and handling of settings?
#   Note one design choice you would keep in your version and one you might change.
# </div>
