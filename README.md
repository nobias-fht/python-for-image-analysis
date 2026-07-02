# Python for Image Analysis

Draft scaffold for a 3.5-day Python image analysis course for young life scientists.

The scripts are written as notebook-style Python files with `# %% [markdown]` and `# %%` cells, so they can later be converted to notebooks with tools such as Jupytext or opened directly in VSCode.

## Audience

Participants should already know:

- basic Python: values, types, variables, functions
- basic image analysis concepts: multidimensional images, bit depth, background subtraction

## Course Aim

By the end of the course, participants should be able to build small, reproducible Python image analysis workflows: load or simulate images, inspect and visualize data, segment objects, measure features, organize results in tables, and turn a prototype into modular code that can run on a workstation or HPC.

## Suggested Environment

This draft assumes a local Python project managed with `uv`.

```bash
uv init python-for-image-analysis
uv add numpy scipy pandas matplotlib scikit-image jupyter ipykernel
uv add --optional napari "napari[all]"
uv run python -m ipykernel install --user --name python-image-analysis
uv run jupyter lab
```

Optional readers for real microscopy formats can be introduced later. The course
currently uses BioIO-style examples for vendor formats:

```bash
uv add tifffile zarr ome-zarr bioio bioio-ome-tiff bioio-ome-zarr bioio-lif bioio-nd2 bioio-czi
```

Vendor-format readers often have extra system or Java requirements, so the course examples avoid depending on them.

## Module Index

| Module | Time | Aim | Draft file |
| --- | ---: | --- | --- |
| 1. Virtual env + Jupyter | 1h | Create an isolated project environment and verify the scientific Python stack. | `modules/module_01_virtual_env_jupyter/01_project_setup_and_first_image.py` |
| 2. Working with bio-images | 1h45 | Treat images as arrays: axes, dtype, slicing, masks, and vectorized arithmetic. | `modules/module_02_working_with_bio_images/01_arrays_dtypes_and_vectorization.py` |
| 3. Opening formats | 1h | Understand common microscopy formats, metadata questions, and safe toy I/O. | `modules/module_03_opening_bio_images/01_formats_and_metadata.py` |
| 4. Visualization | 1h | Make inspection plots and overlays without hiding analysis assumptions. | `modules/module_04_visualizing_images/01_matplotlib_and_napari.py` |
| 5. Operations | 2h30 | Build the core segmentation path: filtering, thresholding, morphology, watershed, measurement. | `modules/module_05_image_analysis_operations/01_operations_segmentation_measurement.py` |
| 6. Pipeline practical | 2h | Combine segmentation, measurement, quality checks, and a simple biological question. | `modules/module_06_pipeline_practical/01_two_channel_pipeline.py` |
| 7. Data analysis | 1h45 | Summarize measurement tables, plot results, and fit a simple model. | `modules/module_07_data_analysis_visualization/01_tables_plots_and_fits.py` |
| 8. Modular Python | 2h30 | Refactor a notebook-style workflow into functions, settings, and a small pipeline class. | `modules/module_08_modular_python/01_modular_pipeline.py` |
| 9. HPC scripts | 1h | Turn an analysis into a parameterized command-line script suitable for batch jobs. | `modules/module_09_hpc_scripts/01_cli_and_slurm.py` |
| 10. Publication organization | 1h30 | Organize a reusable project with metadata, tests, licensing, and citation information. | `modules/module_10_publication_code/01_publication_ready_layout.py` |

## Conversion Note

These scripts are intentionally compact. They are not complete lecture notes. During notebook conversion, each `# %% [markdown]` block can become a short explanation cell and each `# %%` block can become a runnable example or exercise cell.

Convert the module scripts into notebooks with:

```bash
python scripts/convert_notebooks.py
```

By default, notebooks are written to `notebooks/` while preserving the module directory structure.
