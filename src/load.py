import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def load_to_postgres(df):

    USER = os.getenv("POSTGRES_USER")
    PASSWORD = os.getenv("POSTGRES_PASSWORD")
    HOST = os.getenv("POSTGRES_HOST")
    PORT = os.getenv("POSTGRES_PORT")
    DATABASE = os.getenv("POSTGRES_DB")

    engine = create_engine(
        f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    )

    df.to_sql(
        "sales",
        engine,
        if_exists="replace",
        index=False
    )

    print("Data loaded successfully into PostgreSQL.")