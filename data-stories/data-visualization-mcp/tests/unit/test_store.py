"""Unit tests for ResourceStore."""
from datetime import datetime, timezone

import pandas as pd

from data_viz_mcp.models import ColumnInfo, Dataset, PlotType, VizSpec, Plot
from data_viz_mcp.store import ResourceStore


def _store():
    return ResourceStore()


def _ds(store):
    ds_id = store.new_id("ds")
    ds = Dataset(id=ds_id, name="test", columns=[ColumnInfo(name="x", dtype="int64")], row_count=1, created_at=datetime.now(timezone.utc))
    df = pd.DataFrame({"x": [1]})
    store.add_dataset(ds, df)
    return ds, df


def _spec(store, ds_id):
    spec_id = store.new_id("vs")
    now = datetime.now(timezone.utc)
    spec = VizSpec(id=spec_id, dataset_id=ds_id, plot_type=PlotType.LINE, x_column="x", y_column=None, created_at=now, updated_at=now)
    store.add_vizspec(spec)
    return spec


def test_new_id_prefixes():
    s = _store()
    assert s.new_id("ds").startswith("ds_")
    assert s.new_id("vs").startswith("vs_")
    assert s.new_id("pl").startswith("pl_")


def test_new_ids_are_unique():
    s = _store()
    ids = {s.new_id("ds") for _ in range(100)}
    assert len(ids) == 100


def test_dataset_add_get_roundtrip():
    s = _store()
    ds, df = _ds(s)
    result = s.get_dataset(ds.id)
    assert result is not None
    got_ds, got_df = result
    assert got_ds.id == ds.id
    assert list(got_df.columns) == list(df.columns)


def test_dataset_get_missing_returns_none():
    s = _store()
    assert s.get_dataset("ds_nonexistent") is None


def test_dataset_list():
    s = _store()
    _ds(s)
    _ds(s)
    assert len(s.list_datasets()) == 2


def test_vizspec_add_get_roundtrip():
    s = _store()
    ds, _ = _ds(s)
    spec = _spec(s, ds.id)
    assert s.get_vizspec(spec.id) is not None
    assert s.get_vizspec(spec.id).id == spec.id  # type: ignore[union-attr]


def test_vizspec_get_missing_returns_none():
    s = _store()
    assert s.get_vizspec("vs_nonexistent") is None


def test_vizspec_update():
    s = _store()
    ds, _ = _ds(s)
    spec = _spec(s, ds.id)
    updated = s.update_vizspec(spec.id, title="New Title")
    assert updated is not None
    assert updated.title == "New Title"
    assert s.get_vizspec(spec.id).title == "New Title"  # type: ignore[union-attr]


def test_plot_add_get_roundtrip():
    s = _store()
    ds, _ = _ds(s)
    spec = _spec(s, ds.id)
    plot_id = s.new_id("pl")
    plot = Plot(id=plot_id, spec_id=spec.id, has_html=False, created_at=datetime.now(timezone.utc))
    s.add_plot(plot, b"pngbytes", None)
    result = s.get_plot(plot_id)
    assert result is not None
    got_plot, png, html = result
    assert got_plot.id == plot_id
    assert png == b"pngbytes"
    assert html is None


def test_plot_get_missing_returns_none():
    s = _store()
    assert s.get_plot("pl_nonexistent") is None
