from sqlalchemy import create_engine

from preprocess import load_from_infos, load_from_scienceph, load_subject_headings
from services import insert_scienceph, classify_and_insert_article, update_description
from utils import html_cleaner


def run():

    # =========================================================
    # This section here is for loading the articles from science ph DB
    #scienceph_df = load_from_scienceph() # get articles from scienceph
    #print(scienceph_df)
    # =========================================================
    
    
    
    # =========================================================
    # This section here is for inserting the loaded scienceph articles to the KM info table
    #insert_scienceph(scienceph_df) # insert artcles to info table
    # =========================================================
    host="localhost"
    user="root"
    password=""
    database="scienceph_km_new"
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
    
    # =========================================================
    # This section is for classifying the inserted articles (infos)
    # =========================================================
    infos_df = load_from_infos() # get articles from infos
    
    # for index, row in infos_df.iterrows():
    #     clean_html = html_cleaner(row["description"])
    #     update_description(row['id'], clean_html, engine)
    
    
    sh_ids, subject_headings = load_subject_headings() # get the subject headings
    print(subject_headings)
    for index, row in infos_df.iterrows():
        print()
        print("=======================FETCHED ROW=======================")
        
        print("index: ", index)
        print("Info Id: ", row["id"])
        print("title: ", row["title"])
        print("description: ", row["description_text"])
       
        result = classify_and_insert_article(engine, row["id"], row["description_text"], sh_ids, subject_headings, 5)
        print("===================DONE CLASSIFIED======================")
    



if __name__ == "__main__":
    run()
