import pandas as pd
from sqlalchemy import create_engine

def load_from_infos(
    host="localhost",
    user="root",
    password="",
    database="scienceph_km_new",
    table="materials"
) -> pd.DataFrame:
    """
    Connect to MySQL and load data into a Pandas DataFrame.
    """

    # Create connection string for SQLAlchemy
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

    # Read table directly into DataFrame
    query = f"SELECT * FROM {table} WHERE id > (SELECT material_id FROM material_subject_headings ORDER BY id DESC LIMIT 1) ORDER BY id ASC"
    #query = f"SELECT * FROM {table} ORDER BY id ASC LIMIT 10"
    #query = f"SELECT id, article_id, title, excerpt, description, description_text, alias, publish_date FROM {table} ORDER BY id ASC"
    df = pd.read_sql(query, engine)

    # Example cleaning: drop NA values
    # df = df.dropna()

    return df