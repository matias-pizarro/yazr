import pandas as pd
import slugify  # type: ignore[import-untyped]
from IPython.core.interactiveshell import InteractiveShell
from IPython.display import HTML, display

__all__ = [
    "set_notebook_options",
    "normalize_column_names",
    "stop_execution",
]


# Config
def set_notebook_options() -> None:
    InteractiveShell.ast_node_interactivity = "all"
    display(HTML("<style>.container { width:95% !important; }</style>"))

    pd.set_option("display.min_rows", 100)
    pd.set_option("display.max_rows", 100)
    pd.set_option("display.max_columns", 200)
    pd.set_option("display.width", 3000)
    pd.set_option("display.max_colwidth", None)

    pd.set_option("display.float_format", lambda x: "%.5f" % x)
    pd.options.display.float_format = "{:.2f}".format


# Normalize
def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    _df = df.copy()
    df_dict = {slugify.slugify(col, separator="_"): col for col in _df.columns}
    _df.columns = df_dict
    return _df, df_dict


def stop_execution() -> None:
    print("stopping")
    raise Exception("stop!")
    print("stopped")
