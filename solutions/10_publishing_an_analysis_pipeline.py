# %% [markdown]
# # Module 10: organizing code for publication
#
# Time: 1 hour 30 minutes.
#
# If you ever tried using code from GitHub, then you probably ran into any of
# the following issues:
# - No instruction for installing the package
# - No example script to reproduce the published results
# - No example data to explore how the package work
# - No user documentation on how to use the various features
# - No code documentation helping to understand the package design
# - Package depends on unmaintained packages or non-compatible packages
# - No license, so you don't know how to legally use it
# - etc.
#
# ```markdown
# image-analysis-scripts/
# ├── analyze_new2.py
# ├── analyze_new3.py
# ├── cell2.py
# ├── crop_final.py
# ├── data.py
# ├── debug.py
# ├── draft.ipynb
# ├── img2.py
# ├── process_all.py
# └── weird_thresholds.csv
# ```
#
# It does not matter if the code is not perfect, as (publicly-funded) researchers, it is
# our duty to the public and fellow scientists to produce reproducible results. It is much
# easier to set up code to be reproduced than bench experiments. In this module, we will
# go through a list of checkmarks to help you be a leading practitioner of FAIRness in
# scientific code.
#
#
# <div style="
#   background: #f3f4f6;
#   border-left: 6px solid #6b7280;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #374151;
# ">
#   <strong>What's FAIRness?</strong><br>
#   Findability, Accessibility, Interoperability, and Reusability (FAIR) principles have
#   been adapted for [data](https://www.nature.com/articles/sdata201618) and is directly
#   applicable to code:
#   - Findability: it is released on the internet
#   - Accessibility: it can be viewed and downloaded by anyone
#   - Interoperability: it is compatible with the relevant existing software/analysis
#   - Reusability: it can be installed by anyone easily
# </div>
#

# %% [markdown]
# ## 1 - When to turn analysis code into a package
#
# A package is useful when:
#
# - Several scripts reuse the same functions
# - Collaborators need to install the code
# - The pipeline will be run on new datasets
# - A paper or preprint needs a stable, citable version.
#
# A single script may be enough when the analysis is small, one-off, and fully
# documented. Do not package code only for appearance.

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
#   Let's say you have a collection of scripts for a publication, what would be your pre-publicationFAIR
#   checkbox list?
# </div>

# %% [markdown]
# \# --- Exercise
#
# <input type="checkbox" checked> Code is on GitHub <br/>
# <input type="checkbox"> Example data has been released online <br/>
# <input type="checkbox"> License file <br/>
# <input type="checkbox"> Links to pre-print and data (README.md) <br/>
# <input type="checkbox"> Installation instructions (README.md) <br/>
# <input type="checkbox"> User documentation (README.md) <br/>
# <input type="checkbox"> Lock file for environment<br/>
#
# \# ---

# %% [markdown]
# <div style="
#   background: #fdecec;
#   border-left: 6px solid #d64545;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #7f1d1d;
# ">
#   <strong style="color: #7f1d1d;">Warning</strong><br>
#   Avoid putting binary files (images, data, word documents, pdfs, etc.) in a git repo, especially if they are heavy.
# </div>
#

# %% [markdown]
# ## 2 - Minimal package layout
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
#   What are the ingredients of a good package? Can you comment on the various files in the following tree? What are their use?
# </div>

# %% [markdown]
#
#
# ```markdown
# image-analysis-package/
# ├── LICENSE
# ├── pyproject.toml
# ├── README.md
# ├── uv.lock
# ├── .python-version
# ├── docs/
# │   └──  image_analysis_package/
# │       └── ... (*.md)
# ├── src/
# │   └── image_analysis_package/
# │       ├── __init__.py
# │       └── ... (*.py)
# └── tests/
#     ├── __init__.py
#     └── ... (*.py)
# ```

# %% [markdown]
# <div style="
#   background: #f3f4f6;
#   border-left: 6px solid #6b7280;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #374151;
# ">
#   <strong>pyproject.toml</strong><br>
#   This configuration file holds metadata for packaging (who are the authors, where is the source code, etc.),
#   but also instructions for building the package (dependencies, optional dependencies, developer tools configuration, etc.). More
#   on the specifications on the <a href="https://packaging.python.org/en/latest/guides/writing-pyproject-toml/">Python documentation</a>.
# </div>

# %% [markdown]
# ## 3 - Choosing a license
#
# Choose a license before sharing code publicly.
#
# - MIT or BSD-3-Clause: permissive reuse.
# - GPL: derivatives must remain open under compatible terms.
# - Apache-2.0: permissive reuse with explicit patent language.
#
# Add `CITATION.cff` so users and citation tools know how to cite the code.
# Archive releases with Zenodo (which gives you a DOI, can be cited if you don't have
# a publication).
#
# <div style="
#   background: #f3f4f6;
#   border-left: 6px solid #6b7280;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #374151;
# ">
#   <strong>More on licenses</strong><br>
#    Have a quick look at <a href="https://choosealicense.com/">this website</a>.
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
#   Data should have licenses as well! Open licenses are usually CC-0 and CC-BY for fully
#   open and modifyiable data.
# </div>
#

