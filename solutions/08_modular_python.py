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
# Your collaborator wants to use your pipeline and analyse another image with a different background removal settings.
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
#   <strong style="color: #21457f;">Exercise 1 - Reuse your notebook code</strong><br>
#   <ol>
#     <li>Open your module 6 notebook.</li>
#     <li>Copy the background-removal code for one image, including the imports and image loading.</li>
#     <li>Keep your original parameter value.</li>
#     <li>Store the image as <code>image</code> and the corrected channel as <code>original_result</code>.</li>
#     <li>Run the cell.</li>
#   </ol>
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
#   Which variables did you need to bring along for the copied code to run?
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
#   <strong style="color: #21457f;">Exercise 2 - Extract a function
# </strong><br>
#   Write a function <code>remove_background(channel, radius)</code> (or use sigma for your method). Keep loading and plotting outside the function.
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
#   <strong style="color: #21457f;">Exercise 3 - Reuse the function
# </strong><br>
#   <ol>
#     <li>Run your function with the original parameter value. Store the output as <code>result_original</code>.
#     <li>Run it with a different value. Store the output as <code>result_changed</code>.
#     <li>Plot both results side by side. Include the parameter values in the titles.
#   </ol>
# </div>

# %%
# --- Exercise
# Run your function and plot the result.
result_original = remove_background(image[0], 16)
result_changed = remove_background(image[0], 8)

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
vmax = max(result_original.max(), result_changed.max())
axes[0].imshow(result_original, cmap="gray", vmin=0, vmax=vmax)
axes[0].set_title("Radius: 16 pixels")
axes[1].imshow(result_changed, cmap="gray", vmin=0, vmax=vmax)
axes[1].set_title("Radius: 8 pixels")
for ax in axes:
    ax.set_axis_off()
plt.tight_layout()
plt.show()
# ---

# %% [markdown]
# Run this check to confirm that extracting the function preserved the original result:

# %%
import numpy as np

np.testing.assert_array_equal(result_original, original_result)

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
#   How would you use this function on a second image without changing its code?
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
# <strong>Exercise 1 - Move the function</strong>
# <ol>
#   <li>Create <code>analysis.py</code> beside your notebook.</li>
#   <li>Move <code>remove_background</code> into it.</li>
#   <li>Add the imports your function needs inside <code>analysis.py</code>.</li>
# </ol>
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
# <strong>Exercise 2 - Import and check</strong>
# <ol>
#   <li>Replace the notebook's function definition with
#       <code>from analysis import remove_background</code>.</li>
#   <li>Restart the kernel.</li>
#   <li>Run the notebook from the top through the two-parameter comparison.</li>
#   <li>Check that the plots and equality check still work.</li>
# </ol>
# </div>

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
#   Why does analysis.py need its own imports, even though the notebook already imports those libraries?
# </div>
#
# Python caches imported modules. After editing <code>analysis.py</code>, save it and restart the kernel to load your changes.

# %% [markdown]
# ## 3 - Make parameters explicit
#
# Time: 10 minutes.
#
# A settings object groups named parameters and their defaults. We start with one parameter and add others as the analysis grows.
#

# %% [markdown]
# <div style="
#   background: #fff8db;
#   border-left: 6px solid #e2b200;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #6b5300;
# ">
#   <strong>Type hints</strong>
#   <p>Type hints describe the values code expects.</p>
#   <pre><code>radius: int = 16
# sigma: float = 5.0</code></pre>
#   <ul>
#     <li><code>int</code>: an integer.</li>
#     <li><code>float</code>: a floating-point number.</li>
#     <li>The value after <code>=</code> is assigned to the variable.
#         In a dataclass field, it defines the default.</li>
#   </ul>
#   <p>Functions can describe their inputs and output too:</p>
#   <pre><code>def remove_background(channel: np.ndarray, radius: int) -&gt; np.ndarray:</code></pre>
#   <p><code>-&gt; np.ndarray</code> describes the returned value.</p>
#   <p>Type hints help readers and editors. They do not check values at runtime
#      or specify an array's shape.</p>
# </div>

