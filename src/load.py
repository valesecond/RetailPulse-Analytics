import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text

load_dotenv()


def _load_table(df, table_name, engine):

    inspector = inspect(engine)

    if inspector.has_table(table_name):
        with engine.begin() as connection:
            connection.execute(text(f"DELETE FROM {table_name}"))

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False
    )


def load_to_postgres(df_original, df_pt_br):

    USER = os.getenv("POSTGRES_USER", "postgres")
    PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    HOST = os.getenv("POSTGRES_HOST", "localhost")
    PORT = os.getenv("POSTGRES_PORT", "5432")
    DATABASE = os.getenv("POSTGRES_DB", "retailpulse")

    engine = create_engine(
        f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    )

    _load_table(df_original, "sales", engine)

    _load_table(df_pt_br, "sales_pt_br", engine)

    print("Data loaded successfully into PostgreSQL.")