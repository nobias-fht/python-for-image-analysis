# %% [markdown]
# # Module 1: Project setup with `uv`
#
# Time: 1 hour (45 minutes + 15 minutes troubleshooting).
#
# Image analysis relies on Python libraries for tasks such as reading images, working with arrays, and measuring objects. These libraries are our **dependencies**. Their versions matter: an update can change how code runs or how results are calculated.
#
# In this module, we will:
#
# - Create a project environment and add packages with `uv`.
# - Run a notebook in VS Code and fix a missing dependency.
# - Use a lockfile to help reproduce an analysis environment.
# - Compare project dependencies with script and notebook dependencies.
#
# ## 1 - Initialize the project
#
# Open the course folder in VS Code, then choose **Terminal → New Terminal**. Run the shell commands in this module in that terminal, from the `python-for-image-analysis` directory. Use `pwd` to check your location.
#
# You can read this notebook before selecting a kernel. We will set up the kernel before running any Python cells.

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
# Initialize the project by running in the terminal:
#
# ```bash
# uv init
# ```
#
# </div>
#
# You will see that two new files have been created:
#
# - `pyproject.toml`: holds the project's metadata, including dependencies.
# - `main.py`: a small script added by `uv`.

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
# What project name and Python version requirement appear in your `pyproject.toml`? What is in its dependency list so far?
#
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
# If you do not already have a project directory, you can run:
#
# ```bash
# uv init <project name>
# ```
#
# and `uv` will create the project directory for you.
#
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
# Run the starter script:
#
# ```bash
# uv run main.py
# ```
#
# </div>

# %% [markdown]
# The console output should look something like this:
#
# ```console
# Using CPython 3.13.3 interpreter at: /opt/homebrew/opt/python@3.13/bin/python3.13
# Creating virtual environment at: .venv
# Installed 1 package in 51ms
# Hello from python-for-image-analysis!
# ```
#
# The Python version, path, and installation details may differ on your computer.
# Notice the line `Creating virtual environment at: .venv`: running the script
# created the project's environment in the `.venv` directory.
#
# You can now delete the generated `main.py` in the VS Code file explorer; we will work in notebooks.

# %% [markdown]
# ## 2 - Environments and packages
#
# A **virtual environment** holds a project's Python interpreter and installed packages. Keeping a separate environment for each project lets different analyses use different library versions.
#
# When you use the `uv run` command it automatically first locks the dependencies and then syncs the environment.
# You can also do this manually with the commands:
#
# - `uv lock`: resolves all the dependencies into a lock file (this created a `uv.lock` file, which we will discuss shortly).
# - `uv sync`: updates (or creates) the current environment.
#
# You can find more information about these commands in the [uv command reference](https://docs.astral.sh/uv/reference/cli/).
#
# VS Code should be able to detect our new environment to run our notebook cells.
#
# ### Add Jupyter and select a kernel
#
# To be able to run a notebook with the environment we need to install `jupyter`.

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
# Run the command:
#
# ```bash
# uv add jupyter
# ```
#
# </div>
#
# In the top right of the notebook you should see a "Select Kernel" button; use this to select the `python-for-image-analysis` Python environment.
#
# ![Select Kernel](../assets/select_kernel.png)

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
# Look at `pyproject.toml` again. What changed after `uv add jupyter`?
#
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
# Print a message in the cell below. Click its play button or press **Shift+Enter** to run it.
#
# <details>
# <summary>
# <strong>Hint</strong>
# </summary>
#
# Use the `print` function.
# </details>
# </div>

# %%
# --- Exercise
print("Hello from Python for image analysis!")
# ---

# %% [markdown]
# ### The `add` command
#
# When calling `uv add`, `uv` will update `pyproject.toml` and `uv.lock`, and then install the package into the environment. We need to have packages installed in the python environment to be able to use them.
#
# In the next module we will use the library [NumPy](https://numpy.org/install/), so let's try to import it here.
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
#   When you run the next cell, what do you think will happen?
# </div>

# %%
import numpy as np

print("NumPy version:", np.__version__)

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
#   Take action to fix the error above and re-run the cell.
#
#   <details>
#   <summary>
#   <strong>Hint</strong>
#   </summary>
#
#   We need to add `numpy` to the `project`.
#   </details>
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
#   You will need to check on each package's website or PyPI what the install name is. Most of the time it will be intuitive but it is better to check than installing something unknown onto your machine. There is a cyber attack often called "typosquatting", where bad actors will release malicious software under the name of a mistyped popular package.
# </div>

