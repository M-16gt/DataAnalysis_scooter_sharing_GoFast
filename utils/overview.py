from typing import Optional, Union
import pandas as pd


def print_shape_data(df: pd.DataFrame) -> None:
    """
    Выводит информацию о размере DataFrame.

    Функция печатает количество строк и столбцов в переданном DataFrame.

    Args:
        df (pd.DataFrame): DataFrame для анализа размерности.

    Returns:
        None: Функция только выводит информацию, не возвращает значение.

    Example:
        >>> import pandas as pd
        >>> data = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})
        >>> print_shape_data(data)
        Количество строк данных: 3
        Количество столбцов: 2
    """
    print("Количество строк данных: {}\nКоличество столбцов: {}".format(*df.shape))


def print_duplicates(
        df: pd.DataFrame,
        subset: Optional[Union[list[str], str]] = None,
        return_masked: Optional[bool] = True,
) -> Optional[pd.Series]:
    """
    Находит и выводит количество дубликатов в DataFrame.

    Может возвращать маску дубликатов для дальнейшего анализа.

    Args:
        df (pd.DataFrame): DataFrame для поиска дубликатов.
        subset (Optional[Union[list[str], str]]): Список столбцов или имя одного
            столбца для проверки дубликатов. Если None, проверяются все столбцы.
            По умолчанию None.
        return_masked (Optional[bool]): Если True, возвращает булеву серию с метками
            дубликатов. Если False, только выводит информацию. По умолчанию True.

    Returns:
        Optional[pd.Series]: Если return_masked=True, возвращает булеву серию,
        где True отмечает дубликаты. Если return_masked=False, возвращает None.

    Examples:
        >>> import pandas as pd
        >>> data = pd.DataFrame({'A': [1, 1, 2], 'B': ['a', 'a', 'b']})

        # Пример 1: Поиск полных дубликатов
        >>> mask = print_duplicates(data)
        Количество дубликатов: 1.

        # Пример 2: Поиск по одному столбцу
        >>> print_duplicates(data, subset='A')
        Количество дубликатов: 1.

        # Пример 3: Поиск по нескольким столбцам
        >>> print_duplicates(data, subset=['A', 'B'])
        Количество дубликатов: 1.

        # Пример 4: Только вывод информации
        >>> print_duplicates(data, return_masked=False)
        Количество дубликатов: 1.
    """
    duplicates = df.duplicated(subset=subset)

    print("Количество дубликатов: {}.".format(duplicates.sum()))

    if return_masked:
        return duplicates
    return None


def print_categorical_data(df: pd.DataFrame) -> None:
    """
    Анализирует и выводит информацию о категориальных столбцах DataFrame.

    Для каждого категориального (object) столбца показывает:
    - Название столбца
    - Количество уникальных значений
    - Топ-10 самых частых значений с их количеством

    Args:
        df (pd.DataFrame): DataFrame для анализа категориальных данных.

    Returns:
        None: Функция только выводит информацию, не возвращает значение.

    Note:
        1. Анализируются только столбцы с типом 'object' (строковые/категориальные данные)
        2. NaN-значения учитываются в подсчете уникальных значений
        3. Для каждого столбца выводится разделитель для лучшей читаемости

    Example:
        >>> import pandas as pd
        >>> data = pd.DataFrame({
        ...     'Имя': ['Анна', 'Борис', 'Анна', 'Мария'],
        ...     'Город': ['Москва', 'СПб', 'Москва', 'Казань'],
        ...     'Возраст': [25, 30, 25, 28]
        ... })
        >>> print_categorical_data(data)
        --------------------------------------------------
        Колонка: Имя
        - Уникальных значений: 3
        - Топ 10 по количество:
        Анна     2
        Борис    1
        Мария    1

        --------------------------------------------------
        Колонка: Город
        - Уникальных значений: 3
        - Топ 10 по количество:
        Москва    2
        СПб       1
        Казань    1
    """
    cat_cols = df.select_dtypes(include="object").columns

    for col in cat_cols:
        print("-" * 50)
        print(f"Колонка: {col}")
        print("- Уникальных значений:", df[col].nunique(dropna=False))
        print(f"- Топ 10 по количество:")
        print(df[col].value_counts(dropna=False).head(10))
        print()