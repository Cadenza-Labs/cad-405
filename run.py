import typer
import os
import itertools
from pathlib import Path
from rich import print
import subprocess

models = ["EleutherAI/gpt-j-6b", "gpt2-xl", "meta-llama/Llama-2-13b-hf"]
models = ["EleutherAI/gpt-j-6b"]
model_short = ["gj6", "gxl", "l13"]
model_short = ["gj6"]

model_to_shortcode = dict(zip(models, model_short))
datasets = ["imdb", "amazon_polarity"]

losses = [" --loss ccs_prompt_var", ""]
variant_nums = [2,4,8,-1]
variant_nums = [-1]
variants = [f" --num_variants {v}" for v in variant_nums]

combos = itertools.product(losses, models, datasets, variants)

def submit_jobs(outs_path):
    for loss, model, dataset, variant in combos:
        short_model = model_to_shortcode[model]
        short_ds = dataset[0]
        short_loss = "pv" if loss else ""
        command = f"elk elicit {model} {dataset}{loss}{variant} --net ccs --norm burns"
        preamble = f"""#!/bin/bash
#SBATCH --nodes=1
#SBATCH --gpus-per-node=2
#SBATCH --time=2-0
#SBATCH --partition=single
#SBATCH --job-name={short_loss}{short_model}{short_ds}"""
        script = f"""{preamble}

{command}
"""
        # get variant num from  --num_variants {v}
        v = variant[16:]

        # towrite = Path(f"sbatchs/{short_model}{short_ds}{short_loss}{v}.sbatch")
        # with open(towrite, "w") as f:
        #         f.write(script)

        # get cwd
        origin = Path.cwd()
        outs_path.mkdir(exist_ok=True, parents=True)
        os.chdir(outs_path)
        subprocess.run(["sbatch"], input=script, encoding="utf-8")
        os.chdir(origin)

import re
from pathlib import Path      
  
def get_all_sweep_paths(outs_path: Path):
    paths = []

    # get all files in this directory with slurm in the name
    files = list(outs_path.glob('slurm*.out'))
    print(f"len(files): {len(files)}")
    # Open the file and read each line
    for filename in files:
        file = open(filename, 'r')
        for line in file:
            # Use Regex to find the path
            # match = re.search(r'Saving results to (.*$)', line)
            match = re.search(r'Output directory at (.*$)', line)
            if match is not None:
                # if a match is found, convert the path string to pathlib object and add to list
                paths.append(Path(match.group(1)))

    # remove \x1b[1m and \x1b[0m from paths
    paths = [Path(str(p).replace("\x1b[1m", "").replace("\x1b[0m", "")) for p in paths]
    return paths



def copy_with_no_reporters(paths, write_dir_path):
    write_dir_path.mkdir(exist_ok=True, parents=True)
    for path in paths:
        for file in ['eval.csv', 'cfg.yaml']:
            new_path = write_dir_path / path.stem
            new_path.mkdir(exist_ok=True, parents=True)
            with open(new_path / file, "a+") as f:
                with open(path / file, "r") as f2:
                    f.write(f2.read())



if __name__ == "__main__":
    def main():
        outs_path = Path("./data/expt_2/outs")
        # submit_jobs(outs_path)
        processed_data_path = Path("./data/expt_2/no_reporters_expt_2")
        paths = get_all_sweep_paths(outs_path)
        copy_with_no_reporters(paths, processed_data_path)

    typer.run(main)
