import pandas as pd

def clean_data(df):

    df.columns = (
        df.columns
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Converter datas
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        format="%d/%m/%Y"
    )

    df["ship_date"] = pd.to_datetime(
        df["ship_date"],
        format="%d/%m/%Y"
    )

    df = df.dropna()

    return df