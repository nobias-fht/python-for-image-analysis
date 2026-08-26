# %% [markdown]
# # Module 9: running scripts on the HPC
#
# Time: 1 hour.
#
# Essential ideas: batch jobs should be reproducible, parameterized, and able to
# run without manual notebook interaction. A script for the HPC should make
# inputs, outputs, parameters, and environment assumptions explicit.

# %%
import argparse
from pathlib import Path

import pandas as pd
from skimage import io, measure

from src.python_for_ia import make_blobs

# %% [markdown]
# ## From notebook to command-line script
#
# In a normal script, the user can run:
#
# ```bash
# uv run python analyze_image.py --seed 12 --threshold 0.35 --output results.csv
# ```
#
# When to use: any analysis that must be repeated across many images, seeds,
# positions, wells, or parameter sets.
#
# Pitfall: a script that silently writes outputs into the current directory is
# hard to debug on an HPC. Always print or log where outputs go.

# %%


def analyze_synthetic_image(seed: int, threshold: float) -> pd.DataFrame:
    image = make_blobs(seed=seed)
    labels = measure.label(image > threshold)
    table = measure.regionprops_table(
        labels,
        intensity_image=image,
        properties=("label", "area", "mean_intensity"),
    )
    df = pd.DataFrame(table)
    df["seed"] = seed
    df["threshold"] = threshold
    return df


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze a synthetic image.")
    parser.add_argument(
        "--seed", type=int, default=0, help="Random seed used to simulate the image."
    )
    parser.add_argument(
        "--threshold", type=float, default=0.35, help="Foreground threshold."
    )
    parser.add_argument(
        "--output", type=Path, default=Path("scratch_outputs/hpc_results.csv")
    )
    parser.add_argument("--save-image", type=Path, default=None)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned work without writing files.",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(f"seed={args.seed} threshold={args.threshold} output={args.output}")

    if args.dry_run:
        print("Dry run: no files written.")
        return

    args.output.parent.mkdir(parents=True, exist_ok=True)
    results = analyze_synthetic_image(seed=args.seed, threshold=args.threshold)
    results.to_csv(args.output, index=False)

    if args.save_image is not None:
        args.save_image.parent.mkdir(parents=True, exist_ok=True)
        io.imsave(args.save_image, make_blobs(seed=args.seed))

    print(f"Wrote {len(results)} objects to {args.output}")


# %%
main(
    [
        "--seed",
        "3",
        "--threshold",
        "0.35",
        "--output",
        "scratch_outputs/module09_demo.csv",
    ]
)
main(["--seed", "3", "--dry-run"])

# %% [markdown]
# ## Slurm example
#
# Save as `submit_analysis.sbatch`:
#
# ```bash
# !/bin/bash
# #SBATCH --job-name=image-analysis
# #SBATCH --time=00:10:00
# #SBATCH --cpus-per-task=1
# #SBATCH --mem=2G
# #SBATCH --array=0-9
# #SBATCH --output=logs/%x_%A_%a.out
# #SBATCH --error=logs/%x_%A_%a.err
#
# set -euo pipefail
#
# module load python/3.12
# cd /path/to/project
# uv sync
#
# mkdir -p results logs
#
# uv run python analyze_image.py \
#   --seed "${SLURM_ARRAY_TASK_ID}" \
#   --threshold 0.35 \
#   --output "results/result_${SLURM_ARRAY_TASK_ID}.csv"
# ```
#
# Keep the command, environment, code version, and parameters together.

# %% [markdown]
# ## HPC habits that prevent pain
#
# - Test on one tiny input before submitting an array job.
# - Print input and output paths at the start of the script.
# - Write one output per job, then merge later.
# - Avoid writing many jobs to the same file.
# - Use relative paths from the project root or explicit absolute paths.
# - Keep raw data read-only.
# - Record package versions, git commit, and parameters.

# %% [markdown]
# ## Optional exercises
#
# 1. Add a `--min-area` argument and remove objects below that area.
# 2. Change the output filename to include the seed and threshold.
# 3. Write a Slurm array command for seeds 20 to 29.
# 4. Add a `--input` argument that would point to a real image file later.
# 5. Explain why each array job should write a separate output file.

# %%
# Answer sketch (optional, removable)
# parser.add_argument("--min-area", type=float, default=0)
# df = df[df["area"] >= args.min_area]
seed = 4
threshold = 0.35
output = Path(f"results/result_seed_{seed}_threshold_{threshold:.2f}.csv")
print(output)
print("#SBATCH --array=20-29")
print(
    "Separate output files avoid write conflicts and make failed jobs easier to rerun."
)
