import pandas as pd
from app.services.similarity import (
    get_similar,
    ensure_matrix,
    SIM_COLUMNS,
)
from app.components.player_detail import render_detail
from app.services.percentiles import role_percentiles
import streamlit as st
from app.components.similar_panel import render_similar

# ───────────────────────── Mock radar config ────────────────────────────
RADAR_CFG = {"Striker": ["goals_per90", "shots_per90"]}

# Minimal mock data-frame for percentile tests
DF_MOCK = (
    pd.DataFrame(
        [
            # highest goals_per90 (0.9) / highest shots_per90 (3.0)
            {"player": "A", "team": "X", "role": "Striker", "goals_per90": 0.9, "shots_per90": 3.0},
            # lowest goals_per90 (0.6) / lowest shots_per90 (1.0)
            {"player": "B", "team": "X", "role": "Striker", "goals_per90": 0.6, "shots_per90": 1.0},
            # middle values
            {"player": "C", "team": "Y", "role": "Striker", "goals_per90": 0.7, "shots_per90": 2.0},
        ]
    )
    .set_index(pd.Index([0, 1, 2], name="player_id"))
)


# ─────────────────────── helpers ────────────────────────────────────────
def mock_df() -> pd.DataFrame:
    """10-row dummy frame containing every SIM column so similarity code works."""
    data = {c: range(10) for c in SIM_COLUMNS}
    data["player"] = [f"Player {i}" for i in range(10)]
    data["team"] = ["Team"] * 10
    return pd.DataFrame(data).set_index(pd.Index(range(10), name="player_id"))


# ─────────────────────── similarity tests ───────────────────────────────
def test_matrix_build_once():
    df = mock_df()
    mat1 = ensure_matrix(df)
    mat2 = ensure_matrix(df)  # should be fetched from cache
    assert mat1 is mat2


def test_get_similar_topn():
    df = mock_df()
    res = get_similar(df, player_id=5, n=3)
    assert len(res) == 3
    # Row 5 should be most-similar (cosine sim == 1)
    assert res.iloc[0]["similarity"] == 1.0


# ─────────────────────── render-detail tests ────────────────────────────
def test_render_detail_valid_row():
    # need at least n+1 rows (n=5 in get_similar) so provide 6
    rows = 6
    dummy = {
        "player": [f"Test{i}" for i in range(rows)],
        "team": ["Foo"] * rows,
        "minutes_played": [90] * rows,
        "percentiles": [{}] * rows,
        **{col: [1] * rows for col in SIM_COLUMNS},
    }
    df = pd.DataFrame(dummy)
    df.index = pd.Index(range(rows), name="player_id")
    s = df.iloc[0]
    # Should not raise
    render_detail(s, df)


# ─────────────────────── percentile sanity tests ────────────────────────
def test_highest_value_is_max():
    row = DF_MOCK.loc[0]  # A (highest goals_per90)
    pcts = role_percentiles(row, DF_MOCK, cfg=RADAR_CFG)
    assert pcts["goals_per90"] == max(pcts.values())


def test_lowest_value_is_min():
    row = DF_MOCK.loc[1]  # B (lowest shots_per90)
    pcts = role_percentiles(row, DF_MOCK, cfg=RADAR_CFG)
    assert pcts["shots_per90"] == min(pcts.values())

