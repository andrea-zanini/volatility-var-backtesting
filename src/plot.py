import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from config import models

BASE_DIR = Path(__file__).resolve().parent.parent
cartella_plot = BASE_DIR / "results" / "plots"

def volatility_comparison(volatility_forecast: dict, asset: str, volatility_realized: pd.DataFrame):
    colors = {"garch": "#e63946", "ewma": "#457b9d", "rolling": "#2a9d8f"}
    for model in models:
        plt.figure(figsize = (12, 6))
        sns.set_theme(
        style = "ticks",
        palette = "muted",
        font = "serif",
        rc={
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.figsize": (12, 5),
            "axes.grid": True,
            "grid.alpha": 0.4
            })
        sns.despine()
        sns.lineplot(data = volatility_realized, x = "Date", y = asset, color = "black", linewidth = 1,
                     label = f'realized volatility of {asset}')
        sns.lineplot(data = volatility_forecast[model], x = "Date", y = asset, linewidth = 1.5, dashes = (5, 2),
                     color = colors[model], label = f'{model.upper()} of {asset}')
        plt.xlabel("Date")
        plt.ylabel("Volatility")
        plt.legend()
        plt.title("Volatility Comparison")
        plt.savefig(cartella_plot / f"volatility_comparison_{asset}_{model}.png", dpi = 150, bbox_inches = "tight")
        plt.close()

def time_error(realized_error: dict, asset: str):
    colors = {"garch": "#e63946", "ewma": "#457b9d", "rolling": "#2a9d8f"}
    for model in models:
        plt.figure(figsize = (12, 6))
        sns.set_theme(
        style = "ticks",
        palette = "muted",
        font = "serif",
        rc={
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.figsize": (12, 5),
            "axes.grid": True,
            "grid.alpha": 0.4
            })
        sns.despine()
        sns.lineplot(data = realized_error[model], x = "Date", y = asset, color = colors[model])
        plt.xlabel("Date")
        plt.ylabel("Volatility")
        plt.title("Error through the time")
        plt.savefig(cartella_plot / f"error_{asset}_{model}.png", dpi = 150, bbox_inches = "tight")
        plt.close()

def violation_plot(hit: dict, asset: str):
    colors = {"garch": "#e63946", "ewma": "#457b9d", "rolling": "#2a9d8f"}
    for model in models:
        plt.figure(figsize = (12, 6))
        sns.set_theme(
        style = "ticks",
        palette = "muted",
        font = "serif",
        rc={
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.figsize": (12, 5),
            "axes.grid": True,
            "grid.alpha": 0.4
            })
        sns.despine()
        sns.lineplot(data = hit[model], x = "Date", y = asset, marker = "o",
                     color = colors[model], linewidth = 0.5, dashes = (5, 2))
        plt.xlabel("Date")
        plt.ylabel("Violation")
        plt.title("Violation through the time")
        plt.savefig(cartella_plot / f"violation_{asset}_{model}.png", dpi = 150, bbox_inches = "tight")
        plt.close()