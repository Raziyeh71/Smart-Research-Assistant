from transformers import pipeline
from typing import List, Tuple, Dict

class Summarizer:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def summarize_text(self, text: str, max_length: int = 130, min_length: int = 30) -> str:
        """
        Generate a summary of the given text using BART
        """
        if not text:
            return ""
            
        # Truncate text to fit model's maximum input length
        max_tokens = 1024
        text = ' '.join(text.split()[:max_tokens])
        
        try:
            summary = self.summarizer(text, 
                                    max_length=max_length, 
                                    min_length=min_length, 
                                    do_sample=False)[0]['summary_text']
            return summary
        except Exception as e:
            print(f"Error in summarization: {str(e)}")
            return text[:max_length] + "..."

    def summarize_papers(self, papers: List[Dict]) -> List[Tuple[Dict, str]]:
        """
        Summarize academic papers
        """
        summaries = []
        for paper in papers:
            text_to_summarize = f"{paper['title']}. {paper['abstract']}"
            summary = self.summarize_text(text_to_summarize)
            summaries.append((paper, summary))
        return summaries

    def summarize_projects(self, projects: List[Dict]) -> List[Tuple[Dict, str]]:
        """
        Summarize GitHub projects
        """
        summaries = []
        for project in projects:
            text_to_summarize = f"{project['description']}. {project['readme']}"
            summary = self.summarize_text(text_to_summarize)
            summaries.append((project, summary))
        return summaries
