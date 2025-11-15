import pandas as pd
from sqlalchemy import create_engine

def load_from_scienceph(
    host="localhost",
    user="root",
    password="",
    database="science_ph",
    table="articles"
) -> pd.DataFrame:
    """
    Connect to MySQL and load data into a Pandas DataFrame.
    """

    # Create connection string for SQLAlchemy
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

    # Read table directly into DataFrame
    query = f"SELECT article_id, title, introtext, alias, publish_date FROM {table}"
    df = pd.read_sql(query, engine)

    # Example cleaning: drop NA values
    # df = df.dropna()

    return df