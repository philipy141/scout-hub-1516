"""
Compute 0–100 percentiles for a player vs. peers in the **same role**.

Usage
-----
>>> from services.percentiles import role_percentiles, load_radar_config
>>> cfg = load_radar_config()                  # radar_config.yml
>>> pcts = role_percentiles(player_row, df_all, cfg)
"""
from __future__ import annotations
import yaml
from pathlib import Path
import pandas as pd

CONFIG_PATH = Path(__file__).parents[1] / "config" / "radar_config.yml"


# --------------------------------------------------------------------- #
# Helpers                                                               #
# --------------------------------------------------------------------- #
def load_radar_config(path: Path | str = CONFIG_PATH) -> dict:
    """Return YAML as dict{role: [metric, …]} (validated)."""
    with open(path, "r", encoding="utf-8") as f:
        cfg: dict = yaml.safe_load(f)

    # quick validation: at least one role & each role has ≥1 metric
    assert isinstance(cfg, dict) and cfg, "radar_config.yml is empty / invalid"
    for role, metrics in cfg.items():
        if not metrics:
            raise ValueError(f"Role '{role}' has no metrics defined")
    return cfg


def _within_role(df: pd.DataFrame, role: str) -> pd.DataFrame:
    """Subset peers that share player role (case insensitive)."""
    mask = df["role"].str.lower() == role.lower()
    peers = df[mask]
    if peers.empty:
        raise ValueError(f"No peers found for role '{role}'")
    return peers


def _percentile(col: pd.Series, value: float) -> float:
    """Return percentile (0–100) of *value* vs. col (handles NaNs)."""
    rank = (col < value).mean() * 100
    return round(rank, 1)  # one decimal is enough for UI


# --------------------------------------------------------------------- #
# Public API                                                             #
# --------------------------------------------------------------------- #
def role_percentiles(row: pd.Series, df: pd.DataFrame, cfg: dict) -> dict:
    role = row["role"]
    metrics = cfg.get(role, [])
    out = {}

    df_role = df[df["role"] == role]

    for col in metrics:
        values = df_role[col].dropna()
        min_val = values.min()
        max_val = values.max()

        val = row[col]

        if pd.isna(val) or max_val == min_val:
            out[col] = 0.0
        else:
            out[col] = round((val - min_val) / (max_val - min_val) * 100, 1)

    return out

