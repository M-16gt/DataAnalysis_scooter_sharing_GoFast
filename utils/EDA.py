import pandas as pd
import scipy.stats as stats


def get_total_price_by_rule(df: pd.DataFrame, rule: str = "ME") -> pd.Series:
    """
    Агрегирует данные о поездках за указанный период и вычисляет общую выручку.

    Функция выполняет ресемплинг исходного DataFrame по дате, агрегирует ключевые
    показатели (цена за минуту, длительность и т.д.) и рассчитывает итоговую выручку
    для каждого периода.

    Args:
        df (pd.DataFrame): Исходный DataFrame, содержащий данные о поездках.
            Обязательные колонки: 'date' (в формате datetime), 'minute_price',
            'duration', 'start_ride_price', 'user_id', 'subscription_fee'.
        rule (str, optional): Правило ресемплинга для агрегации по времени.
            Используется стандартные строки Pandas (например, 'ME' для месяца,
            'W' для недели, 'D' для дня). По умолчанию 'ME' (конец месяца).

    Returns:
        pd.Series: Серия, индексированная датой (периодом агрегации), содержащая
        общую выручку за каждый период.

    Formula:
        total_price = (max(minute_price) * sum(duration)) +
                      sum(start_ride_price) +
                      (max(subscription_fee) * nunique(user_id))

    Example:
        >>> monthly_revenue = get_total_price_by_rule(trips_df, rule='ME')
        >>> weekly_revenue = get_total_price_by_rule(trips_df, rule='W')
    """
    df = df.copy()
    df.index = df["date"]

    df = df.resample(rule=rule).aggregate(
        {
            "minute_price": "max",
            "duration": "sum",
            "start_ride_price": "sum",
            "user_id": "nunique",  # NOQA
            "subscription_fee": "max",
        }
    )

    df["total_price"] = (
        df["minute_price"] * df["duration"]
        + df["start_ride_price"]
        + df["subscription_fee"] * df["user_id"]
    )

    return df["total_price"]


def check_ttest_1samp(
    df: pd.DataFrame, popmean: float, alternative: str, _alpha: float = 0.05
) -> None:
    """
    Выполняет одновыборочный t-тест Стьюдента и выводит интерпретацию результата.

    Тест проверяет гипотезу о равенстве математического ожидания (среднего)
    выборки заданному значению `popmean`.

    Args:
        df (pd.DataFrame): Входные данные (выборка). Должна быть числовая колонка.
        popmean (float): Предполагаемое среднее значение генеральной совокупности
            (математическое ожидание) согласно нулевой гипотезе (H0).
        alternative (str): Формулировка альтернативной гипотезы (H1).
            Допустимые значения: 'two-sided' (двусторонняя), 'less' (меньше),
            'greater' (больше).
        _alpha (float, optional): Уровень значимости для принятия решения.
            По умолчанию 0.05.

    Returns:
        None: Функция выводит результат в консоль.

    Prints:
        T-statistic: Значение t-статистики.
        P-value: Значение p-value.
        Решение: "Отклоняем нулевую гипотезу." или "Нет оснований отклонить нулевую гипотезу."

    Note:
        Нулевая гипотеза (H0): среднее выборки равно `popmean`.
        Решение принимается сравнением p-value с уровнем значимости `_alpha`.
    """
    result = stats.ttest_1samp(df, popmean, alternative=alternative)

    print("T-statistic: {}".format(result.statistic))
    print("P-value: {}".format(result.pvalue))

    if result.pvalue < _alpha:
        print("Отклоняем нулевую гипотезу.")
    else:
        print("Нет оснований отклонить нулевую гипотезу.")


def check_ttest_ind(
    df1: pd.DataFrame, df2: pd.DataFrame, alternative: str, _alpha: float = 0.05
) -> None:
    """
    Выполняет двухвыборочный t-тест Стьюдента для независимых выборок и выводит результат.

    Тест проверяет гипотезу о равенстве математических ожиданий (средних) двух
    независимых выборок. Используется модификация Уэлча (не предполагает равенства
    дисперсий, `equal_var=False`).

    Args:
        df1 (pd.DataFrame): Данные первой независимой выборки (числовая колонка).
        df2 (pd.DataFrame): Данные второй независимой выборки (числовая колонка).
        alternative (str): Формулировка альтернативной гипотезы (H1).
            Допустимые значения: 'two-sided' (средние не равны), 'less' (среднее df1
            меньше среднего df2), 'greater' (среднее df1 больше среднего df2).
        _alpha (float, optional): Уровень значимости для принятия решения.
            По умолчанию 0.05.

    Returns:
        None: Функция выводит результат в консоль.

    Prints:
        T-statistic: Значение t-статистики.
        P-value: Значение p-value.
        Решение: "Отклоняем нулевую гипотезу." или "Нет оснований отклонить нулевую гипотезу."

    Note:
        Нулевая гипотеза (H0): средние двух выборок равны.
        Решение принимается сравнением p-value с уровнем значимости `_alpha`.
        Используется критерий Уэлча, который надежнее при неравных дисперсиях и
        размерах выборок.
    """
    result = stats.ttest_ind(df1, df2, alternative=alternative, equal_var=False)
    print("T-statistic: {}".format(result.statistic))
    print("P-value: {}".format(result.pvalue))

    if result.pvalue < _alpha:
        print("Отклоняем нулевую гипотезу.")
    else:
        print("Нет оснований отклонить нулевую гипотезу.")