from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "date",
    "campaign",
    "channel",
    "country",
    "spend",
    "impressions",
    "clicks",
    "installs",
    "conversions",
    "revenue",
]

NUMERIC_COLUMNS = [
    "spend",
    "impressions",
    "clicks",
    "installs",
    "conversions",
    "revenue",
]

TEXT_COLUMNS = [
    "campaign",
    "channel",
    "country",
]


def load_campaign_data(file_path: str | Path) -> pd.DataFrame:
    """Load and validate campaign performance data from a CSV file."""

    try:
        data = pd.read_csv(file_path)
    except pd.errors.EmptyDataError as error:
        raise ValueError("The CSV file is empty.") from error

    if data.empty:
        raise ValueError("The CSV file is empty.")

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    try:
        data["date"] = pd.to_datetime(data["date"], errors="raise")
    except (ValueError, TypeError) as error:
        raise ValueError("Column 'date' contains invalid date values.") from error

    for column in NUMERIC_COLUMNS:
        try:
            data[column] = pd.to_numeric(data[column], errors="raise")
        except (ValueError, TypeError) as error:
            raise ValueError(
                f"Column '{column}' contains invalid numeric values."
            ) from error

        if (data[column] < 0).any():
            raise ValueError(
                f"Column '{column}' cannot contain negative values."
            )

    for column in TEXT_COLUMNS:
        if data[column].isna().any() or data[column].astype(str).str.strip().eq("").any():
            raise ValueError(
                f"Column '{column}' cannot contain empty values."
            )

    return data


if __name__ == "__main__":
    campaign_data = load_campaign_data("data/sample_campaign_data.csv")

    print("Campaign data loaded successfully.")
    print(f"Rows: {len(campaign_data)}")
    print(f"Campaigns: {campaign_data['campaign'].nunique()}")
    print(f"Date range: {campaign_data['date'].min().date()} to {campaign_data['date'].max().date()}")