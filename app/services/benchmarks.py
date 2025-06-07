# app/services/benchmarks.py
import pandas as pd
from typing import Dict

def role_benchmarks(
    player: pd.Series,
    population: pd.DataFrame,
    metrics: list[str],
    role_key: str = "radar_role"
) -> pd.DataFrame:
    """
    Returns a DataFrame with:
      metric        – metric name
      player_pct    – player's percentile (0–100)
      role_avg_pct  – average percentile across population
      quartile_flag – "top", "bottom", or "".
    """
    # 1) get each metric’s percentile for the population
    pops = population[metrics].rank(pct=True) * 100
    # 2) compute role-average percentile
    role_avg = pops.mean(axis=0)
    # 3) get the individual player percentiles
    player_vals = player[metrics]
    # we already have percentiles for the player via role_percentiles,
    # but if needed we can recompute here:
    player_pct = player_vals.rank(pct=True).reindex(metrics) * 100

    rows = []
    for m in metrics:
        p = float(player_pct[m])
        avg = float(role_avg[m])
        flag = ""
        if p >= 75:
            flag = "top"
        elif p <= 25:
            flag = "bottom"
        rows.append({"metric": m, "player_pct": p, "role_avg_pct": avg, "quartile": flag})
    return pd.DataFrame(rows)
