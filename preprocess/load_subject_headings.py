from typing import Tuple, List
import pandas as pd
from sqlalchemy import create_engine

def load_subject_headings(
    host:str='localhost',
    user:str='root',
    password:str='',
    database:str='km_external_congress',
    table:str='subject_headings'
) -> Tuple[List[int], List[str]] :
    
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
    query = f"SELECT id, subject_heading FROM {table} ORDER BY subject_heading ASC"
    df = pd.read_sql(query, engine)
    
    ids = df["id"].tolist()
    labels = df["subject_heading"].tolist()

   # print(df)
    return ids, labels