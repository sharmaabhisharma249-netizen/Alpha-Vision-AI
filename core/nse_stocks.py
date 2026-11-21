import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "nifty500.csv"


def load_nse_stocks():
    df = pd.read_csv(DATA_PATH)

    df = df.rename(columns={
        "Company Name": "Company",
        "Industry": "Sector"
    })
    df["Symbol"] = df["Symbol"].astype(str) + ".NS"
    return df[["Symbol", "Company", "Sector"]]
    