# %% [markdown]
# ## 4 - README contents
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
# <div style="
#   background: #fff8db;
#   border-left: 6px solid #e2b200;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #8a6a00;
# ">
#   <strong style="color: #8a6a00;">Note</strong><br>
#   A README that says "run the notebook" is not enough, provide the full command-line
#   instructions.
# </div>

# %% [markdown]
# ## 5 - Documentation
#
# Documentation can refer to two things:
# - API or usage of the code
# - Docstring: documentation of the code itself
#

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
#   What needs documenting in this function? How would you do it?
# </div>


# %%
def remove_background(img, func, params):
    bg = func(**params)
    res = img - bg
    return res, bg


# %%
from typing import Any, Callable
from numpy.typing import NDArray


def remove_background(
    img: NDArray, func: Callable, params: dict[str, Any]
) -> tuple[NDArray, NDArray]:
    """Remove background by computing the background from `img` and subtracting it.

    Parameters
    ----------
    img : numpy.ndarray
        Image from which to remove background.
    func : Callable
        Background estimation function.
    params : dict[str, Any]
        Parameters to be passed to `func`.

    Returns
    -------
    numpy.ndarray
        Background-free image
    numpy.ndarray
        Estimated background removed from the image.
    """
    bg = func(**params)
    res = img - bg
    return res, bg


# %% [markdown]
# ## 6 - Code reproducibility
#
# Keep enough information to understand how results were produced:
#
# - use git!
# - code version or git commit used for the results
# - lock file (remember `uv`?)
# - parameter/configuration file for running scripts
# - if possible, tag the commits used to create results (see [git tags](https://git-scm.com/book/en/v2/Git-Basics-Tagging))
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
#   Try to run the following code multiple times, what do you observe?
#
#   Then pass a number to `default_rng()`.
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
#   What is the name of the parameter we passed?
# </div>

# %%
import numpy as np

# -- Exercise
rng = np.random.default_rng(42)
# ---

# Here are some experimental results
results = np.asarray([0.1, 4.5, 6.1, 2.1, 0.5, 6.3, 4.2, 6.2, 9.1, 0.8, 4.2, 2.7])

# Estimate the uncertainty of the results mean by bootstrapping the results randomly
bootstrap_means = np.array(
    [rng.choice(results, size=len(results), replace=True).mean() for _ in range(20)]
)

mean = results.mean()
bootstrap_se = bootstrap_means.std(ddof=1)
ci_95 = np.percentile(bootstrap_means, [2.5, 97.5])

print("Mean:", mean)
print("Bootstrap standard error:", bootstrap_se)
print("Approximate 95% CI:", ci_95)

# %% [markdown]
# ## 7 - Advanced package features
#
# Here are some advanced software engineering features worth mentining to improve code
# quality, reproducibility and maintainability.
#
#
# - Tests are a suite of small functions that validate that each piece of software does
# exactly what was intended. They are used to catch bugs and change of behaviours.
# - Continuous Integration (CI) is the automation of the tests to continuously run them
# against the latest changes.
# - Continuous Deployment (CD) is the automation of the package release.

# %% [markdown]
# ## 8 - A small release checklist
#
# Use a checklist before making a repository public or submitting a manuscript:
#
#
# <input type="checkbox" checked> Code is on GitHub (or alternatives)<br/>
# <input type="checkbox" checked> Code has a (open-source) license <br/>
# <input type="checkbox" checked> (Optional, if applicable) Code is packageable <br/>
# <input type="checkbox" checked> README contains clear install and run instructions <br/>
# <input type="checkbox" checked> Dependencies are declared in `pyproject.toml` <br/>
# <input type="checkbox" checked> A lockfile is provided <br/>
# <input type="checkbox" checked> Example data has been released (e.g. Zenodo or BioImage Archive) <br/>
# <input type="checkbox" checked> Example code runs on the example data <br/>
# <input type="checkbox" checked> Reproducibility (and deterministic) scripts are provided <br/>
# <input type="checkbox" checked> Core functionalities and output generation are not mixed <br/>
# <input type="checkbox" checked> A release tag is created for the submitted pre-print/paper <br/>
# <input type="checkbox" checked> Citation instructions are present <br/>
#
# <div style="
#   background: #fdecec;
#   border-left: 6px solid #d64545;
#   padding: 12px 16px;
#   border-radius: 8px;
#   margin: 12px 0;
#   color: #7f1d1d;
# ">
#   <strong style="color: #7f1d1d;">Critical</strong><br>
#   Don't underestimate how important and time-intensive data release is. You need to document
#   scientifically and accurately how the data was acquired, (pre-)processed and analyzed. You need
#   to describe the type, image size, bit depth, channel names, axes organization of the raw
#   data.
#
#   Your future self and colleagues will thank you.
#   </div>
#

# %% [markdown]
#
