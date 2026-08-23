import pytest
from app.services.graphing import function_graph

def test_function_graph_produces_bounded_plotly_compatible_spec():
    spec = function_graph([-1, 0, 1], [1, 0, 1], title="y = x²", points=[(0, 0, "turning point")])
    assert spec["data"][0]["type"] == "scatter"
    assert spec["data"][0]["x"] == [-1, 0, 1]
    assert spec["layout"]["title"]["text"] == "y = x²"

def test_function_graph_rejects_unpaired_or_oversized_coordinates():
    with pytest.raises(ValueError):
        function_graph([0, 1], [0], title="invalid")
    with pytest.raises(ValueError):
        function_graph(range(402), range(402), title="too large")
