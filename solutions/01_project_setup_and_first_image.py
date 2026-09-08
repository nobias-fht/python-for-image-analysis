# %% [markdown]
# # Module 1: virtual environments, Jupyter, and a first image
#
# Time: 1 hour.
#
# Essential idea: an analysis is easier to trust when the Python environment is
# explicit, isolated, and used consistently from the terminal, VSCode, and
# Jupyter. In this short module, students should leave with one working project
# and one tiny image-processing example.

# %% [markdown]
# ## Terminal setup with uv
#
# Run these commands in a terminal. The exact project name can change, but the
# logic should stay the same:
#
# ```bash
# uv init python-for-image-analysis
# # download scripts
# uv add numpy
# ```
#
# Useful mental model:
#
# - `uv` creates and updates the project environment.
# - VSCode should use `.venv/bin/python` from that project.
# - Jupyter runs a kernel; the kernel should point to the same environment.
#
# Common pitfall: installing a package in one environment and running the
# notebook with another kernel. When imports mysteriously fail, first check the
# Python executable and kernel name.
