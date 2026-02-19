"""
plot_helpers.py
Small helpers for consistent matplotlib plots and saving figures.

Design goal:
- Keep styling light and portable
- Avoid hard-coded colors unless required
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt


@dataclass
class PlotConfig:
    figures_dir: str = "reports/figures"
    dpi: int = 160
    tight_layout: bool = True
    grid: bool = True
    grid_alpha: float = 0.35
    grid_linewidth: float = 0.3


def setup_matplotlib_defaults(font_size: int = 11):
    """
    Apply simple matplotlib defaults for readability.
    Keeps it minimal so charts look good in notebooks and exports.
    """
    plt.rcParams.update(
        {
            "figure.figsize": (10, 6),
            "axes.titlesize": font_size + 2,
            "axes.labelsize": font_size,
            "xtick.labelsize": font_size - 1,
            "ytick.labelsize": font_size - 1,
        }
    )


def apply_grid(ax: Optional[plt.Axes] = None, cfg: Optional[PlotConfig] = None):
    cfg = cfg or PlotConfig()
    ax = ax or plt.gca()
    if cfg.grid:
        ax.grid(True, which="both", linewidth=cfg.grid_linewidth, alpha=cfg.grid_alpha)


def save_figure(
    filename: str,
    cfg: Optional[PlotConfig] = None,
    subdir: Optional[str] = None,
    close: bool = True,
) -> str:
    """
    Saves the current matplotlib figure to reports/figures (or subdir).
    Returns absolute-ish path string.
    """
    cfg = cfg or PlotConfig()

    out_dir = Path(cfg.figures_dir)
    if subdir:
        out_dir = out_dir / subdir
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / filename

    if cfg.tight_layout:
        plt.tight_layout()

    plt.savefig(out_path, dpi=cfg.dpi)
    if close:
        plt.close()

    return str(out_path)


def new_figure(title: Optional[str] = None, cfg: Optional[PlotConfig] = None):
    """
    Creates a fresh figure and axis with optional title.
    """
    cfg = cfg or PlotConfig()
    fig, ax = plt.subplots()
    if title:
        ax.set_title(title)
    apply_grid(ax, cfg)
    return fig, ax
