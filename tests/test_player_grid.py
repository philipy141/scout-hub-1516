import pandas as pd
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
