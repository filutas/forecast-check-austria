from src.forecasts import fetch_forecasts

LAT, LON = 48.24861, 16.35639
for m in ['ecmwf_ifs025', 'gfs_seamless', 'icon_seamless']:
    try:
        x = fetch_forecasts('5904', LAT, LON, m, '2025-01-01', '2025-03-31')
        print(m, 'rows', len(x), '| missing t_fc', int(x['t_fc'].isna().sum()), '| missing p_fc', int(x['p_fc'].isna().sum()))
    except Exception as err:
        print(m, 'FAILED:', err)