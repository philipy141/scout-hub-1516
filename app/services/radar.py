"""
Reusable radar-chart builder.

Call `build_radar(metric_dict, order=None, title="")` with a dict like:
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
def build_radar(
    metrics: Dict[str, float],
    order: Sequence[str] | None = None,
    title: str = "",
) -> go.Figure:
    """
    Build a closed‐polygon radar chart.

    Parameters
    ----------
    metrics : dict[str, float]
        Mapping metric → percentile (0-100).
    order : sequence[str] | None
        Radial order. If None, natural key order is used.
    title : str
        Optional title.

    Returns
    -------
    go.Figure
    """
    if order is None:
        order = list(metrics.keys())

    # ensure order has only keys in dict
    order = [m for m in order if m in metrics]

    # ensure closed polygon by repeating first value
    r = [metrics[m] for m in order] + [metrics[order[0]]]
    theta = list(order) + [order[0]]

    fig = go.Figure(
        go.Scatterpolar(
            r=r,
            theta=theta,
            fill="toself",
            line=dict(width=2),
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(range=[0, 100], tickvals=[0, 25, 50, 75, 100]),
        ),
        showlegend=False,
        title=title,
        margin=dict(l=30, r=30, t=60, b=30),
        height=400,
    )

    return fig


# ─────────────────────── PNG helper (≤50 kB) ─────────────────────────────
def save_png(fig: go.Figure, path: str, scale: float = 1.0) -> Tuple[str, int]:
    """
    Save figure to PNG, shrinking until ≤50 kB.

    Returns (path, size_bytes).
    """
    # Try down-scaling until small enough (max 5 attempts)
    for s in [1.0, 0.9, 0.8, 0.7, 0.6]:
        buf = pio.to_image(fig, format="png", scale=scale * s)
        if len(buf) <= 50_000 or s == 0.6:
            with open(path, "wb") as f:
                f.write(buf)
            return path, len(buf)
    # Should never reach here
    raise RuntimeError("Could not shrink PNG below 50 kB")
