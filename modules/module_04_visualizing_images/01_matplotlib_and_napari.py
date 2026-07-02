# %% [markdown]
# # Module 4: visualizing images
#
# Essential ideas: display choices affect interpretation. Use contrast limits,
# colormaps, overlays, masks, and labels deliberately.

# %%
import matplotlib.pyplot as plt
import numpy as np
from skimage import color, filters, measure, segmentation

from course_utils import make_blobs

# %%
image = make_blobs(seed=11)
mask = image > filters.threshold_otsu(image)
labels = measure.label(mask)
labels = segmentation.clear_border(labels)

# %% [markdown]
# ## Images, masks, labels, and overlays with matplotlib

# %%
overlay = color.label2rgb(labels, image=image, bg_label=0, alpha=0.35)

fig, axes = plt.subplots(1, 4, figsize=(11, 3))
axes[0].imshow(image, cmap="gray")
axes[0].set_title("image")
axes[1].imshow(image, cmap="magma", vmin=0, vmax=0.8)
axes[1].set_title("contrast")
axes[2].imshow(mask, cmap="gray")
axes[2].set_title("mask")
axes[3].imshow(overlay)
axes[3].set_title("labels")
for ax in axes:
    ax.axis("off")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Napari preview
#
# Napari is useful for interactive inspection of multidimensional images,
# label layers, points, and shapes.

# %%
try:
    import napari

    viewer = napari.Viewer()
    viewer.add_image(image, name="synthetic image", colormap="gray")
    viewer.add_labels(labels, name="segmentation")
except ImportError:
    print("napari is optional. Install with: uv add --optional napari 'napari[all]'")

# %% [markdown]
# ## Optional exercises
#
# 1. Change `vmin` and `vmax` to make dim objects visible.
# 2. Plot label boundaries over the grayscale image.

# %%
# Answer sketch (optional, removable)
boundaries = segmentation.find_boundaries(labels)
rgb = np.dstack([image, image, image])
rgb[boundaries] = [1, 0, 0]
plt.imshow(rgb)
plt.axis("off")
plt.show()
