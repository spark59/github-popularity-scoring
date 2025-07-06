from datetime import date
from app.clients.github_client import GitHubClient
from app.models.repo_summary import RepoSummary
from app.models.scored_repo_summary import ScoredRepoSummary
from typing import List
import heapq
import math

class GithubScoreService:
    def __init__(self):
        self.github_client = GitHubClient()

    async def get_and_score_repositories(self, language: str, created_time: date, page: int, per_page: int) -> List[ScoredRepoSummary]:        
        repo_search_result = await self.github_client.search_repositories(language, created_time, page, per_page)
        return self.sort_by_git_scores(repo_search_result.items)

    def sort_by_git_scores(self, repos: List[RepoSummary]) -> List[ScoredRepoSummary]:
        heap = []
        for idx, repo in enumerate(repos):
            score = self.calculate_score(repo)
            heapq.heappush(heap, (-score, idx, repo))

        scored_repos = []
        while heap:
            score, idx, repo = heapq.heappop(heap)
            scored_repos.append(
                ScoredRepoSummary(
                    name=repo.name,
                    stars_count=repo.stargazers_count,
                    forks_count=repo.forks_count,
                    updated_at=repo.updated_at,
                    score= -score,
                    url=repo.html_url
                )
            )
        return scored_repos

    def calculate_score(self, repo):
        stars = repo.stargazers_count
        forks = repo.forks_count
        days_since_update = (date.today() - repo.updated_at.date()).days

        stars_score = math.log1p(stars)
        forks_score = math.log1p(forks)

        recency_score = 1 / (1 + days_since_update / 30)

        score = (stars_score * 0.6) + (forks_score * 0.3) + (recency_score * 0.1)

        score = min(max(score * 10, 0), 100)
        return round(score, 2)
