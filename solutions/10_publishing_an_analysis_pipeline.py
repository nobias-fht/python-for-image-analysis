# %% [markdown]
# # Module 10: organizing code for publication
#
# Time: 1 hour 30 minutes.
#
# Essential ideas: publication-ready code is understandable, runnable, citeable,
# legally reusable, and connected to the data and results it produced. It does
# not need to be perfect software, but it should let a future reader reproduce
# the analysis without guessing.

# %% [markdown]
# ## When to turn analysis code into a package
#
# A package is useful when:
#
# - several scripts reuse the same functions,
# - collaborators need to install the code,
# - the pipeline will be run on new datasets,
# - tests should import core functions,
# - a paper or preprint needs a stable, citable version.
#
# A single script may be enough when the analysis is small, one-off, and fully
# documented. Do not package code only for appearance; package it when it lowers
# future friction.

# %% [markdown]
# ## Minimal package layout
#
# ```text
# image-analysis-project/
#   README.md
#   LICENSE
#   pyproject.toml
#   CITATION.cff
#   CHANGELOG.md
#   .gitignore
#   src/
#     image_analysis_project/
#       __init__.py
#       io.py
#       segmentation.py
#       measurements.py
#       visualization.py
#       cli.py
#   tests/
#     test_segmentation.py
#     test_measurements.py
#   scripts/
#     run_pipeline.py
#   notebooks/
#     exploratory_analysis.ipynb
#   docs/
#     workflow.md
#   data/
#     README.md
# ```
#
# Pitfall: do not commit large raw microscopy datasets into git. Use a data
# repository, institutional storage, OMERO, BioImage Archive, Zenodo, or another
# system appropriate for the project.

# %% [markdown]
# ## pyproject sketch
#
# ```toml
# [project]
# name = "image-analysis-project"
# version = "0.1.0"
# description = "Reproducible image analysis workflow for ..."
# readme = "README.md"
# requires-python = ">=3.11"
# license = { text = "BSD-3-Clause" }
# authors = [{ name = "Your Name" }]
# dependencies = [
#   "numpy",
#   "pandas",
#   "scikit-image",
#   "scipy",
#   "matplotlib",
# ]
#
# [project.optional-dependencies]
# dev = ["pytest", "ruff"]
# notebooks = ["jupyter", "ipykernel"]
#
# [project.scripts]
# analyze-images = "image_analysis_project.cli:main"
# ```
#
# When to use optional dependencies: put heavy viewers, notebook tools, or
# format-specific readers in extras when not every user needs them.

# %% [markdown]
# ## README contents
#
# A useful README answers:
#
# - What biological or technical problem does this solve?
# - What inputs are expected?
# - What outputs are produced?
# - How do I install the environment?
# - How do I run a minimal example?
# - What parameters matter?
# - Where are example data or test data?
# - How should the code be cited?
#
# Pitfall: a README that only says "run the notebook" is not enough for a
# reproducible workflow.

# %% [markdown]
# ## Licensing and citation
#
# Choose a license before sharing code publicly.
#
# - MIT or BSD-3-Clause: permissive reuse.
# - GPL: derivatives must remain open under compatible terms.
# - Apache-2.0: permissive reuse with explicit patent language.
#
# Add `CITATION.cff` so users and citation tools know how to cite the code.
# Archive releases with Zenodo or an institutional repository when the code
# supports a publication.

# %% [markdown]
# ## Tests and continuous integration
#
# Tests should cover the small functions that carry the analysis logic:
#
# - segmentation returns labels with the expected shape,
# - empty images fail clearly or return empty results,
# - measurement tables contain required columns,
# - CLI parsing accepts documented arguments,
# - a tiny example pipeline runs end to end.
#
# Continuous integration can run tests automatically on GitHub, GitLab, or other
# platforms. Start small: one test file and one workflow is already useful.

# %% [markdown]
# ## Documentation and provenance
#
# Keep enough information to understand how results were produced:
#
# - code version or git commit,
# - package versions or lock file,
# - raw data location and checksum when possible,
# - parameter file,
# - command used to run the analysis,
# - output directory and date,
# - known limitations and QC decisions.
#
# When to use a parameter file: when a command has many options or when the same
# pipeline is run across experiments with different settings.

# %% [markdown]
# ## Repository hosting and release choices
#
# GitHub, GitLab, and Codeberg can all host public code. The important parts are
# not the platform logo, but whether the repository has:
#
# - issue tracking or a contact route,
# - releases or tags,
# - a license,
# - clear installation instructions,
# - archived versions for published results,
# - documentation for data access.

# %%
from pathlib import Path

layout_paths = [
    "README.md",
    "LICENSE",
    "pyproject.toml",
    "CITATION.cff",
    "CHANGELOG.md",
    "src/image_analysis_project/__init__.py",
    "src/image_analysis_project/segmentation.py",
    "src/image_analysis_project/measurements.py",
    "tests/test_segmentation.py",
    "tests/test_measurements.py",
    "scripts/run_pipeline.py",
    "docs/workflow.md",
    "data/README.md",
]

for path in layout_paths:
    print(Path(path))

# %% [markdown]
# ## A small release checklist
#
# Use a checklist before making a repository public or submitting a manuscript:
#
# - The repository has a license.
# - The README contains install and run instructions.
# - Dependencies are declared in `pyproject.toml` or equivalent.
# - Example data or a clear data-access note exists.
# - The analysis can run from a clean environment.
# - Generated outputs are not mixed with source code.
# - Core functions have at least small tests.
# - Large data and private data are not committed.
# - A release tag is created for the submitted version.
# - Citation instructions are present.

# %%
release_checklist = {
    "license": True,
    "readme_install": True,
    "declared_dependencies": True,
    "example_or_data_note": False,
    "tests": False,
    "citation": True,
}

missing = [name for name, ok in release_checklist.items() if not ok]
print("Missing before release:", missing)

# %% [markdown]
# ## Optional exercises
#
# 1. Draft a one-paragraph README summary for the two-channel pipeline.
# 2. Choose a license and explain the tradeoff in one sentence.
# 3. Write three tests you would add first.
# 4. Draft a `CITATION.cff` entry with title, authors, version, and date.
# 5. Write a short data availability note for raw microscopy files that cannot
#    be committed to git.

# %%
# Answer sketch (optional, removable)
readme_summary = (
    "This project segments two-channel fluorescence microscopy images, measures "
    "per-object intensity ratio and shape, classifies objects into two "
    "populations, and exports reproducible measurement tables for downstream "
    "analysis."
)
license_choice = (
    "BSD-3-Clause: permissive reuse while keeping attribution requirements clear."
)
first_tests = [
    "segment_instances returns a label image with the same YX shape as input",
    "measure_objects returns label, area, ratio, and ellipticity columns",
    "the CLI writes a CSV for a tiny synthetic input",
]
citation_cff = {
    "cff-version": "1.2.0",
    "title": "Two-channel microscopy image analysis pipeline",
    "authors": [{"family-names": "Scientist", "given-names": "Ada"}],
    "version": "0.1.0",
    "date-released": "2026-07-02",
}
data_note = (
    "Raw microscopy files are stored in the institutional data repository under "
    "accession XYZ. A small synthetic example is included for testing."
)

print(readme_summary)
print(license_choice)
print(first_tests)
print(citation_cff)
print(data_note)
