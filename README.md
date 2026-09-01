# Python for BioImage Analysis


## For students

## For instructors

### Set up

During development python scripts and notebooks in `solutions/` are kept in sync using [jupytext](https://jupytext.readthedocs.io/en/latest/). You should install the `jupytext` VSCode extension to maintain both ways synchronization between notebooks and scripts

- Install the `jupytext` VSCode extension.
- Install pre-commit
    ```python
    uv run pre-commit install
    ```
- Modify the python scripts in `solutions/`. 
- To create the notebook from the script you can run:
    ``` bash
    uv run jupytext solutions/05_image_analysis_with_skimage.py --sync
    ```
- Keep it out of git tracking, and let the VSCode extension sync the modification from ipynb to py

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


### HTML blocks in md cells

```markdown

### TODO in red
<div style="
  background: #fdecec;
  border-left: 6px solid #d64545;
  padding: 12px 16px;
  border-radius: 8px;
  margin: 12px 0;
  color: #7f1d1d;
">
  <strong style="color: #7f1d1d;">TODO</strong><br>
  A TODO (red)
  </div>

### Exercises in blue
<div style="
  background: #accffb;
  border-left: 6px solid #2f80ed;
  padding: 12px 16px;
  border-radius: 8px;
  margin: 12px 0;
  color: #21457f;
">
  <strong style="color: #21457f;">Exercise</strong><br>
  Exercises in blue
</div>

### Questions in green
<div style="
  background: #e8f7ec;
  border-left: 6px solid #2f9e44;
  padding: 12px 16px;
  border-radius: 8px;
  margin: 12px 0;
  color: #1f5f2c;
">
  <strong style="color: #1f5f2c;">Question</strong><br>
  Questions in green
</div>

### Optional exercises in gray
<div style="
  background: #f3f4f6;
  border-left: 6px solid #6b7280;
  padding: 12px 16px;
  border-radius: 8px;
  margin: 12px 0;
  color: #374151;
">
  <strong>Optional Exercise</strong><br>
  Optional exercises in gray
</div>

```


### Pushing new content

Please open a PR for new content, fixes, refactoring etc.

