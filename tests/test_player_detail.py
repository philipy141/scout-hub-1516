import pandas as pd
from app.components.player_detail import render_detail

def test_render_detail_no_crash():
    # just ensures function accepts None / Series without error
    render_detail(None)
    s = pd.Series({"player": "Test", "team": "Foo", "minutes_played": 90})
    render_detail(s)
