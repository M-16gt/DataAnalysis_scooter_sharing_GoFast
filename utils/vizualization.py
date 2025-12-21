from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",  # Шрифт с поддержкой кириллицы
        "font.size": 12,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
    }
)

sns.set_style("whitegrid")
sns.set_context("paper")


def hist_boxplot(
    data: pd.DataFrame,
    columns: list[str],
    ncols: int = 2,
    hue: Optional[str] = None,
    kde: bool = False,
    save_path: Optional[Path] = None,
) -> None:

    plot_rows = len(columns)
    fig, axes = plt.subplots(
        nrows=plot_rows,
        ncols=ncols,
        figsize=(14, 5 * plot_rows),
        squeeze=False,
        constrained_layout=True,
    )

    for idx, col in enumerate(columns):
        sns.histplot(data=data, x=col, ax=axes[idx, 0], kde=kde, hue=hue)
        sns.boxplot(data=data, x=col, ax=axes[idx, 1], hue=hue)

        axes[idx, 0].set_xlabel(col)
        axes[idx, 1].set_xlabel(col)
        axes[idx, 0].set_ylabel("Количество")

    plt.suptitle("Гистограмма и ящик с усами количественных признаков")

    if save_path:
        plt.savefig(save_path)
    plt.show()
    plt.close(fig)


def scatterplot(
    data: pd.DataFrame,
    x: str,
    ys: list[str],
    hue: Optional[str] = None,
    ncols: int = 2,
    save_path: Optional[Path] = None,
) -> None:
    plot_rows = (int(np.ceil(len(ys) / ncols)))
    fig, axes = plt.subplots(
        plot_rows,
        ncols=ncols,
        figsize=(7 * ncols, 6 * plot_rows),
        squeeze=False,
        constrained_layout=True,
    )

    for idx, y in enumerate(ys):
        i, j = divmod(idx, ncols)
        ax = axes[i, j]

        sns.scatterplot(data=data, x=x, y=y, hue=hue, ax=ax)

        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title(f"Зависимость между {y} и {x}")

    for ax in axes.flat[len(ys) :]:
        ax.set_visible(False)

    plt.suptitle(f"Диаграммы рассеяния относительно признака '{x}'")

    if save_path:
        plt.savefig(save_path)
    plt.show()
    plt.close(fig)
