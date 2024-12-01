# Smart Research Assistant

A powerful research assistant that leverages LangGraph, LangChain, and MemoryGPT to help track and analyze academic papers and GitHub projects.

## Features

- Retrieves latest academic papers and GitHub projects
- Summarizes content using deep learning
- Builds semantic graphs showing connections between research topics
- Maintains context of past queries for personalized insights
- Visualizes research trends and relationships

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file with your API keys:
```
OPENAI_API_KEY=your_key_here
GITHUB_TOKEN=your_github_token
```

## Usage

Run the main application:
```bash
python main.py
```

## Project Structure

- `main.py`: Entry point of the application
- `research_agent/`: Core agent implementation
  - `paper_retriever.py`: Academic paper retrieval logic
  - `github_retriever.py`: GitHub project retrieval
  - `summarizer.py`: Deep learning-based summarization
  - `memory_manager.py`: MemoryGPT implementation
  - `graph_builder.py`: Semantic graph construction
- `utils/`: Utility functions
- `data/`: Storage for retrieved data and generated graphs
