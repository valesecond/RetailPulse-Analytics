from src.extract import load_data
from src.transform import clean_data
from src.load import load_to_postgres

def main():

    # Extração
    df = load_data("data/raw/sales.csv")

    # Transformação
    df = clean_data(df)

    # Salvando CSV tratado
    df.to_csv(
        "data/processed/clean_sales.csv",
        index=False
    )

    # Carregando no PostgreSQL
    load_to_postgres(df)

    print("\nPipeline executed successfully.\n")

    print(df.head())

if __name__ == "__main__":
    main()