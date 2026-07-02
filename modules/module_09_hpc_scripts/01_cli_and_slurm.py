# %% [markdown]
# # Module 9: running scripts on the HPC
#
# Essential ideas: batch jobs should be reproducible, parameterized, and able to
# run without manual notebook interaction.

# %%
import argparse
from pathlib import Path

import pandas as pd
from skimage import io, measure

from course_utils import make_blobs

# %% [markdown]
# ## Command-line arguments
#
# In a normal script, the user can run:
#
# ```bash
# uv run python analyze_image.py --seed 12 --output results.csv
# ```

# %%


def analyze_synthetic_image(seed: int) -> pd.DataFrame:
    image = make_blobs(seed=seed)
    labels = measure.label(image > 0.35)
    table = measure.regionprops_table(
        labels,
        intensity_image=image,
        properties=("label", "area", "mean_intensity"),
    )
    return pd.DataFrame(table)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze a synthetic image.")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output", type=Path, default=Path("scratch_outputs/hpc_results.csv"))
    parser.add_argument("--save-image", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    results = analyze_synthetic_image(seed=args.seed)
    results.to_csv(args.output, index=False)
    if args.save_image is not None:
        args.save_image.parent.mkdir(parents=True, exist_ok=True)
        io.imsave(args.save_image, make_blobs(seed=args.seed))
    print(f"Wrote {len(results)} objects to {args.output}")


# %%
main(["--seed", "3", "--output", "scratch_outputs/module09_demo.csv"])

# %% [markdown]
# ## Slurm example
#
# Save as `submit_analysis.sbatch`:
#
# ```bash
# #!/bin/bash
# #SBATCH --job-name=image-analysis
# #SBATCH --time=00:10:00
# #SBATCH --cpus-per-task=1
# #SBATCH --mem=2G
# #SBATCH --array=0-9
#
# set -euo pipefail
#
# module load python/3.12
# cd /path/to/project
# uv sync
#
# uv run python analyze_image.py \
#   --seed "${SLURM_ARRAY_TASK_ID}" \
#   --output "results/result_${SLURM_ARRAY_TASK_ID}.csv"
# ```
#
# Keep the command, environment, code version, and parameters together.

# %% [markdown]
# ## Optional exercises
#
# 1. Add a `--threshold` argument.
# 2. Change the output filename to include the seed.

# %%
# Answer sketch (optional, removable)
# parser.add_argument("--threshold", type=float, default=0.35)
# output = Path(f"results/result_seed_{args.seed}.csv")
