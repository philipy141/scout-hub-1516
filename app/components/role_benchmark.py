# app/components/role_benchmark.py
import plotly.graph_objects as go
import streamlit as st
from app.services.benchmarks import role_benchmarks
import pandas as pd

ICON = {"top": "🔼", "bottom": "🔽", "": ""}

def render_benchmark(
    player: pd.Series,
    population: pd.DataFrame,
    metrics: list[str],
    role_key: str = "radar_role"
) -> None:
    df = role_benchmarks(player, population, metrics, role_key)

    # build horizontal bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=[f"{ICON[q]} {m}" for m, q in zip(df.metric, df.quartile)],
        x=df.player_pct,
        orientation='h',
        name="Player",
        marker=dict(color='rgba(50, 150, 250, 0.6)')
    ))
    # add role‐average as lines
    for idx, row in df.iterrows():
        fig.add_shape(dict(
            type="line", x0=row.role_avg_pct, x1=row.role_avg_pct,
            y0=idx-0.4, y1=idx+0.4,
            line=dict(color="black", dash="dash")
        ))

    fig.update_layout(
        title="Versus Role Benchmark",
        xaxis=dict(range=[0, 100], title="Percentile"),
        yaxis=dict(autorange="reversed"),  # so first metric on top
        height=50 * len(metrics) + 100,
        margin=dict(l=100, r=20, t=40, b=20),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)
