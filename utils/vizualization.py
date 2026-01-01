from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Глобальные настройки стиля для matplotlib
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

# Настройка стиля seaborn
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
    """
    Создает комбинированные графики: гистограмму и boxplot для указанных числовых колонок.

    Для каждой колонки создается два графика в одном ряду:
    слева - гистограмма с опциональным KDE, справа - ящик с усами.

    Args:
        data (pd.DataFrame): DataFrame с данными для визуализации.
        columns (list[str]): Список имен числовых колонок для анализа.
        ncols (int, optional): Количество колонок в макете графиков. Всегда 2 (гистограмма + boxplot).
            По умолчанию 2.
        hue (Optional[str], optional): Имя категориальной колонки для разделения данных по цвету.
            По умолчанию None.
        kde (bool, optional): Если True, добавляет кривую плотности распределения (KDE) к гистограмме.
            По умолчанию False.
        save_path (Optional[Path], optional): Путь для сохранения графика. Если None, график только отображается.
            По умолчанию None.

    Returns:
        None: Функция отображает графики через plt.show() и не возвращает значения.

    Examples:
        >>> # Анализ распределения возраста и дохода
        >>> hist_boxplot(df, columns=['age', 'income'], kde=True)
        >>>
        >>> # Анализ с разделением по полу и сохранением в файл
        >>> hist_boxplot(df, columns=['height', 'weight'], hue='gender',
        ...              save_path=Path('distributions.png'))
    """
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
    """
    Создает сетку диаграмм рассеяния для анализа зависимости переменных от базового признака.

    Для каждой переменной в списке ys создается отдельный scatterplot с общим признаком x на оси X.

    Args:
        data (pd.DataFrame): DataFrame с данными для визуализации.
        x (str): Имя признака для оси X (общий для всех графиков).
        ys (list[str]): Список имен признаков для оси Y (каждый будет в отдельном графике).
        hue (Optional[str], optional): Имя категориальной колонки для разделения данных по цвету.
            По умолчанию None.
        ncols (int, optional): Количество колонок в сетке графиков. По умолчанию 2.
        save_path (Optional[Path], optional): Путь для сохранения графика. Если None, график только отображается.
            По умолчанию None.

    Returns:
        None: Функция отображает графики через plt.show() и не возвращает значения.

    Examples:
        >>> # Анализ зависимости нескольких переменных от возраста
        >>> scatterplot(df, x='age', ys=['income', 'height', 'weight'], ncols=2)
        >>>
        >>> # Анализ с разделением по городу и сохранением результата
        >>> scatterplot(df, x='temperature', ys=['sales', 'revenue'],
        ...             hue='city', save_path=Path('scatter_analysis.png'))
    """
    plot_rows = int(np.ceil(len(ys) / ncols))
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

    for ax in axes.flat[len(ys):]:
        ax.set_visible(False)

    plt.suptitle(f"Диаграммы рассеяния относительно признака '{x}'")

    if save_path:
        plt.savefig(save_path)
    plt.show()
    plt.close(fig)