# %% [markdown]
# <div style="
#   background: #fff8db;
#   border-left: 6px solid #e2b200;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #6b5300;
# ">
#   <strong>Dataclasses</strong>
#   <p>A dataclass groups related values into one object.
#      Here, it stores analysis parameters.</p>
#   <pre><code>from dataclasses import dataclass
#
# @dataclass(frozen=True)
# class Settings:
#     tophat_radius: int = 16</code></pre>
#   <ul>
#     <li><code>@dataclass</code> supplies the code for creating and displaying the object.</li>
#     <li><code>tophat_radius</code> is a field with a type hint and a default.</li>
#     <li><code>frozen=True</code> prevents assigning new values to its fields.</li>
#   </ul>
#   <p>Create configurations and access a parameter by name:</p>
#   <pre><code>settings_original = Settings()
# settings_changed = Settings(tophat_radius=8)
#
# settings_original.tophat_radius</code></pre>
# </div>

# %% [markdown]
# Use your method's parameter name, such as `gaussian_sigma` for Gaussian
# background estimation, and your original value as the default.
#
# <div style="
#   background: #accffb;
#   border-left: 6px solid #2f80ed;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #21457f;
# ">
#   <strong style="color: #21457f;">Exercise 1 - Define settings</strong><br>
#   <ol>
#     <li>Copy the template below into the next cell.</li>
#     <li>Replace <code>pass</code> with a field for your background-removal
#         parameter.</li>
#     <li>Use your original parameter value as its default.</li>
#   </ol>
# </div>
#
# ```python
# from dataclasses import dataclass
#
# @dataclass(frozen=True)
# class Settings:
#     pass  # Example: tophat_radius: int = 16
# ```

# %%
# --- Exercise
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    tophat_radius: int = 16


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
#   <strong style="color: #21457f;">Exercise 2 - Create two configurations</strong><br>
#   <ol>
#     <li>Create <code>settings_original = Settings()</code>.</li>
#     <li>Create <code>settings_changed</code> with the changed value from section 1.</li>
#     <li>Print both objects.</li>
#   </ol>
# </div>

# %%
# --- Exercise
settings_original = Settings()
settings_changed = Settings(tophat_radius=8)

print(settings_original)
print(settings_changed)
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
#   <strong style="color: #21457f;">Exercise 3 - Use your settings</strong><br>
#   <ol>
#     <li>Call <code>remove_background</code> using the parameter from each
#         settings object.</li>
#     <li>Store the outputs as <code>configured_original</code> and
#         <code>configured_changed</code>.</li>
#     <li>Plot both results side by side.</li>
#   </ol>
# </div>
#
# Hint: <code>configured_original = remove_background(image[0], settings_original.tophat_radius)</code>

# %%
# --- Exercise
configured_original = remove_background(image[0], settings_original.tophat_radius)
configured_changed = remove_background(image[0], settings_changed.tophat_radius)

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
vmax = max(configured_original.max(), configured_changed.max())
for ax, corrected, config in zip(
    axes,
    [configured_original, configured_changed],
    [settings_original, settings_changed],
):
    ax.imshow(corrected, cmap="gray", vmin=0, vmax=vmax)
    ax.set_title(f"Radius: {config.tophat_radius} pixels")
    ax.set_axis_off()
plt.tight_layout()
plt.show()
# ---

# %% [markdown]
# Check that both configurations reproduce the results from section 1.
# Use the same image and the same two parameter values.

# %%
np.testing.assert_array_equal(configured_original, result_original)
np.testing.assert_array_equal(configured_changed, result_changed)

# %% [markdown]
# <div style="
#   background: #e8f7ec;
#   border-left: 6px solid #2f9e44;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #1f5f2c;
# ">
# <strong style="color: #1f5f2c;">Question</strong><br>
#   Where can you find the parameter value used to produce <code>configured_changed</code>?
# </div>
#
# With one parameter, settings may seem unnecessary. As the analysis grows, they keep parameters together and let you pass one configuration to your pipeline.

# %% [markdown]
# ## 4 - Build a reusable analysis project
#
# Time: 10 minutes of introduction + 80 minutes of guided practical.
#
# Turn your module 6 analysis into code that can process another image with different
# settings. Keep the scientific algorithm unchanged.
#
# ### Before you start: organise by responsibility

# %% [markdown]
# <div style="
#   background: #fff8db;
#   border-left: 6px solid #e2b200;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #6b5300;
# ">
#   <strong>Why use multiple modules?</strong>
#   <p>Group code that has a shared purpose. Computing measurements and saving a CSV
#   are different responsibilities.</p>
#   <p>Separating them lets you change how results are saved without changing how
#   they are calculated.</p>
#   <p>Each module needs a clear purpose and its own imports. Choose the file
#   organisation that makes sense for your analysis.</p>
# </div>

