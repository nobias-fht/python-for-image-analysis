# %% [markdown]
# # Module 12: segmenting cells with Cellpose
#

# %%
from pathlib import Path

import matplotlib.pyplot as plt
from tifffile import imread, imwrite

from careamics.careamist import CAREamist
from careamics.config.factories import create_n2v_config
from careamics.plotting import plot_loss

# %%
# Load data
files = list(Path("../data/practical_project/noisy").glob("*.tif"))
images = [imread(f)[0] for f in files]
for img in images:
    print(f"Image size: {img.shape}")

# %%
config = create_n2v_config(
    experiment_name="n2v_ch0",
    data_type="array",
    axes="YX",
    batch_size=2,
    patch_size=(64, 64),
    num_epochs=10,
)

careamist = CAREamist(config)
careamist.train(train_data=images)

# %%
# Plot loss
plot_loss(careamist.get_losses())

# %%
# Predict
predictions, _ = careamist.predict(pred_data=images)

# %%
# Compare raw and prediction
fig, axes = plt.subplots(len(images), 2, figsize=(6, 14), constrained_layout=True)

for i in range(len(images)):
    axes[i, 0].imshow(images[i])
    axes[i, 0].set_title(f"Image {i}")
    axes[i, 0].axis("off")

    axes[i, 1].imshow(predictions[i])
    axes[i, 1].set_title("Prediction")
    axes[i, 1].axis("off")


# %%
# Save images
out_path = Path("../data/practical_project/denoised")
out_path.mkdir(exist_ok=True, parents=True)

for i in range(len(predictions)):
    imwrite(out_path / f"image_{i}.tif", predictions[i])
