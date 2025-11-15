import pandas as pd
from sqlalchemy import create_engine

def load_from_snt(
    host="localhost",
    user="root",
    password="",
    database="sntpost",
    table="posts"
) -> pd.DataFrame:
    """
    Connect to MySQL and load data into a Pandas DataFrame.
    """

    # Create connection string for SQLAlchemy
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

    # Read table directly into DataFrame
    query = f"SELECT id, excerpt, title, description, description_text FROM {table} WHERE status='publish'"
    df = pd.read_sql(query, engine)

    # Example cleaning: drop NA values
    #df = df.dropna()

    return df