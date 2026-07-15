# Python for BioImage Analysis


## For students

## For instructors

### Set up

During development python scripts and notebooks in `solutions/` are kept in sync using [jupytext](https://jupytext.readthedocs.io/en/latest/). To ensure that the notebooks are correctly formatted and up to date, we use [pre-commit](https://pre-commit.com/) to run jupytext automatically. In addition, you should install the `jupytext` VSCode extension to maintain both ways synchronization between notebooks and scripts. Finally, the `exercises/` notebooks are generated
using pre-commit by stripping the exercise clause.


- Install the `jupytext` VSCode extension.
- Install pre-commit
    ```python
    uv run pre-commit install
    ```
- Modify the python scripts in `solutions/`. 


### Implementing the modules

Exercises should be marked with the following clause:
```python
# --- Exercise
<code>
# ---
```

Markdown cells are written in the following format:
```python
# %% [markdown]
# <some markdown>
#
```

Code cells as:
```python
# %%
```