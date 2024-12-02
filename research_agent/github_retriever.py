"""
GitHub Repository Retriever Module

This module provides functionality to search and analyze GitHub repositories
related to specific research topics. It uses the GitHub API to fetch repositories
and extract relevant information about their implementation details.
"""

from typing import List, Dict, Optional
from github import Github, Repository
from github.GithubException import RateLimitExceededException, GithubException
import logging
from datetime import datetime, timedelta
import time
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubRetriever:
    """A class to retrieve and analyze relevant GitHub repositories."""
    
    def __init__(self, github_token: str, max_results: int = 5):
        """
        Initialize the GitHub retriever.
        
        Args:
            github_token (str): GitHub API token for authentication
            max_results (int, optional): Maximum number of repositories to return. Defaults to 5.
        """
        self.github = Github(github_token)
        self.max_results = max_results
        self._rate_limit_handler = self._create_rate_limit_handler()
    
    def search(self, query: str) -> List[Dict]:
        """
        Search for relevant GitHub repositories based on the query.
        
        Args:
            query (str): Search query string
            
        Returns:
            List[Dict]: List of repository information dictionaries
        
        Raises:
            GithubException: If there's an error accessing the GitHub API
        """
        try:
            # Enhance search query with relevant topics
            enhanced_query = self._enhance_query(query)
            logger.info(f"Searching GitHub with enhanced query: {enhanced_query}")
            
            # Search repositories with enhanced query
            repos = self._search_repositories(enhanced_query)
            
            # Process and analyze repositories
            return self._process_repositories(repos)
            
        except RateLimitExceededException:
            logger.warning("GitHub API rate limit exceeded. Implementing exponential backoff...")
            return self._handle_rate_limit()
            
        except GithubException as e:
            logger.error(f"GitHub API error: {str(e)}")
            return []
    
    def _enhance_query(self, query: str) -> str:
        """
        Enhance the search query with relevant filters and topics.
        
        Args:
            query (str): Original search query
            
        Returns:
            str: Enhanced query string
        """
        # Add language filters for common research implementation languages
        languages = ["python", "pytorch", "tensorflow", "julia"]
        language_filter = " OR ".join(f"language:{lang}" for lang in languages)
        
        # Add topic filters for research-related repositories
        topics = ["machine-learning", "deep-learning", "research", "paper-implementation"]
        topic_filter = " OR ".join(f"topic:{topic}" for topic in topics)
        
        # Combine filters with original query
        enhanced_query = f"{query} ({language_filter}) ({topic_filter})"
        
        # Add quality filters
        enhanced_query += " stars:>50 fork:true"
        
        return enhanced_query
    
    def _search_repositories(self, query: str) -> List[Repository.Repository]:
        """
        Search GitHub repositories with pagination and sorting.
        
        Args:
            query (str): Enhanced search query
            
        Returns:
            List[Repository.Repository]: List of GitHub repository objects
        """
        repos = []
        for repo in self.github.search_repositories(
            query=query,
            sort="stars",
            order="desc"
        ):
            if len(repos) >= self.max_results:
                break
            repos.append(repo)
        return repos
    
    def _process_repositories(self, repos: List[Repository.Repository]) -> List[Dict]:
        """
        Process repository information and extract relevant details.
        
        Args:
            repos (List[Repository.Repository]): List of GitHub repository objects
            
        Returns:
            List[Dict]: Processed repository information
        """
        processed_repos = []
        for repo in repos:
            # Extract repository details
            repo_info = {
                'full_name': repo.full_name,
                'description': repo.description,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'url': repo.html_url,
                'created_at': repo.created_at.isoformat(),
                'updated_at': repo.updated_at.isoformat(),
                'language': repo.language,
                'topics': repo.get_topics(),
                'has_readme': self._has_readme(repo),
                'readme_content': self._get_readme_content(repo),
                'paper_references': self._extract_paper_references(repo)
            }
            processed_repos.append(repo_info)
        return processed_repos
    
    def _has_readme(self, repo: Repository.Repository) -> bool:
        """Check if repository has a README file."""
        try:
            repo.get_readme()
            return True
        except GithubException:
            return False
    
    def _get_readme_content(self, repo: Repository.Repository) -> Optional[str]:
        """Get README content if available."""
        try:
            readme = repo.get_readme()
            return readme.decoded_content.decode('utf-8')
        except GithubException:
            return None
    
    def _extract_paper_references(self, repo: Repository.Repository) -> List[str]:
        """Extract paper references from README and repository description."""
        readme_content = self._get_readme_content(repo)
        if not readme_content:
            return []
        
        # Look for arXiv links
        arxiv_pattern = r'arxiv\.org/abs/\d+\.\d+'
        arxiv_refs = re.findall(arxiv_pattern, readme_content)
        
        # Look for paper titles in quotes followed by year
        paper_pattern = r'"([^"]+)"\s*\(?\d{4}\)?'
        paper_refs = re.findall(paper_pattern, readme_content)
        
        return list(set(arxiv_refs + paper_refs))
    
    def _create_rate_limit_handler(self):
        """Create a generator for handling rate limits with exponential backoff."""
        wait_time = 1
        while True:
            rate_limit = self.github.get_rate_limit()
            if rate_limit.search.remaining > 0:
                wait_time = 1
                yield
            else:
                logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                wait_time *= 2
                yield
    
    def _handle_rate_limit(self):
        """Handle rate limit exception with exponential backoff."""
        next(self._rate_limit_handler)
        return self.search(query)  # Retry the search
