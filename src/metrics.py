import numpy as np

KEYS = ['station', 'model', 'lead_days']


def temp_metrics(df):
    d = df.dropna(subset=['t_obs', 't_fc']).copy()
    d['err'] = d['t_fc'] - d['t_obs']
    g = d.groupby(KEYS)['err']
    out = g.agg(n='size', bias='mean',
                mae=lambda s: s.abs().mean(),
                rmse=lambda s: np.sqrt((s ** 2).mean()))
    return out.reset_index()


def daily_precip(df):
    d = df.dropna(subset=['p_obs', 'p_fc']).copy()
    d['day'] = d['time'].dt.floor('D')
    g = d.groupby(KEYS + ['day']).agg(p_obs=('p_obs', 'sum'), p_fc=('p_fc', 'sum'), hours=('p_obs', 'size'))
    g = g.reset_index()
    return g[g['hours'] == 24]


def precip_scores(daily, threshold=1.0):
    d = daily.copy()
    o = d['p_obs'] >= threshold
    f = d['p_fc'] >= threshold
    d['hit'] = (o & f).astype(int)
    d['miss'] = (o & ~f).astype(int)
    d['fa'] = (~o & f).astype(int)
    s = d.groupby(KEYS)[['hit', 'miss', 'fa']].sum().reset_index()
    s['pod'] = s['hit'] / (s['hit'] + s['miss']).replace(0, np.nan)
    s['far'] = s['fa'] / (s['hit'] + s['fa']).replace(0, np.nan)
    return s