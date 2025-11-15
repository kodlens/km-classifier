from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, InfoSubjectHeading

def insert_info_subject_heading(data) -> None:
    KM_EXTERNAL = "mysql+mysqlconnector://root:@localhost/km_external"
    # 👇 connection string directly here (MySQL local DB "scienceph")
    
    if data is not None and not data.empty:
        # create engine + session for scienceph DB
        engine = create_engine(KM_EXTERNAL, echo=True)
        Session = sessionmaker(bind=engine)

        # create table if not exists
        Base.metadata.create_all(bind=engine)

        # open session
        session = Session()
        info_data = []

        for index, row in data.iterrows() :
            # insert one record
            new_data = InfoSubjectHeading(
                info_id=row['info_id'], 
                subject_heading_id=row['subject_heading_id'],
            )
            info_data.append(new_data)

        session.add_all(info_data)
        session.commit()
        session.close()
        
        print("Inserted successfully.")

    else :

        print('No scienceph data detected.')