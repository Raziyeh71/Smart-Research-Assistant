"""
Research Paper Summarizer Module

This module provides intelligent summarization of research papers and GitHub projects
using advanced NLP techniques to extract key findings and contributions.
"""

from typing import List, Dict, Tuple, Any
import openai
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Summarizer:
    """A class to generate intelligent summaries of research papers and projects."""

    def __init__(self):
        """Initialize the summarizer with OpenAI configuration."""
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("SUMMARY_MODEL", "gpt-3.5-turbo")

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
                summary = self._generate_summary(prompt)
                
                summaries.append((paper, summary))
                logger.info(f"Generated summary for paper: {paper.get('title', 'Unknown')}")
                
            except Exception as e:
                logger.error(f"Error summarizing paper: {str(e)}")
                continue
                
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
                summary = self._generate_summary(prompt)
                
                summaries.append((project, summary))
                logger.info(f"Generated summary for project: {project.get('full_name', 'Unknown')}")
                
            except Exception as e:
                logger.error(f"Error summarizing project: {str(e)}")
                continue
                
        return summaries

    def _create_paper_prompt(self, paper: Dict) -> str:
        """Create a prompt for paper summarization."""
        return f"""Analyze this research paper and provide a concise, informative summary:

Title: {paper.get('title', 'Unknown')}
Authors: {', '.join(paper.get('authors', []))}
Year: {paper.get('year', 'Unknown')}
Abstract: {paper.get('abstract', '')}

Please provide a brief summary that includes:
1. Main contribution and key findings
2. Methodology highlights
3. Practical implications
4. Why this paper is significant

Keep the summary concise and focused on what would be most relevant for a researcher."""

    def _create_project_prompt(self, project: Dict) -> str:
        """Create a prompt for project summarization."""
        return f"""Analyze this GitHub project and provide a concise, informative summary:

Repository: {project.get('full_name', 'Unknown')}
Description: {project.get('description', '')}
Topics: {', '.join(project.get('topics', []))}
README: {project.get('readme_content', '')}
Paper References: {', '.join(project.get('paper_references', []))}

Please provide a brief summary that includes:
1. Main purpose and features
2. Implementation approach
3. Related research papers or methods
4. Why this implementation is noteworthy

Focus on what would be most relevant for a researcher looking to implement related methods."""

    def _generate_summary(self, prompt: str) -> str:
        """
        Generate a summary using OpenAI's API.

        Args:
            prompt (str): The prompt for generating the summary

        Returns:
            str: Generated summary
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a research assistant specialized in summarizing academic papers and technical implementations. Provide concise, technical, and insightful summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=250,
                temperature=0.5,
                top_p=0.95
            )
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return "Error generating summary"
