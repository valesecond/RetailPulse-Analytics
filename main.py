from src.extract import load_data
from src.transform import clean_data, translate_to_pt_br
from src.load import load_to_postgres

def main():

    df = load_data("data/raw/sales.csv")

    df_clean = clean_data(df)
    df_pt_br = translate_to_pt_br(df_clean)

    df_clean.to_csv(
        "data/processed/clean_sales.csv",
        index=False
    )

    df_pt_br.to_csv(
        "data/processed/clean_sales_pt_br.csv",
        index=False
    )

    load_to_postgres(df_clean, df_pt_br)

    print("\nPipeline executed successfully.\n")

    print(df_clean.head())

if __name__ == "__main__":
    main()