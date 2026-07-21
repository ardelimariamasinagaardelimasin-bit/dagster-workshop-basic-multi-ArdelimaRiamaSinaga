import os

import pandas as pd
from dagster import ConfigurableResource


class Warehouse(ConfigurableResource):
    data_dir: str

    def _path(self, name: str) -> str:
        return os.path.join(self.data_dir, f"{name}.csv")

    def read_csv(self, name: str) -> pd.DataFrame:
        return pd.read_csv(self._path(name))

    def write_csv(self, name: str, df: pd.DataFrame) -> None:
        df.to_csv(self._path(name), index=False)
