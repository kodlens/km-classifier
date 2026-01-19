import re
import requests
import json
from sqlalchemy import create_engine, text
from datetime import datetime

OLLAMA_API = "http://127.0.0.1:11434/api/generate"
#wsl hostname -I  <--- this command display IP
#OLLAMA_API = "http://172.29.194.254:11435/api/generate"
#OLLAMA_API = "http://172.25.214.89:11434/api/generate"


MODEL = "llama3"

def classify_and_insert_article(info_id, description_text, sh_ids, subject_headings, top_k=5):
    # Create prompt for Ollama classification
    # prompt = f"""
    #     You are a professional text classifier for a knowledge management system.
    #     Given the article below, select the {top_k} most relevant subject headings with id from this list:

    #     {' | '.join(sh_ids) + ':' .join(subject_headings)}

    #     Article:
    #     \"\"\"{description_text}\"\"\"

    #     Respond only with a valid JSON array of objects, each having "id", "label", "score" and "analysis" keys, like:
    #     [
    #         {{ "id": "192", "label": "Science and Technology Programs", "score": 0.95, "analysis": "Your analysis why you classified this..." }},
    #         {{ "id": "23", "label": "Languages and Linguistics", "score": 0.85, "analysis": "Your analysis why you classified this..." }}
    #     ]
        
    #     Do not add anything except valid json response.
    # """
    
    # prompt = f"""
    #     You are a professional article classifier.

    #     Given the article below, select the top {top_k} most relevant subject headings from the SubjectHeadings.
    #     Each subject heading includes both an ID and label, formatted as: ID:Label. Strictly follow the format. 
    #     Use the label for subject heading and make a relevance on the article and pick the correspond id of the selected subject heading.
        
    #     SubjectHeadings:
    #     { ' | '.join([f"{id}:{label}" for id, label in zip(sh_ids, subject_headings)]) }

    #     Article:
    #     \"\"\"{description_text}\"\"\"
        
        
    #     Pick the id from the SubjectHeadings
        
    #     Respond **only** with a valid JSON array of objects, each having the following keys:
    #     - "id": the SubjectHeading ID (string)
    #     - "label": the SubjectHeading label (string)
    #     - "score": relevance score (float between 0 and 1)
    #     - "analysis": a short explanation of why this classification fits the article or empty string if nothing is relevant.
        
        
    #     Example format:
    #     [
    #         {{
    #             "id": 153,
    #             "label": "Physics",
    #             "score": 0.95,
    #             "analysis": "The article discusses about motion."
    #         }},
    #         {{
    #             "id": 181,
    #             "label": "Aquaculture, Fisheries, Angling",
    #             "score": 0.85,
    #             "analysis": "It focuses on fishpond and study life in water."
    #         }}
    #     ]

    #     Strictly do not include anything else, only valid JSON response.
    # """
    
    
    prompt = f"""
        You are a strict classification engine, not a chatbot.

        TASK:
        Select up to {top_k} MOST RELEVANT subject headings from the list below.
        If no subject heading is clearly relevant, return an EMPTY JSON array [].

        RULES (MUST FOLLOW):
        - Choose ONLY from the provided SubjectHeadings.
        - Do NOT guess or infer loosely related topics.
        - Only select a subject heading if it is DIRECTLY and CLEARLY related.
        - Maximum output items: {top_k}
        - Minimum relevance score to include an item: 0.50
        - If fewer than {top_k} meet the threshold, return fewer.
        - If below threshold, use the Others

        SubjectHeadings (ID:Label):
        { ' | '.join([f"{id}:{label}" for id, label in zip(sh_ids, subject_headings)]) }

        Article:
        \"\"\"{description_text}\"\"\"


        OUTPUT FORMAT:
        Respond ONLY with valid JSON.

        Each object must contain:
        - "id": SubjectHeading ID (number)
        - "label": SubjectHeading label (string)
        - "score": float between 0.70 and 1.00
        - "analysis": short factual justification (1 sentence max)

        EXAMPLE:
        [
        {{
            "id": 153,
            "label": "Physics",
            "score": 0.92,
            "analysis": "The article discusses motion, force, and physical laws."
        }}
        ]

        Do NOT include explanations, markdown, or extra text.
        Return ONLY JSON.
        """

    # Send request to Ollama
    response = requests.post(OLLAMA_API, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2}
    })
    
    #print("PROMPT: ", prompt)

    result_text = response.json().get("response", "").strip()
    print()
    print('OLLAMA RESPONSE: ', result_text)
    
    try:
        parsed = json.loads(result_text)
        
    except json.JSONDecodeError:
        # fallback: extract labels manually
        print()
        print('------------ ERROR PARSING JSON FROM AI. Trying other method... -----------')
        print()
        
        parsed = []
        
        partial_json = re.findall(r'\{[^{}]+\}', result_text)
        parsed = []
        for obj_str in partial_json:
            try:
                parsed.append(json.loads(obj_str))
            except json.JSONDecodeError:
                continue  # skip malformed object
                
        # for label in subject_headings:
        #     if label.lower() in result_text.lower():
        #         parsed.append({"id":0,"label": label, "score": 0.5, "analysis":""})
                
            

    
    # Limit top_k
    parsed = parsed[:top_k]
    # print()
    # print('PARSED AFTER TRY AND CATCH: ', parsed)
    # print("TYPE:", type(parsed))
    # print("LENGTH:", len(parsed))
    print()
    
    # Map labels back to their IDs and prepare for DB insertion
    # print("-------MAPPING LABELS--------")
    # print()
    
    #top_results = []
    # for p in parsed:
    #     if not isinstance(p, dict):
    #         print("Skipping non-dict item:", p)
    #         continue
        
    #     lbl = p["label"].strip()  # remove leading/trailing spaces
    #     print(f'MAPPING ------ {lbl}')
    #     score = float(p.get("score", 0.5))
    #     analysis = p["analysis"]

    #     if lbl in subject_headings:
    #         idx = subject_headings.index(lbl)
    #         print('LABEL INDEX ', idx)
    #         label_id = sh_ids[idx]
    #         print('ID OF THE LABEL ', label_id)
    #         print('LABEL IS ', lbl)
            
    #         top_results.append({"id": label_id, "label": lbl, "score": score, "analysis": analysis})
    #         print(f'MAPPED ------ {lbl}')
           
    #     else:
    #         print(f"No match found for '{lbl}'\n")

    # DB connection info
    host = "localhost"
    user = "root"
    password = ""
    database = "km_test"
    table = "info_subject_headings"

    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

    insert_query = text(f"""
        INSERT INTO {table} (info_id, subject_heading_id, score, analysis, created_at)
        VALUES (:info_id, :subject_heading_id, :score, :analysis, :created_at)
    """)
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requiredKeys = ["id", "label", "score", "analysis"];
    
    #print(f"test parsed {parsed[0]['id']}")
    
    
    # Insert results
    with engine.begin() as conn:
        #for res in top_results:
        for res in parsed:
            print()
            print(f'INSERTING TO DB ---- [{res["id"]}] {res["label"]} [score: {res["score"]}] ')
            print(f'ANALYSIS: {res["analysis"]}')
            if res["score"] > 0.5 :
                conn.execute(insert_query, {
                    "info_id": info_id,
                    "subject_heading_id": res["id"],
                    "score": res["score"],
                    "analysis": res["analysis"],
                    "created_at": current_time
                })
                
                print('---------INSERTED--------')
                print()
            else :
                print(f"EXCLUDED ------ Score is below 0.5 [{res['id']}] {res['label']} [{res['score']}]")
                
            print()

    return {"results": parsed}
