from pathlib import Path
import yaml
import os
import pandas as pd
import matplotlib.pyplot as plt

def updated_plot_with_cfg(sweep_path: Path) -> plt.Figure:
    """
    Plots the Layer vs. AUROC Estimate for a given filename, focusing on entries where prompt_ensembling is 'partial'.
    Extracts model information from the cfg.yaml in the same directory.
    
    Args:
    - filename (str): Path to the eval.csv file
    
    Returns:
    - Figure: Matplotlib figure object
    """
    # Load the data
    df = pd.read_csv(sweep_path / 'eval.csv')
    
    # Filter for prompt_ensembling=partial
    partial_df = df[df['prompt_ensembling'] == 'partial']
    
    # Extract dataset name from the DataFrame
    dataset = partial_df['dataset'].iloc[0]
    
    # Extracting model name from the cfg.yaml in the same directory
    cfg_path = sweep_path / 'cfg.yaml'
    with open(cfg_path, 'r') as cfg_file:
        cfg = yaml.safe_load(cfg_file)
        model = cfg['data']['model']
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(partial_df['layer'], partial_df['auroc_estimate'], marker='o', linestyle='-')
    ax.set_xlabel('Layer')
    ax.set_ylabel('AUROC Estimate')
    ax.set_title(f"model: {model}, dataset: {dataset}, ensembling=partial")
    ax.grid(True)
    plt.tight_layout()
    
    return fig

# Plot for all 4 files using the updated function
expt_folder = Path("./data/expt_2/")
reporters_path = expt_folder / "no_reporters_expt_2"
sweep_paths = list(reporters_path.iterdir())
figures_with_cfg = [updated_plot_with_cfg(sweep_path) for sweep_path in sweep_paths]


fig, axs = plt.subplots(2, 2, figsize=(20, 12))
axs = axs.flatten()
for i, sweep_path in enumerate(sweep_paths):
    # Load the data
    df = pd.read_csv(sweep_path / 'eval.csv')
    
    # Filter for prompt_ensembling=partial
    partial_df = df[df['prompt_ensembling'] == 'partial']
    
    # Extract dataset name from the DataFrame
    dataset = partial_df['dataset'].iloc[0]
    
    # Extracting model name from the cfg.yaml in the same directory
    cfg_path = sweep_path / 'cfg.yaml'
    with open(cfg_path, 'r') as cfg_file:
        cfg = yaml.safe_load(cfg_file)
        model = cfg['data']['model']
        loss = cfg['net']['loss']
    
    # Plot
    axs[i].plot(partial_df['layer'], partial_df['auroc_estimate'], marker='o', linestyle='-')
    axs[i].set_xlabel('Layer')
    axs[i].set_ylabel('AUROC Estimate')
    axs[i].set_title(f"model: {model}, dataset: {dataset}, loss={loss}, ens=partial")
    axs[i].grid(True)

plt.tight_layout()
plt.savefig(expt_folder / 'plots.png')