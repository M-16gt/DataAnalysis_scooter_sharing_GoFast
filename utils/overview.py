from typing import Optional, Union

import pandas as pd


def print_shape_data(df: pd.DataFrame) -> None:
    print("Количество строк данных: {}\nКоличество столбцов: {}".format(*df.shape))


def print_duplicates(
    df: pd.DataFrame, subset: Optional[Union[list[str], str]] = None
) -> pd.Series:
    duplicates = df.duplicated(subset=subset)

    print("Количество дубликатов: {}.".format(duplicates.sum()))

    return duplicates


def print_categorical_data(df: pd.DataFrame) -> None:
    cat_cols = df.select_dtypes(include="object").columns

    for col in cat_cols:
        print("-" * 50)
        print(f"Колонка: {col}")
        print("- Уникальных значений:", df[col].nunique(dropna=False))
        print(f"- Топ 10 по количество:")
        print(df[col].value_counts(dropna=False).head(10))
        print()
