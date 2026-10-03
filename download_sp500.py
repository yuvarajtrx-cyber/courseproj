"""Download daily S&P 500 index (^GSPC) OHLCV data for the last 10 years."""

import argparse
from datetime import date
from pathlib import Path

import pandas as pd
import yfinance as yf

TICKER = "^GSPC"


def download(years: int = 10) -> pd.DataFrame:
    end = date.today()
    start = end.replace(year=end.year - years)
    df = yf.download(
        TICKER,
        start=start.isoformat(),
        end=end.isoformat(),
        interval="1d",
        auto_adjust=False,
        progress=False,
    )
    if df.empty:
        raise RuntimeError(f"No data returned for {TICKER}")
    # yfinance returns MultiIndex columns (field, ticker); flatten to field names.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df.index.name = "Date"
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--years", type=int, default=10)
    parser.add_argument("--out", default="data/sp500_daily_ohlcv.csv")
    args = parser.parse_args()

    df = download(args.years)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out)
    print(f"Saved {len(df)} rows ({df.index[0].date()} to {df.index[-1].date()}) to {args.out}")


if __name__ == "__main__":
    main()