# %% [markdown]
# <div style="
#   background: #e8f7ec;
#   border-left: 6px solid #2f9e44;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #1f5f2c;
# ">
#   <strong>Discussion</strong>
#   <p>Which steps in your analysis belong together?</p>
# </div>

# %% [markdown]
# <div style="
#   background: #fff8db;
#   border-left: 6px solid #e2b200;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #6b5300;
# ">
#   <strong>NumPy-style docstrings</strong>
#   <p>A docstring appears immediately inside a function or class. It explains how
#   to use it.</p>
#   <ul>
#     <li>Start with a short description of its purpose.</li>
#     <li>Use <code>Parameters</code> for inputs, including shape, channels, and units.</li>
#     <li>Use <code>Returns</code> for outputs.</li>
#     <li>Use <code>Attributes</code> to describe settings fields.</li>
#   </ul>
#   <p>Type hints describe types. Docstrings explain meaning.</p>
# </div>

# %% [markdown]
# Use this NumPy-style example as a guide. Adapt it to your own background-removal
# method.
#
# ```python
# def remove_background(channel: np.ndarray, radius: int) -> np.ndarray:
#     """Remove background using a white top-hat filter.
#
#     Parameters
#     ----------
#     channel : np.ndarray
#         A 2D image channel.
#     radius : int
#         Radius of the disk footprint, in pixels.
#
#     Returns
#     -------
#     np.ndarray
#         Background-corrected channel, with the same shape as the input.
#     """
#     # Your existing computation goes here.
# ```
#
# Document settings with their meaning and units too:
#
# ```python
# @dataclass(frozen=True)
# class Settings:
#     """Parameters controlling the analysis.
#
#     Attributes
#     ----------
#     tophat_radius : int
#         Radius of the background-removal disk, in pixels. Default is 16.
#     """
#
#     tophat_radius: int = 16
# ```
#
# ### 1. Save a baseline - 10 minutes

# %% [markdown]
# <div style="
#   background: #accffb;
#   border-left: 6px solid #2f80ed;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #21457f;
# ">
#   <strong>Exercise 1 - Preserve the original result</strong>
#   <ol>
#     <li>Run your original module 6 analysis on one image.</li>
#     <li>Save its labels and measurement table to files.</li>
#     <li>Record the image filename and parameter values.</li>
#   </ol>
# </div>

# %% [markdown]
# **Hint:** use `np.save()` for labels and `table.to_csv(..., index=False)` for
# measurements. Keep these baseline files unchanged during refactoring so you can
# load them after restarting the kernel.
#
# ### 2. Extract and check - 20 minutes

# %% [markdown]
# <div style="
#   background: #accffb;
#   border-left: 6px solid #2f80ed;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #21457f;
# ">
#   <strong>Exercise 2 - Move one computation</strong>
#   <ol>
#     <li>Choose one computation to extract.</li>
#     <li>Give it explicit inputs and returned outputs.</li>
#     <li>Move it into a module with the imports it needs.</li>
#     <li>Call it from your notebook.</li>
#     <li>Compare its output with the original computation on the same input.</li>
#   </ol>
# </div>

# %% [markdown]
# **Checkpoint: did moving the code change its result?**
#
# Regression check: use the original computation's output as the expected result.
# For example, once your segmentation returns labels:
#
# ```python
# np.testing.assert_array_equal(refactored_labels, original_labels)
# ```
#
# For floating-point measurements:
# ```python
# import pandas as pd
#
# pd.testing.assert_frame_equal(
#     refactored_table.set_index("label").sort_index(),
#     original_table.set_index("label").sort_index(),
#     check_exact=False,
#     rtol=1e-6,
#     atol=1e-8,
# )
# ```
#
# Continue extracting the remaining computations once your first check passes.
#
# ### 3. Connect the steps - 20 minutes

# %% [markdown]
# <div style="
#   background: #accffb;
#   border-left: 6px solid #2f80ed;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #21457f;
# ">
#   <strong>Exercise 3 - Build the entry point</strong>
#   <ol>
#     <li>Move <code>Settings</code> into a module and add the remaining parameters.</li>
#     <li>Create one entry point that receives an image and settings.</li>
#     <li>Call your analysis functions in order.</li>
#     <li>Return labels and a measurement table.</li>
#     <li>Document the entry point and settings using NumPy-style docstrings.</li>
#   </ol>
# </div>

