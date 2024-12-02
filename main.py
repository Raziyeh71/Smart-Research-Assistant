import os
from dotenv import load_dotenv
from research_agent.paper_retriever import PaperRetriever
from research_agent.github_retriever import GitHubRetriever
from research_agent.summarizer import Summarizer
from research_agent.memory_manager import MemoryManager
from research_agent.graph_builder import GraphBuilder
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

def main():
    load_dotenv()
    
    # Initialize components
    paper_retriever = PaperRetriever()
    github_retriever = GitHubRetriever(os.getenv("GITHUB_TOKEN"))
    summarizer = Summarizer()
    memory_manager = MemoryManager()
    graph_builder = GraphBuilder()
    console = Console()
    
    while True:
        query = input("\nEnter your research query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
            
        # Store query in memory
        memory_manager.add_query(query)
        
        # Retrieve papers and projects
        console.print("\n[bold blue]🔍 Searching for papers and projects...[/bold blue]")
        papers = paper_retriever.search(query)
        projects = github_retriever.search(query)
        
        # Generate summaries
        console.print("\n[bold blue]📝 Generating summaries...[/bold blue]")
        paper_summaries = summarizer.summarize_papers(papers)
        project_summaries = summarizer.summarize_projects(projects)
        
        # Update knowledge graph
        graph_builder.update_graph(query, paper_summaries + project_summaries)
        
        # Get personalized insights
        insights = memory_manager.get_insights(query, paper_summaries + project_summaries)
        
        # Display results in a beautiful format
        console.print("\n[bold green]📚 Research Findings[/bold green]")
        console.print("=" * 80)
        
        # Display papers
        console.print("\n[bold cyan]📄 Relevant Papers[/bold cyan]")
        for paper, summary in paper_summaries:
            paper_md = f"""
### {paper['title']}

**Authors:** {', '.join(paper['authors'])}
**Year:** {paper.get('year', 'N/A')}
**Citations:** {paper.get('citations', 'N/A')}
**URL:** {paper.get('url', 'N/A')}

**Summary:**
{summary}

---
"""
            console.print(Panel(Markdown(paper_md), title="Research Paper", border_style="cyan"))
            
        # Display GitHub projects
        console.print("\n[bold magenta]💻 Relevant GitHub Projects[/bold magenta]")
        for project, summary in project_summaries:
            project_md = f"""
### [{project['full_name']}]({project['url']})

**Stars:** {project.get('stars', 0)} ⭐
**Language:** {project.get('language', 'N/A')}
**Last Updated:** {project.get('updated_at', 'N/A')}
**Topics:** {', '.join(project.get('topics', []))}

**Summary:**
{summary}

**Paper References:**
{chr(10).join(['- ' + ref for ref in project.get('paper_references', [])])}

---
"""
            console.print(Panel(Markdown(project_md), title="GitHub Project", border_style="magenta"))
            
        # Display insights
        if insights:
            console.print("\n[bold yellow]💡 Personalized Insights[/bold yellow]")
            console.print(Panel(insights, title="Based on Your Research History", border_style="yellow"))
        
        console.print("\n[bold green]✨ Research Complete![/bold green]")
        console.print("Use these findings to advance your research. Happy coding! 🚀\n")

if __name__ == "__main__":
    main()
