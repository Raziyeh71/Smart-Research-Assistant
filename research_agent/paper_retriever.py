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
        try:
            search_query = scholarly.search_pubs(query)
            
            for _ in range(self.max_results):
                try:
                    paper = next(search_query)
                    # Handle the paper data directly as it comes from scholarly
                    paper_info = {
                        'title': paper['bib'].get('title', ''),
                        'authors': paper['bib'].get('author', []),
                        'year': paper['bib'].get('year', ''),
                        'abstract': paper['bib'].get('abstract', ''),
                        'url': paper['pub_url'] if 'pub_url' in paper else '',
                        'citations': paper.get('num_citations', 0)
                    }
                    papers.append(paper_info)
                except StopIteration:
                    break
                except Exception as e:
                    print(f"Error processing paper: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Error searching papers: {str(e)}")
            
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