# %% [markdown]
# **Hint:** aim for one call such as `labels, table = run_image(image, settings)`.
# A function or a class is fine. Document the input shape, channel order, parameter
# units, and the meaning of both outputs.
#
# **Checkpoint:** one call runs the complete analysis.
#
# ### Debugging pause - 10 minutes
#
# This supplied example expects channels first, but receives a channel-last image.
# It runs without an exception and selects the wrong data.

# %%
import numpy as np


def select_nucleus_channel(image):
    nuclei = image[0]  # Expects (channel, y, x).
    return nuclei


channel_last = np.zeros((4, 5, 2))
channel_last[..., 0] = 1
channel_last[..., 1] = 7

# %% [markdown]
# <div style="
#   background: #e8f7ec;
#   border-left: 6px solid #2f9e44;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #1f5f2c;
# ">
#   <strong>Predict</strong>
#   <p>What shape should one channel have, and what shape will <code>image[0]</code> have here?</p>
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
#   <strong>Live demonstration - Inspect the mismatch</strong>
#   <ol>
#     <li>Set a breakpoint on <code>nuclei = image[0]</code>.</li>
#     <li>Debug the next cell in VS Code.</li>
#     <li>Inspect <code>image.shape</code>, then step over the assignment.</li>
#     <li>Inspect <code>nuclei.shape</code> and explain the mismatch.</li>
#   </ol>
# </div>

# %%
wrong_channel = select_nucleus_channel(channel_last)
print("Selected shape:", wrong_channel.shape)

# %% [markdown]
# <div style="
#   background: #accffb;
#   border-left: 6px solid #2f80ed;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #21457f;
# ">
#   <strong>Exercise 4 - Fix and check</strong>
#   <ol>
#     <li>Use <code>np.moveaxis</code> to convert this image to channel-first layout.</li>
#     <li>Call <code>select_nucleus_channel</code> again and store the result as <code>correct_channel</code>.</li>
#     <li>Run the checks below.</li>
#   </ol>
# </div>

# %%
# --- Exercise
channel_first = np.moveaxis(channel_last, -1, 0)
correct_channel = select_nucleus_channel(channel_first)
# ---

# %%
assert correct_channel.shape == (4, 5)
np.testing.assert_array_equal(correct_channel, np.ones((4, 5)))

# %% [markdown]
# **Hint:** three dimensions alone do not identify the channel axis. Make this
# conversion at the input boundary when you know the source layout.
#
# ### 4. Verify and reuse - 20 minutes

# %% [markdown]
# <div style="
#   background: #accffb;
#   border-left: 6px solid #2f80ed;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #21457f;
# ">
#   <strong>Exercise 5 - Run from a fresh kernel</strong>
#   <ol>
#     <li>Save your modules and restart the kernel.</li>
#     <li>Run your analysis with the original image and settings.</li>
#     <li>Load the saved baseline and compare labels and measurements.</li>
#     <li>Inspect the segmentation visually alongside the original image.</li>
#     <li>Run another image with different settings, keeping both results.</li>
#   </ol>
# </div>

# %% [markdown]
# **Finish when:** the original result is reproduced and the second analysis
# requires no edits inside your analysis modules.

# %% [markdown]
# <div style="
#   background: #f3f4f6;
#   border-left: 6px solid #6b7280;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #374151;
# ">
#   <strong>Optional Exercise 1 - Extend the analysis</strong>
#   <ol>
#     <li>Add folder processing or compare several parameter values.</li>
#     <li>Reuse your existing single-image entry point.</li>
#   </ol>
# </div>

# %% [markdown]
# <div style="
#   background: #f3f4f6;
#   border-left: 6px solid #6b7280;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #374151;
# ">
#   <strong>Optional Exercise 2 - Compare designs</strong>
#   <ol>
#     <li>Open the <a href="../src/nuclei_pipeline/">reference pipeline</a>, starting with <a href="../src/nuclei_pipeline/pipeline.py">pipeline.py</a>.</li>
#     <li>Compare file organisation, function inputs and outputs, and handling of settings.</li>
#     <li>Note one design choice you would keep in your version and one you might change.</li>
#   </ol>
# </div>