# %% [markdown]
# ## 3 - Lockfiles and reproducibility
#
# The three parts of our setup serve different purposes:
#
# | Item | Purpose |
# | --- | --- |
# | `pyproject.toml` | Declares the project's direct dependencies and allowed version ranges. |
# | `uv.lock` | Records resolved package versions, including dependencies of our dependencies. |
# | `.venv/` | Contains the locally installed environment used to run the code. |
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
#   Do not commit the environment `.venv/` into the versioning system (git) because it will become very heavy!
# </div>
#
#
# A requirement such as `numpy>=2.0` in the `pyproject.toml` allows several versions, if someone is using your project as a library this allows some flexibility. However, it does not guarantee that future versions of NumPy will actually be compatible with your code. Libraries require constant active maintainence to ensure they are compatible with the dependencies they declare.
#
# A lockfile records the exact versions present in the environment when the lockfile was created.
# This is great for analysis workflows, it is a record of the dependencies that worked last time the analysis was run.
# If there a versions that depend on a particular machine, (e.g. Mac, Linux or Windows) it will record all of the available equivalent versions.
#
# ### Recreate the environment
#
# To later recreate the environment, say on another computer, we can do
#
# ```bash
# uv sync
# ```
#
# This creates or updates `.venv` from the lockfile. If the project requirements have changed, `uv sync` may update the lockfile too. To require an up-to-date lockfile without allowing changes to it, use:
#
# ```bash
# uv sync --locked
# ```
#
# This reports an error if the lockfile is missing or no longer matches the project requirements. `uv run` also checks the lockfile and environment automatically before running a command.
#
# See the [uv locking and syncing guide](https://docs.astral.sh/uv/concepts/projects/sync/) for details.

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
# Open `uv.lock` and find the NumPy entry. Compare its exact version with the requirement in `pyproject.toml` and the version printed by the notebook.
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
#   In the lock file there are many more packages listed than in the `pyproject.toml`, what are these other packages?
# </div>

# %% [markdown]
# ### Why this matters for image analysis
#
# Imagine rerunning a cell-counting analysis six months later. A library update might change a segmentation default, fix a numerical calculation, or remove a function. Reusing the locked dependencies reduces the chance that an unplanned software update changes your results.
#
# A lockfile is one part of reproducibility. Also keep the input images, analysis code, parameter values, Python version, and any random seeds. Hardware and operating-system differences may still affect results.

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
# A colleague receives your notebook and `pyproject.toml`, but no lockfile. Why might they install different package versions? Could a lockfile alone reproduce your cell counts without the original images and analysis settings?
#
# </div>

# %% [markdown]
# ## 4 - Project dependencies or a script header?
#
# For this course, several notebooks share the same packages, so we keep dependencies together in `pyproject.toml` and use one project environment.
#
# For a standalone `.py` script, `uv` can instead read dependencies from a specially formatted header comment. For example, a separate `array_demo.py` could contain:
#
# <div style="
#   background-color: var(--vscode-textCodeBlock-background, rgba(127,127,127,0.12));
#   color: var(--vscode-editor-foreground, inherit);
#   border: 1px solid var(--vscode-editorWidget-border, #888);
#   padding: 12px;
#   border-radius: 6px;
#   font-family: var(--vscode-editor-font-family, monospace);
# ">
#
# ```python
# # /// script
# # requires-python = ">=3.11"
# # dependencies = ["numpy"]
# # ///
#
# import numpy as np
#
# print(np.arange(3))
# ```
# </div>
#
# These comments tell `uv` what the script needs. Python itself treats them as ordinary comments. Run it with:
#
# ```bash
# uv run array_demo.py
# ```
#
# `uv` uses an isolated environment for the script's declared dependencies, independently of the project's dependencies. You can add a dependency to that header with `uv add --script array_demo.py numpy`.
#
# The header is a dependency declaration, not a lockfile. To record resolved versions for the script, run `uv lock --script array_demo.py`; this creates `array_demo.py.lock` alongside it.
#
# See the [uv script guide](https://docs.astral.sh/uv/guides/scripts/).

# %% [markdown]
# ## 5 - `juv` for standalone notebooks
#
# [`juv`](https://github.com/manzt/juv) brings a similar approach to Jupyter notebooks: dependencies travel with the notebook, and `juv` uses `uv` to prepare an environment when launching it. It can also store a dependency lockfile in the notebook's metadata.
#
# This is useful for sharing an individual notebook. Our course uses the shared `pyproject.toml` environment in VS Code; `juv` is an alternative workflow to try separately.

# %% [markdown]
# <div style="
#   background: #f3f4f6;
#   border-left: 6px solid #6b7280;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #374151;
# ">
#   <strong style="color: #374151;">Optional Exercise</strong><br>
#
# In a separate practice folder, try:
#
# ```bash
# uvx juv init demo.ipynb
# uvx juv add demo.ipynb numpy
# uvx juv lock demo.ipynb
# uvx juv run demo.ipynb
# ```
#
# `uvx` runs the `juv` tool without adding it to the course project's dependencies. The last command launches JupyterLab with an environment prepared for this notebook.
#
# In `demo.ipynb`, run `import numpy as np` and then `print(np.arange(3))`. Compare this workflow with selecting the course project's `.venv` kernel in VS Code. Stop the Jupyter server with **Ctrl+C** in its terminal when finished.
#
# </div>
