# app/services/similarity.py
from __future__ import annotations
import time
from functools import lru_cache
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# Columns used for similarity
SIM_COLUMNS = [
    "progressive_passes_per90",
    "progressive_carries_per90",
    "xa_per90",
    "goals_per90",
    "shots_per90",
    "tackles_won_per90",
    "interceptions_per90",
    "pressures_successful_per90",
]

_CACHE: dict[str, np.ndarray] = {}   # stores matrix keyed by DF hash

def _normalise(df: pd.DataFrame) -> np.ndarray:
    scaler = MinMaxScaler()
    return scaler.fit_transform(df[SIM_COLUMNS])

def _key(df: pd.DataFrame) -> str:
    """Create a stable key from DF shape + checksum so cache invalidates
    if data changes."""
    return f"{len(df)}-{hash(tuple(df[SIM_COLUMNS].sum().round(6)))}"

@lru_cache(maxsize=4)
def _build_matrix(df_key: str, data: tuple) -> np.ndarray:
    """Internal helper wrapped by lru_cache to build / cache matrix."""
    X = np.vstack(data)              # restore ndarray from tuple
    return cosine_similarity(X)

def ensure_matrix(df: pd.DataFrame) -> np.ndarray:
    key = _key(df)
    if key not in _CACHE:            # first time for this DF
        X = _normalise(df)
        # store a lightweight tuple so the lru_cache remains hashable
        mat = _build_matrix(key, tuple(map(tuple, X)))
        _CACHE[key] = mat
    return _CACHE[key]

def get_similar(df: pd.DataFrame, player_id: int, n: int = 5) -> pd.DataFrame:
    current_row = df.loc[player_id]

    # --- NEW: Filter same role ---
    same_role_df = df[df["role"] == current_row["role"]].copy()
    
    # Drop non-numeric and ID columns for similarity calculation
    numeric_cols = same_role_df.select_dtypes(include="number").columns
    feature_cols = [col for col in numeric_cols if col not in ["player_id", "minutes", "age"]]
    
    # Normalize features (min-max)
    norm_df = same_role_df[feature_cols].copy()
    norm_df = (norm_df - norm_df.min()) / (norm_df.max() - norm_df.min())
    norm_df.fillna(0, inplace=True)

    # Vector for the selected player
    v1 = norm_df.loc[player_id].values.reshape(1, -1)
    
    # Cosine similarity to all others in same role
    from sklearn.metrics.pairwise import cosine_similarity
    sim_scores = cosine_similarity(v1, norm_df.values)[0]

    same_role_df = same_role_df.copy()
    same_role_df["similarity"] = sim_scores

    # Remove self
    same_role_df = same_role_df[same_role_df.index != player_id]

    # Sort and return top n
    top_similar = same_role_df.sort_values("similarity", ascending=False).head(n)

    return top_similar.reset_index()  # index carries player_id


