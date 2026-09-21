import argparse
from pathlib import Path
import pandas as pd

BUCKETS = [-1, 1, 2, 4, 7, 12, 24, float("inf")]
LABELS = ["<1h", "1-2h", "2-4h", "4-7h", "7-12h", "12-24h", "24h+"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input, parse_dates=["process_time"])
    now = pd.Timestamp.now()

    out = df[
        (df["status"] == "OPEN") &
        (df["event_name"].str.contains("OUTAGE", case=False, na=False))
    ].copy()

    out["down_ageing_hours"] = (now - out["process_time"]).dt.total_seconds() / 3600
    out["ageing_bucket"] = pd.cut(
        out["down_ageing_hours"],
        bins=BUCKETS,
        labels=LABELS
    )

    out = out.sort_values("process_time").drop_duplicates("site_id", keep="first")

    summary = pd.pivot_table(
        out,
        index="circle",
        columns="ageing_bucket",
        values="site_id",
        aggfunc="nunique",
        fill_value=0,
        observed=False
    )
    summary["site_down_total"] = summary.sum(axis=1)

    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(target, engine="openpyxl") as writer:
        out.to_excel(writer, sheet_name="Open Outages", index=False)
        summary.reset_index().to_excel(writer, sheet_name="Summary", index=False)

if __name__ == "__main__":
    main()
