from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Info
from utils import html_cleaner
from utils import slugify

def insert_scienceph(data, table="km_mock_external") -> None:
    # 👇 connection string directly here (MySQL local DB "scienceph")
    host="localhost"
    user="root"
    password=""
    database="km_mock_external"
    
    if data is not None and not data.empty:
        # create engine + session for scienceph DB
       # engine = create_engine(KM_EXTERNAL, echo=True)
        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
        
        Session = sessionmaker(bind=engine)

        # create table if not exists
        Base.metadata.create_all(bind=engine)

        # open session
        session = Session()
        infos = []

        for index, row in data.iterrows() :
            # insert one record
            new_info = Info(
                title=row['title'], 
                excerpt='', 
                description=row['introtext'],
                description_text=html_cleaner(row['introtext']),
                #alias=slugify(row['title'])\
                alias=row['alias'],
                source='scienceph',
                publish_date=row['publish_date']
            )
            infos.append(new_info)

        session.add_all(infos)
        session.commit()
        session.close()
        
        print("Inserted successfully.")

    else :

        print('No scienceph data detected.')