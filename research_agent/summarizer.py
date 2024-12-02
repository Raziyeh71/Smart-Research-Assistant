"""
Research Paper Summarizer Module

This module provides intelligent summarization of research papers and GitHub projects
using advanced NLP techniques to extract key findings and contributions.
"""

from typing import List, Dict, Tuple, Any
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Summarizer:
    """A class to generate intelligent summaries of research papers and projects."""

    def __init__(self):
        """Initialize the summarizer with OpenAI configuration."""
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-3.5-turbo"  # Using a specific model to avoid rate limits
        self.retry_delay = 5  # seconds to wait between retries

    def summarize_papers(self, papers: List[Dict]) -> List[Tuple[Dict, str]]:
        """
        Generate concise, intelligent summaries of academic papers.

        Args:
            papers (List[Dict]): List of paper information dictionaries

        Returns:
            List[Tuple[Dict, str]]: List of (paper_info, summary) tuples
        """
        summaries = []
        for paper in papers:
            try:
                # Create a prompt that extracts key information
                prompt = self._create_paper_prompt(paper)
                
                # Generate summary using OpenAI
                summary = self._generate_summary_with_retry(prompt)
                
                if summary:
                    summaries.append((paper, summary))
                    logger.info(f"Generated summary for paper: {paper.get('title', 'Unknown')}")
                
            except Exception as e:
                logger.error(f"Error summarizing paper: {str(e)}")
                # Create a basic summary from available information
                summary = self._create_basic_summary(paper)
                summaries.append((paper, summary))
                
        return summaries

    def summarize_projects(self, projects: List[Dict]) -> List[Tuple[Dict, str]]:
        """
        Generate concise summaries of GitHub projects.

        Args:
            projects (List[Dict]): List of project information dictionaries

        Returns:
            List[Tuple[Dict, str]]: List of (project_info, summary) tuples
        """
        summaries = []
        for project in projects:
            try:
                # Create a prompt that focuses on implementation details
                prompt = self._create_project_prompt(project)
                
                # Generate summary using OpenAI
                summary = self._generate_summary_with_retry(prompt)
                
                if summary:
                    summaries.append((project, summary))
                    logger.info(f"Generated summary for project: {project.get('full_name', 'Unknown')}")
                
            except Exception as e:
                logger.error(f"Error summarizing project: {str(e)}")
                # Create a basic summary from available information
                summary = self._create_basic_project_summary(project)
                summaries.append((project, summary))
                
        return summaries

    def _create_basic_summary(self, paper: Dict) -> str:
        """Create a basic summary when AI generation fails."""
        title = paper.get('title', 'Unknown')
        authors = ', '.join(paper.get('authors', []))
        year = paper.get('year', 'Unknown')
        abstract = paper.get('abstract', '')
        
        return f"""Title: {title}
Authors: {authors}
Year: {year}
Abstract: {abstract[:200]}..."""

    def _create_basic_project_summary(self, project: Dict) -> str:
        """Create a basic summary when AI generation fails."""
        name = project.get('full_name', 'Unknown')
        desc = project.get('description', '')
        topics = ', '.join(project.get('topics', []))
        
        return f"""Repository: {name}
Description: {desc}
Topics: {topics}"""

    def _create_paper_prompt(self, paper: Dict) -> str:
        """Create a prompt for paper summarization."""
        return f"""Analyze this research paper and provide a concise summary:

Title: {paper.get('title', 'Unknown')}
Authors: {', '.join(paper.get('authors', []))}
Year: {paper.get('year', 'Unknown')}
Abstract: {paper.get('abstract', '')}

Key points to include:
1. Main contribution
2. Key findings
3. Why it matters

Keep it brief and focused."""

    def _create_project_prompt(self, project: Dict) -> str:
        """Create a prompt for project summarization."""
        return f"""Analyze this GitHub project and provide a concise summary:

Repository: {project.get('full_name', 'Unknown')}
Description: {project.get('description', '')}
Topics: {', '.join(project.get('topics', []))}

Focus on:
1. Main purpose
2. Key features
3. Why it's useful

Keep it brief and focused."""

    def _generate_summary_with_retry(self, prompt: str, max_retries: int = 3) -> str:
        """
        Generate a summary with retry logic for rate limits.

        Args:
            prompt (str): The prompt for generating the summary
            max_retries (int): Maximum number of retry attempts

        Returns:
            str: Generated summary or basic information if failed
        """
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a research assistant. Provide brief, technical summaries."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150,  # Reduced token count
                    temperature=0.3   # More focused responses
                )
                return response.choices[0].message.content.strip()
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if "rate limit" in str(e).lower():
                    if attempt < max_retries - 1:
                        wait_time = self.retry_delay * (attempt + 1)
                        logger.info(f"Rate limit hit. Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                    continue
                return None
                
        return None
