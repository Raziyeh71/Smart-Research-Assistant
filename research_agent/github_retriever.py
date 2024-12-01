from github import Github
from typing import List, Dict

class GitHubRetriever:
    def __init__(self, github_token: str):
        self.github = Github(github_token)
        self.max_results = 5

    def search(self, query: str) -> List[Dict]:
        """
        Search for relevant GitHub repositories
        """
        repositories = []
        
        try:
            # Search repositories with query
            repos = self.github.search_repositories(
                query=query,
                sort="stars",
                order="desc"
            )

            # Get top repositories
            for repo in repos[:self.max_results]:
                repo_info = {
                    'full_name': repo.full_name,
                    'description': repo.description,
                    'stars': repo.stargazers_count,
                    'url': repo.html_url,
                    'topics': repo.get_topics(),
                    'last_updated': repo.updated_at.strftime("%Y-%m-%d"),
                    'readme': self.get_readme(repo)
                }
                repositories.append(repo_info)

        except Exception as e:
            print(f"Error searching GitHub: {str(e)}")

        return repositories

    def get_readme(self, repo) -> str:
        """
        Retrieve README content from repository
        """
        try:
            readme = repo.get_readme()
            return readme.decoded_content.decode('utf-8')
        except:
            return ""
