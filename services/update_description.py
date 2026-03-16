

from sqlalchemy import text


def update_description(id, clean_html, engine):
    
    update = text(f"""
        UPDATE materials SET description_text = :description_text WHERE id = :id
    """)
    
    with engine.begin() as conn:
        conn.execute(update, {
            "description_text": clean_html,
            "id": id
        })