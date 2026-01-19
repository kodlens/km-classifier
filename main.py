from preprocess import load_from_infos, load_from_scienceph, load_subject_headings
from services import insert_scienceph, classify_and_insert_article


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
    
    
    # =========================================================
    # This section is for classifying the inserted articles (infos)
    # =========================================================
    infos_df = load_from_infos() # get articles from infos
    sh_ids, subject_headings = load_subject_headings() # get the subject headings
    
    print(subject_headings)
    for index, row in infos_df.iterrows():
        print()
        print("=======================FETCHED ROW=======================")
        
        print("index: ", index)
        print("Info Id: ", row["id"])
        print("title: ", row["title"])
        print("description: ", row["description_text"])
       
        result = classify_and_insert_article(row["id"], row["description_text"], sh_ids, subject_headings)
        print("===================DONE CLASSIFIED======================")
    



if __name__ == "__main__":
    run()
