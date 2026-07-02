# %% [markdown]
# # Module 10: organizing code for publication
#
# Essential ideas: make the project understandable to future readers, citeable,
# runnable, and legally reusable.

# %% [markdown]
# ## Minimal package layout
#
# ```text
# image-analysis-project/
#   README.md
#   LICENSE
#   pyproject.toml
#   CITATION.cff
#   src/
#     image_analysis_project/
#       __init__.py
#       io.py
#       segmentation.py
#       measurements.py
#       cli.py
#   tests/
#     test_segmentation.py
#   scripts/
#     run_pipeline.py
#   docs/
#     workflow.md
# ```

# %% [markdown]
# ## pyproject sketch
#
# ```toml
# [project]
# name = "image-analysis-project"
# version = "0.1.0"
# description = "Reproducible image analysis workflow for ..."
# requires-python = ">=3.11"
# dependencies = ["numpy", "pandas", "scikit-image", "scipy", "matplotlib"]
#
# [project.scripts]
# analyze-images = "image_analysis_project.cli:main"
# ```

# %% [markdown]
# ## Release checklist
#
# - Choose a license before making the repository public.
# - Add a README with installation, example data, and expected output.
# - Include small tests for core functions.
# - Keep raw data out of git if files are large or sensitive.
# - Tag releases and archive them with Zenodo or an institutional repository.
# - Add `CITATION.cff` so others know how to cite the work.
# - Prefer open platforms when possible: GitHub, GitLab, or Codeberg.

# %%
from pathlib import Path

layout_paths = [
    "README.md",
    "LICENSE",
    "pyproject.toml",
    "CITATION.cff",
    "src/image_analysis_project/__init__.py",
    "src/image_analysis_project/segmentation.py",
    "tests/test_segmentation.py",
]

for path in layout_paths:
    print(Path(path))

# %% [markdown]
# ## Optional exercises
#
# 1. Draft a one-paragraph README summary for a pipeline project.
# 2. Pick a license and explain why it fits the intended sharing model.

# %%
# Answer sketch (optional, removable)
readme_summary = (
    "This project segments fluorescent cell images, measures object intensity "
    "and shape, and exports reproducible per-cell tables for downstream analysis."
)
license_choice = "MIT or BSD-3-Clause for permissive reuse; GPL if derivatives must remain open."
print(readme_summary)
print(license_choice)
