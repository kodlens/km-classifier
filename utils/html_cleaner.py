
 #pip install beautifulsoup4
from bs4 import BeautifulSoup

def html_cleaner(html_content='') -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    clean_text = soup.get_text(separator=" ", strip=True)
    print('clean')

    return clean_text