from typing import List, Dict
import chromadb
from datetime import datetime

class MemoryManager:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("research_memory")

    def add_query(self, query: str):
        """
        Store a new query in memory
        """
        timestamp = datetime.now().isoformat()
        self.collection.add(
            documents=[query],
            metadatas=[{"timestamp": timestamp, "type": "query"}],
            ids=[f"query_{timestamp}"]
        )

    def add_content(self, content: str, content_type: str):
        """
        Store content (papers, projects) in memory
        """
        timestamp = datetime.now().isoformat()
        self.collection.add(
            documents=[content],
            metadatas=[{"timestamp": timestamp, "type": content_type}],
            ids=[f"{content_type}_{timestamp}"]
        )

    def get_insights(self, current_query: str, current_findings: List[tuple]) -> str:
        """
        Generate insights based on current query and past research history
        """
        # Search for related past queries and findings
        results = self.collection.query(
            query_texts=[current_query],
            n_results=5
        )
        
        if not results["documents"]:
            return "This is your first query on this topic."
            
        # Analyze patterns and generate insights
        past_queries = [doc for doc, metadata in zip(results["documents"][0], results["metadatas"][0]) 
                       if metadata["type"] == "query"]
        
        insights = []
        
        if past_queries:
            insights.append("Related to your previous research:")
            for query in past_queries:
                insights.append(f"- {query}")
        
        # Add insights about current findings
        if current_findings:
            insights.append("\nKey connections in current findings:")
            for item, summary in current_findings[:3]:
                if isinstance(item, dict):
                    title = item.get('title', item.get('full_name', 'Unknown'))
                    insights.append(f"- {title}")
        
        return "\n".join(insights)
