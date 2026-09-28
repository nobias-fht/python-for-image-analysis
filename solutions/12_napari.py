# %% [markdown]
# # Module 12: interactive image exploration with napari
#
# [napari](https://napari.org/) is an open-source, multi-dimensional image
# viewer for Python. It is designed for exploring scientific images and can
# display images, labels, points, shapes, surfaces, and tracks as separate
# interactive layers. Because napari is built around NumPy arrays, it can also
# be controlled directly from Python and extended with plugins.
#
# ### Objective
#
# - Install and start napari
# - Explore images and labels with the graphical interface
# - Interact with a napari viewer from its built-in console
# - Install and try a napari plugin

# %% [markdown]
# ## 1 - Install napari
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
# Open a terminal in the project directory and install napari with all of its
# optional desktop dependencies:
#
# `uv pip install "napari[all]"`
#
# Start napari from the same environment:
#
# `uv run napari`
#
# </div>

# %% [markdown]
# ## 2 - napari walk-through
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
# Let's have a little tour.
#
# - **Load data:** open an image by dragging it into napari or using
#   **File → Open File(s)**.
# - **Adjust contrast:** change the contrast limits, colormap, gamma, and
#   opacity in the image-layer controls.
# - **Work with layers:** select, hide, reorder, rename, duplicate, and remove
#   layers in the layer list.
# - **Create a mask layer:** add a Labels layer and observe that integer values
#   are displayed as different labels.
# - **Modify a mask:** use the paint, erase, fill, and label-picker tools and
#   change the brush size.
# - **Save a mask:** select the Labels layer and use **File → Save Selected
#   Layer(s)** to save the edited mask.
#
# </div>
#

# %% [markdown]
# ## 3 - Use the built-in console
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
#   napari includes an IPython console that gives you access to the running
# viewer. Open it from **Window → Console**. The current viewer is
# available through the variable `viewer`.
#
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
# In the built-in console:
#
# 1. List the layers with `viewer.layers`.
# 2. Select an image layer and inspect its NumPy array with
#    `viewer.layers.selection.active.data.shape` and
#    `viewer.layers.selection.active.data.dtype`.
# 3. Rename the active layer by assigning to its `.name` property.
# 4. Change the active image layer's colormap by assigning a colormap name to
#    its `.colormap` property.
# 5. Create a mask from the image and add it as a Labels layer. For example:
#
#    ```
#    image = viewer.layers.selection.active.data
#    mask = image > image.mean()
#    viewer.add_labels(mask, name="threshold mask")
#    ```
#
# 6. Modify the mask with the Labels painting tools and confirm in the console
#    that the layer data changed.
#
# </div>

# %% [markdown]
# ## 4 - Install a napari plugin
#
# Plugins add file readers, processing tools, sample data, and new widgets to
# napari. They can be discovered through the
# [napari hub](https://www.napari-hub.org/) or from napari's plugin installer.
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
# 1. Open **Plugins → Install/Uninstall Plugins**.
# 2. Search for a plugin that is useful for your work, or choose one from the
#    napari hub.
# 3. Read its documentation and check its supported napari and Python versions.
# 4. Install the plugin and restart napari if requested.
# 5. Find the plugin in the **Plugins** menu, open it, and try one operation on
#    an image.
# 6. Identify what the plugin added: a reader, writer, widget, processing
#    command, or sample dataset.
#
# </div>
