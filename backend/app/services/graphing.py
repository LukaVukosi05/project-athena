"""Validated Plotly figure specifications for the browser whiteboard."""
from collections.abc import Sequence
import json
try:
    import plotly.graph_objects as go
except ImportError:  # Local/offline fallback; production installs requirements.txt.
    go = None

def function_graph(x: Sequence[float], y: Sequence[float], *, title: str,
                   x_label: str = "x", y_label: str = "y",
                   points: Sequence[tuple[float, float, str]] = ()) -> dict:
    """Create a bounded graph spec from curriculum-authored coordinates."""
    if len(x) != len(y) or len(x) < 2 or len(x) > 401:
        raise ValueError("Graph coordinates must contain 2 to 401 paired points")
    if go is None:
        data = [{"type": "scatter", "x": list(x), "y": list(y), "mode": "lines", "name": title}]
        if points:
            data.append({"type": "scatter", "x": [p[0] for p in points], "y": [p[1] for p in points], "text": [p[2] for p in points], "mode": "markers+text"})
        return {"data": data, "layout": {"title": {"text": title}, "xaxis": {"title": {"text": x_label}}, "yaxis": {"title": {"text": y_label}}}}
    figure = go.Figure(go.Scatter(x=list(x), y=list(y), mode="lines", name=title,
                                  line={"color": "#2456CF", "width": 4}))
    if points:
        figure.add_trace(go.Scatter(x=[p[0] for p in points], y=[p[1] for p in points],
            text=[p[2] for p in points], mode="markers+text", textposition="top center",
            marker={"color": "#B45309", "size": 10}, name="Key points"))
    figure.update_layout(title={"text": title}, xaxis_title=x_label, yaxis_title=y_label,
        showlegend=False, template="plotly_white", margin={"l": 45, "r": 20, "t": 45, "b": 45})
    return json.loads(figure.to_json())
