import plotly.graph_objects as go
from app.services.radar import build_radar, save_png

def _dummy():
    return {
        "goals": 90,
        "xG": 75,
        "shots": 60,
        "dribbles": 40,
        "pressures": 20,
    }

def test_returns_figure():
    fig = build_radar(_dummy(), title="Test")
    assert isinstance(fig, go.Figure)
    # first + last point identical ⇒ closed polygon
    pts = fig.data[0].r
    assert pts[0] == pts[-1]

def test_save_png_under_50kb(tmp_path):
    fig = build_radar(_dummy())
    path = tmp_path / "radar.png"
    _, size = save_png(fig, path)
    assert size <= 50_000
