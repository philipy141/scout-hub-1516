"""
Reusable radar-chart builder.

Call `build_radar(metric_dict, title="", raw=None)` with a dict like:
    {
        "goals_per90":     87.4,
        "xg_per_shot":     42.0,
        "progressive_carries": 66.7,
        ...
    }
Returns a Plotly `go.Figure`.

Use `save_png(fig, path)` to persist ≤50 kB PNGs.
"""

from __future__ import annotations
import io
from typing import Dict, Sequence, Tuple

import plotly.graph_objects as go
import plotly.io as pio


# ─────────────────────────── Core builder ────────────────────────────────
def build_radar(metrics: dict, raw: dict | None = None, title: str = "") -> go.Figure:
    if not metrics:
        return go.Figure()

    order = list(metrics.keys())
    r = [metrics[m] for m in order] + [metrics[order[0]]]
    theta = order + [order[0]]

    # Prepare tooltip text if raw is provided
    if raw:
        hover = [f"{m}: {raw.get(m, '–')}" for m in order]
        hover += [hover[0]]  # close the loop
    else:
        hover = None

    fig = go.Figure(
        data=go.Scatterpolar(
            r=r,
            theta=theta,
            fill='toself',
            name=title,
            hovertext=hover,
            hoverinfo="text" if hover else "all"
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        margin=dict(t=40, r=40, b=40, l=40),
        height=400,
    )
    return fig



# ─────────────────────── PNG helper (≤50 kB) ─────────────────────────────
def save_png(fig: go.Figure, path: str, scale: float = 1.0) -> Tuple[str, int]:
    """
    Save figure to PNG, shrinking until ≤50 kB.

    Returns (path, size_bytes).
    """
    for s in [1.0, 0.9, 0.8, 0.7, 0.6]:
        buf = pio.to_image(fig, format="png", scale=scale * s)
        if len(buf) <= 50_000 or s == 0.6:
            with open(path, "wb") as f:
                f.write(buf)
            return path, len(buf)
    raise RuntimeError("Could not shrink PNG below 50 kB")
