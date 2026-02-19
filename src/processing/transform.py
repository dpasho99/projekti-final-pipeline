import pandas as pd
from src.api.client import get_country_info

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["title"] = df["title"].astype(str).str.strip()
    return df

def enrich_with_country(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # DEMO: vendos country bazuar në shkronjën e parë të titullit
    df["country_input"] = df["title"].str[0].map(
        lambda ch: "Albania" if ch and ch.upper() < "H" else "Italy"
    )

    regions, pops, currs = [], [], []
    for c in df["country_input"]:
        info = get_country_info(c)
        if info is None:
            regions.append(None)
            pops.append(None)
            currs.append(None)
        else:
            regions.append(info["region"])
            pops.append(info["population"])
            currs.append(info["currencies"])

    df["region"] = regions
    df["population"] = pops
    df["currencies"] = currs
    return df

def compute_metrics(df: pd.DataFrame) -> pd.DataFrame:
    agg = (
        df.groupby(["region", "rating"], dropna=False)
        .agg(avg_price=("price_gbp", "mean"), count=("title", "count"))
        .reset_index()
        .sort_values("count", ascending=False)
    )
    return agg