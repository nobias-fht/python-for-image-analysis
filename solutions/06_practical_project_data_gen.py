# %% [markdown]
# # Module 6: data generation

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from skimage import filters
from tifffile import imread, imwrite

# %%
files = list(Path("../data/practical_project/raw").glob("*.tif"))
raw = [imread(f) for f in files]
for r in raw:
    print(f"Image size: {r.shape}")

# %%
fig, axes = plt.subplots(
    len(raw),
    3,
    figsize=(8, 22),
    gridspec_kw={"width_ratios": [1.4, 1.4, 1]},
    constrained_layout=True,
)

for i in range(len(raw)):
    axes[i, 0].imshow(raw[i][0])
    axes[i, 0].set_title("Channel 0")
    axes[i, 0].axis("off")

    axes[i, 1].imshow(raw[i][1])
    axes[i, 1].set_title("Channel 1")
    axes[i, 1].axis("off")

    axes[i, 2].hist(raw[i][0].ravel(), bins=64, alpha=0.5)
    axes[i, 2].hist(raw[i][1].ravel(), bins=64, alpha=0.5)
    axes[i, 2].set_title("Histogram")


# %%
def norm(im, ref):
    return ref.mean() * im / im.mean()


# generate background
n = len(raw)
rng = np.random.default_rng()

fig, axes = plt.subplots(3, len(raw), figsize=(12, 8), constrained_layout=True)

images = []
for i in range(n):
    img = raw[i][0]

    # --- Bg

    # # pull a number
    # k = rng.integers(3, 6, 1)

    # # choose among the images
    # indices = rng.choice(n, k, replace=False)

    # # choose strength
    # alphas = rng.dirichlet(np.ones(k))

    # # sum images
    # bg = np.sum([alphas[a_idx] * raw[idx][0] for a_idx, idx in enumerate(indices)], axis=0)

    # # gaussian blur
    # bg = filters.gaussian(bg, sigma=80)
    # bg = norm(bg, img)

    yy, xx = np.indices(img.shape)
    bg = np.zeros_like(img)
    cy = 0.4 * img.shape[0]
    cx = 0.7 * img.shape[1]
    sigma = 250

    bg = np.exp(-((yy - cy) ** 2 + (xx - cx) ** 2) / (2 * sigma**2))
    bg = img.mean() * bg  # controls background strength

    axes[0, i].imshow(bg)
    axes[0, i].set_title("Background")
    axes[0, i].axis("off")

    # --- Noise
    noisy = img + rng.normal(0, scale=2_000, size=img.shape)
    noisy = np.clip(noisy, 0, None)

    axes[1, i].imshow(noisy)
    axes[1, i].set_title("Noisy")
    axes[1, i].axis("off")

    # --- Sum
    tot = np.floor(norm(noisy + 2 * bg, img))

    axes[2, i].imshow(tot)
    axes[2, i].set_title("Sum")
    axes[2, i].axis("off")

    images.append(np.stack([tot, raw[i][1]]))
    print(images[-1].shape)

plt.tight_layout()

# %%
fig, axes = plt.subplots(
    len(images),
    3,
    figsize=(8, 22),
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

    axes[i, 2].hist(images[i][0].ravel(), bins=100, alpha=0.5)
    axes[i, 2].hist(images[i][1].ravel(), bins=100, alpha=0.5)
    axes[i, 2].set_title("Histogram")

# %%
plt.hist((noisy).ravel(), bins=40)

# %%
save_path = Path("../data/practical_project/noisy")
save_path.mkdir(parents=True, exist_ok=True)

for i, img in enumerate(images):
    imwrite(save_path / f"image_{i}.tif", img)

# %%
