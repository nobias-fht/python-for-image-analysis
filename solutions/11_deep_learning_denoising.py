# %% [markdown]
# # Module 11: denoising images with Noise2Void
#
# Noise in microscopy images is often a limiting factor for downstream analysis. A popular
# algorithm for deep-learning denoising is Noise2Void. It leverages the statistical independence
# of pixel noise to restore the image.
#
# What is Noise2Void good for?
#
# - It is self-supervised, no need to have ground truth images for training
# - It trains fast!
# - Most microscopy images contain noise that is uncorrelated spatially.
#
# What are its limitations?
#
# - Some microscopy methods have spatial correlations in the noise, if these are strong enough
# then Noise2Void will make the correlation appear strongly in the resulting image
#
# The way to run Noise2Void is through the [CAREamics library](https://careamics.github.io/latest/).
#
#
# ## 1 - Installing CAREamics
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
# Add `careamics` to the project and restart the kernel.
# </div>

# %%
from pathlib import Path

import matplotlib.pyplot as plt

from careamics.careamist import CAREamist
from careamics.plotting import plot_loss

from python_for_ia import images_with_noise

# %% [markdown]
# ## 2 - Running Noise2Void in CAREamics
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
# Let's look at the example data. Plot several slices of a cropped region (e.g. 100 to 150
# in X and Y) to make the noise apparent.
#
# </div>

# %%
noisy_imgs = images_with_noise()

# --- Exercise
z = [20, 30, 40]
slices = (slice(100, 150),) * 2

fig, axes = plt.subplots(1, len(z), figsize=(6, 10), constrained_layout=True)

for i in range(len(z)):
    axes[i].imshow(noisy_imgs[z[i]][slices])
    axes[i].set_title(f"Slice {z[i]}")
    axes[i].axis("off")
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
# CAREamics has a single function call to create a configuration. Find the correct function
# to create a N2V configuration in [the documentation](https://careamics.github.io/latest/content/guides/current/)
# and create one.
#
# </div>
#
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
#   What `data_type` and `axis` should use?
# </div>

# %%
# --- Exercise
from careamics.config import create_n2v_config

config = create_n2v_config(
    experiment_name="n2v",
    data_type="array",
    axes="ZYX",
    batch_size=16,
    patch_size=(8, 64, 64),
    num_epochs=30,
)
# ---

careamist = CAREamist(config)
careamist.train(train_data=noisy_imgs)

# %% [markdown]
# As often with deep-learning, we want to look at the loss to see how the training went.
#
# <div style="
#   background: #fff8db;
#   border-left: 6px solid #e2b200;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #8a6a00;
# ">
#   <strong style="color: #8a6a00;">Note</strong><br>
#
#   The loss in Noise2Void is a bit meaningless. Indeed, it compares a noisy pixel (input)
#   to a predicted value (hopefully denoised). Since the input is noisy, the best denoised
#   pixel value will be different from the input value and the loss will never reach 0. Even
#   worse, fluctuations do not indicate improvement or not.
# </div>

# %%
# Plot loss
plot_loss(careamist.get_losses(), plot_metrics=False, plot_learning_rate=False)

# %% [markdown]
# Let's perform some prediction and compare with the original image.
#
# <div style="
#   background: #fff8db;
#   border-left: 6px solid #e2b200;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #8a6a00;
# ">
#   <strong style="color: #8a6a00;">Note</strong><br>
#
#   Predicting on training data is normally very bad practice when it comes to judging the
#   performances of a deep learning algorithm. Why is it okay with Noise2Void? It is self-supervised
#   and is not meant to be applied on any other data. We did not bias the algorithm towards
#   a particular ground-truth. Therefore we can predict on our training data!
# </div>

# %%
# Predict
predictions, _ = careamist.predict(pred_data=noisy_imgs)

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
# Plot the same slices and spatial crops as in the beginning of the module, but this time
# compare three images: the noisy input, the predicted denoised image and the residual image
# (input - prediction).
#
# <b>Hint</b>: Inspect the type of `predictions`.
#
# </div>

# %%
# --- Exercise
fig, axes = plt.subplots(len(z), 3, figsize=(8, 10), constrained_layout=True)

for i in range(len(z)):
    noisy = noisy_imgs[z[i]][slices]
    pred = predictions[0][z[i]][slices]
    res = noisy - pred

    axes[i, 0].imshow(noisy)
    axes[i, 0].set_title(f"Image {z[i]}")
    axes[i, 0].axis("off")

    axes[i, 1].imshow(pred)
    axes[i, 1].set_title("Prediction")
    axes[i, 1].axis("off")

    axes[i, 2].imshow(res)
    axes[i, 2].set_title("Residuals")
    axes[i, 2].axis("off")
# ---


# %% [markdown]
# <div style="
#   background: #f3f4f6;
#   border-left: 6px solid #6b7280;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #374151;
# ">
#   <strong>Optional Exercise</strong><br>
#   Save the predictions to disk.
# </div>
