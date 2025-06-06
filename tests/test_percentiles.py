import pandas as pd
from app.services.percentiles import role_percentiles, load_radar_config

# mock mini-dataset: two roles, three metrics
DATA = {
    "player": ["A", "B", "C", "D"],
    "role":   ["Striker", "Striker", "CB", "CB"],
    "goals_per90": [0.6, 0.2, 0.05, 0.1],
    "shots_per90": [3.0, 1.0, 0.2, 0.3],
    "tackles_per90": [0.1, 0.2, 3.0, 2.5],
}
DF_MOCK = pd.DataFrame(DATA)

RADAR_CFG = {
    "Striker":  ["goals_per90", "shots_per90"],
    "CB":       ["tackles_per90"],
}


def test_percentiles_bounds():
    row = DF_MOCK.loc[0]            # A – Striker 0.6 g/90
    pcts = role_percentiles(row, DF_MOCK, cfg=RADAR_CFG)
    # all values must be within 0–100 and not NaN
    for v in pcts.values():
        assert 0.0 <= v <= 100.0
        assert not pd.isna(v)


def test_highest_value_gets_100():
    row = DF_MOCK.loc[0]            # A has highest goals_per90 among Strikers
    pcts = role_percentiles(row, DF_MOCK, cfg=RADAR_CFG)
    assert pcts["goals_per90"] == 100.0


def test_lowest_value_gets_0():
    row = DF_MOCK.loc[1]            # B has lowest shots_per90 among Strikers
    pcts = role_percentiles(row, DF_MOCK, cfg=RADAR_CFG)
    assert pcts["shots_per90"] == 0.0
