from scholarly import scholarly
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

class PaperRetriever:
    def __init__(self):
        self.max_results = 5

    def search(self, query: str) -> List[Dict]:
        """
        Search for academic papers using Google Scholar
        """
        papers = []
        search_query = scholarly.search_pubs(query)
        
        for i in range(self.max_results):
            try:
                paper = next(search_query)
                paper_info = {
                    'title': paper.bib.get('title', ''),
                    'authors': paper.bib.get('author', []),
                    'year': paper.bib.get('year', ''),
                    'abstract': paper.bib.get('abstract', ''),
                    'url': paper.bib.get('url', ''),
                    'citations': paper.citedby
                }
                papers.append(paper_info)
            except StopIteration:
                break
            
        return papers

    def get_full_text(self, url: str) -> str:
        """
        Attempt to retrieve full text of paper (when available)
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # This is a simplified version - actual implementation would need
                # to handle different paper hosting sites differently
                text = soup.get_text()
                return text
        except:
            pass
        return ""
