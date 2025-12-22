import pandas as pd
import scipy.stats as stats

def get_total_price_by_rule(df: pd.DataFrame, rule: str = "ME") -> pd.Series:
    df = df.copy()
    df.index = df["date"]

    df = df.resample(rule=rule).aggregate({
        'minute_price': 'max',
        'duration': 'sum',
        'start_ride_price': 'sum',
        'subscription_fee': 'sum'
    })

    df["total_price"] = df["minute_price"] * df["duration"] + df["start_ride_price"] + df["subscription_fee"]

    return df["total_price"]

def check_ttest_1samp(df: pd.DataFrame, popmean, alternative, text: str, _alpha: float = 0.05) -> None:
    # Сырая версия

    result = stats.ttest_1samp(df, popmean, alternative=alternative)

    if result.pvalue < _alpha:
        print("Отклоняем нулевую гипотезу о {}.".format(text))
    else:
        print("Нету причины отклонения нулевой гипотезы")