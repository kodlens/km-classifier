import pandas as pd
from sqlalchemy import create_engine

def load_from_infos(
    host="localhost",
    user="root",
    password="",
    database="km_mock_external",
    table="infos"
) -> pd.DataFrame:
    """
    Connect to MySQL and load data into a Pandas DataFrame.
    """

    # Create connection string for SQLAlchemy
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

    # Read table directly into DataFrame
    query = f"SELECT id, article_id, title, excerpt, description, description_text, alias, publish_date FROM {table} WHERE id < (SELECT info_id FROM info_subject_headings ORDER BY info_id ASC LIMIT 1) ORDER BY id DESC"
    df = pd.read_sql(query, engine)

    # Example cleaning: drop NA values
    # df = df.dropna()

    return df