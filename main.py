import os
from dotenv import load_dotenv
from research_agent.paper_retriever import PaperRetriever
from research_agent.github_retriever import GitHubRetriever
from research_agent.summarizer import Summarizer
from research_agent.memory_manager import MemoryManager
from research_agent.graph_builder import GraphBuilder

def main():
    load_dotenv()
    
    # Initialize components
    paper_retriever = PaperRetriever()
    github_retriever = GitHubRetriever(os.getenv("GITHUB_TOKEN"))
    summarizer = Summarizer()
    memory_manager = MemoryManager()
    graph_builder = GraphBuilder()
    
    while True:
        query = input("\nEnter your research query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
            
        # Store query in memory
        memory_manager.add_query(query)
        
        # Retrieve papers and projects
        papers = paper_retriever.search(query)
        projects = github_retriever.search(query)
        
        # Generate summaries
        paper_summaries = summarizer.summarize_papers(papers)
        project_summaries = summarizer.summarize_projects(projects)
        
        # Update knowledge graph
        graph_builder.update_graph(query, paper_summaries + project_summaries)
        
        # Get personalized insights based on memory
        insights = memory_manager.get_insights(query, paper_summaries + project_summaries)
        
        # Display results
        print("\nFindings:")
        print("=========")
        print("\nRelevant Papers:")
        for paper, summary in paper_summaries:
            print(f"\nTitle: {paper['title']}")
            print(f"Summary: {summary}")
            
        print("\nRelevant GitHub Projects:")
        for project, summary in project_summaries:
            print(f"\nRepo: {project['full_name']}")
            print(f"Summary: {summary}")
            
        print("\nInsights based on your research history:")
        print(insights)
        
        # Visualize the knowledge graph
        graph_builder.visualize()

if __name__ == "__main__":
    main()
