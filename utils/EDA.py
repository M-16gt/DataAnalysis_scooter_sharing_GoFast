import pandas as pd
import scipy.stats as stats

def get_total_price_by_rule(df: pd.DataFrame, rule: str = "ME") -> pd.Series:
    df = df.copy()
    df.index = df["date"]

    df = df.resample(rule=rule).aggregate({
        'minute_price': 'max',
        'duration': 'sum',
        'start_ride_price': 'sum',
        'user_id': 'nunique', # NOQA
        'subscription_fee': 'max'
    })

    df["total_price"] = df["minute_price"] * df["duration"] + df["start_ride_price"] + df["subscription_fee"] * df["user_id"]

    return df["total_price"]

def check_ttest_1samp(df: pd.DataFrame, popmean, alternative, _alpha: float = 0.05) -> None: # NOQA

    result = stats.ttest_1samp(df, popmean, alternative=alternative)

    print("T-statistic: {}".format(result.statistic))
    print("P-value: {}".format(result.pvalue))

    if result.pvalue < _alpha:
        print("Отклоняем нулевую гипотезу.")
    else:
        print("Нету причины отклонения нулевой гипотезы.")

def check_ttest_ind(df1: pd.DataFrame, df2: pd.DataFrame, alternative,  _alpha: float = 0.05) -> None: # NOQA
    result = stats.ttest_ind(df1, df2, alternative=alternative, equal_var=False)
    print("T-statistic: {}".format(result.statistic))
    print("P-value: {}".format(result.pvalue))

    if result.pvalue < _alpha:
        print("Отклоняем нулевую гипотезу.")
    else:
        print("Нету причины отклонения нулевой гипотезы.")