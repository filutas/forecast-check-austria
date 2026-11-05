import math
import pandas as pd
import pytest
from src.metrics import temp_metrics, daily_precip, precip_scores


def test_temp_metrics_hand_calculated():
    df = pd.DataFrame({'station': ['a'] * 3, 'model': ['m'] * 3, 'lead_days': [1] * 3,
                       't_obs': [10.0, 10.0, 10.0], 't_fc': [11.0, 9.0, 13.0]})
    r = temp_metrics(df).iloc[0]
    assert r['bias'] == pytest.approx(1.0)
    assert r['mae'] == pytest.approx(5 / 3)
    assert r['rmse'] == pytest.approx(math.sqrt(11 / 3))


def test_temp_metrics_ignores_missing():
    df = pd.DataFrame({'station': ['a'] * 3, 'model': ['m'] * 3, 'lead_days': [1] * 3,
                       't_obs': [10.0, None, 10.0], 't_fc': [12.0, 20.0, 8.0]})
    r = temp_metrics(df).iloc[0]
    assert r['n'] == 2
    assert r['bias'] == pytest.approx(0.0)


def test_daily_precip_requires_24_hours():
    times = pd.date_range('2025-01-01', periods=30, freq='h', tz='UTC')
    df = pd.DataFrame({'station': 'a', 'model': 'm', 'lead_days': 1, 'time': times,
                       'p_obs': 1.0, 'p_fc': 0.5})
    d = daily_precip(df)
    assert len(d) == 1
    assert d.iloc[0]['p_obs'] == pytest.approx(24.0)
    assert d.iloc[0]['p_fc'] == pytest.approx(12.0)


def test_precip_scores_counts():
    daily = pd.DataFrame({'station': ['a'] * 4, 'model': ['m'] * 4, 'lead_days': [1] * 4,
                          'p_obs': [5.0, 5.0, 0.0, 0.0], 'p_fc': [4.0, 0.0, 3.0, 0.0]})
    s = precip_scores(daily).iloc[0]
    assert (s['hit'], s['miss'], s['fa']) == (1, 1, 1)
    assert s['pod'] == pytest.approx(0.5)
    assert s['far'] == pytest.approx(0.5)