# %% [markdown]
# # Module 1: Project setup with `uv`
#
# Time: 1 hour (45 minutes + 15 minutes troubleshooting).
#
# When working on scientific applications of python we will often rely on 3rd party open-source libraries which can be used through python's import system. Because of this python has a thriving open-source scientific ecosystem, however it comes with the added complication of managing dependencies and their versions. New versions of libraries are not always compatible with old code, or new versions of a second library that you might need for you project.
#
# In this module we will learn about the tool `uv` that will allow us to manage our dependencies effectively and keep our code reproducible in the future.
#
# ### Question
#
# What is the best way to manage dependencies and ensure that code remains reproducible?
#
# ### Objective
#
# - Learn how to manage dependecies with `uv`.
# - Learn what is a lock file and why is it important.

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
