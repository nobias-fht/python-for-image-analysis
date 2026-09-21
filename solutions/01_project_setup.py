# %% [markdown]
# # Module 1: Project setup with `uv`
#
# Time: 1 hour (45 minutes + 15 minutes troubleshooting).
#
# When working on scientific applications of python we will often rely on 3rd party open-source libraries which can be used through python's import system. Because of this python has a thriving open-source scientific ecosystem, however it comes with the added complication of managing dependencies and their versions. New versions of libraries are not always compatible with old code, or other libraries your project depends on.
#
# In this module we will learn about the tool `uv` that will allow us to manage our dependencies effectively and keep our code reproducible in the future.
#
# <div style="display: flex; align-items: center; gap: 12px;">
#     <img src="https://docs.astral.sh/uv/assets/logo-letter.svg" alt="Logo" style="height: 40px; width: auto;">
#     uv
# </div>
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
# ## Introduction to `uv`
#
# You can use a terminal with VS Code by selecting from the toolbar **Terminal -> New Terminal**.
#
# In your teminal, make sure you are in the `python-for-image-analysis` directory, try printing the working directory with the `pwd` command.
#
# <!-- Useful mental model:
#
# - `uv` creates and updates the project environment.
# - VSCode should use `.venv/bin/python` from that project.
# - Jupyter runs a kernel; the kernel should point to the same environment.
#
# Common pitfall: installing a package in one environment and running the
# notebook with another kernel. When imports mysteriously fail, first check the
# Python executable and kernel name. -->

# %% [markdown]
# ### Initialize python project
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
#   Initialize the project by running in the terminal:
#
#   ```bash
#   uv init
#   ```
# </div>
#
# You will see that two new files have been created:
#
# - `pyproject.toml`
#   - This holds all of the projects metadata including dependencies.
# - `main.py`
#   - A small script added by `uv`

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
#
#   Take a look inside the `pyproject.toml` file, what sort of metadata is stored there so far?
# </div>
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
#   If you do not already have a project directory, you can run:
#
#   ```bash
#   uv init <project name>
#   ```
#   and `uv` will create the project directory for you.
#
# </div>

# %% [markdown]
# We will delete the `main.py` file, but before we do, try running it with the `uv run` command.
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
#   Run the `main.py` script with:
#
#   ```bash
#   uv run main.py
#   ```
# </div>

# %% [markdown]
# The console output should look something like the following
#
# ```console
# Using CPython 3.13.3 interpreter at: /opt/homebrew/opt/python@3.13/bin/python3.13
# Creating virtual environment at: .venv
# Installed 1 package in 51ms
# Hello from python-for-image-analysis!
# ```
#
# Notice it created a virtual environment in the project directory under the `.env` file.
# When you use the `uv run` command it automatically first runs `uv lock` followed by `uv sync`:
# - `uv lock`: resolves all the dependencies into a lock file (this created a `uv.lock` file, which we will discuss shortly.)
# - `uv sync`: updates (or creates) the current environment.
#
# VS Code should now be able to find the environment, in the top right of the notebook you should see a "Select Kernel" button, use this to select the `python-for-image-analysis` python environment.
#
# ![Select Kernel](../assets/select_kernel.png)

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
#   To be able to run a notebook with the environment we need to install `jupyter`.
#
#   Run the command:
#
#   ```bash
#   uv add jupyter
#   ```
# </div>
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
#   Look inside the `pyproject.toml` file, what has changed?
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
#   <strong style="color: #21457f;">Exercise</strong><br>
#
#   Print a message in the cell below to confirm that the environment is set-up to run the notebook.
#
#   <details>
#   <summary><strong>Hint</strong></summary>
#
#   Use the `print` function.
#   </details>
# </div>

# %%
# --- Exercise
print("Hello python for image analysis course!")
# ---

# %%
