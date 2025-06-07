import sys
import os
import pandas as pd

# Ensure the path points to the actual project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.components.player_grid import _format_df, VISIBLE_COLS

def test_format_df_returns_expected_columns():
    df = pd.DataFrame({
        "player": ["A"],
        "team": ["B"],
        "minutes_played": [1234],
        "junk": [0],
    })
    out = _format_df(df)
    assert list(out.columns) == ["Name", "Team", "Minutes"]
