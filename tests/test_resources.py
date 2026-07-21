import pandas as pd

from workshop.resources import Warehouse


def test_write_csv_then_read_csv_round_trips(tmp_path):
    warehouse = Warehouse(data_dir=str(tmp_path))
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})

    warehouse.write_csv("sample", df)
    result = warehouse.read_csv("sample")

    assert result.equals(df)
    assert (tmp_path / "sample.csv").exists()
