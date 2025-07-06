import pytest
from datetime import date, datetime, timedelta
from app.services.github_score_service import GithubScoreService
from app.models.repo_summary import RepoSummary
from app.models.repo_search_result import RepoSearchResult
from pydantic import HttpUrl

@pytest.mark.asyncio
async def test_get_and_score_repositories():
    mock_repo = RepoSummary(
        id=1,
        language="python",
        name="test-repo",
        stargazers_count=100,
        forks_count=50,
        updated_at=datetime.now() - timedelta(days=10),
        html_url=HttpUrl("https://github.com/test/test-repo")
    )

    from app.clients.github_client import GitHubClient

    class MockGitHubClient(GitHubClient):
        async def search_repositories(
            self,
            language: str,
            created_date: date,
            page: int = 1,
            per_page: int = 100
        ) -> RepoSearchResult:

            mock_repo = RepoSummary(
                id=1,
                language="python",
                name="test-repo",
                stargazers_count=100,
                forks_count=50,
                updated_at=datetime.now() - timedelta(days=10),
                html_url= HttpUrl("https://github.com/test/test-repo")
            )

            return RepoSearchResult(
                total_count=1,
                items=[mock_repo],
                incomplete_results=False
            )

    service = GithubScoreService()
    service.github_client = MockGitHubClient()

    scored_repos = await service.get_and_score_repositories("python", date(2021, 1, 1), 10, 100)

    assert len(scored_repos) == 1
    scored = scored_repos[0]
    assert scored.name == "test-repo"
    assert scored.stars_count == 100
    assert scored.forks_count == 50
    assert isinstance(scored.score, float)
    assert 0 <= scored.score <= 100
    assert str(scored.url) == "https://github.com/test/test-repo"


def test_sort_by_git_scores():
    service = GithubScoreService()

    repo1 = RepoSummary(
        id=1,
        language="python",
        name="repo1",
        stargazers_count=200,
        forks_count=30,
        updated_at=datetime.now() - timedelta(days=5),
        html_url=HttpUrl("https://github.com/test/repo1")
    )

    repo2 = RepoSummary(
        id=2,
        language="python",
        name="repo2",
        stargazers_count=100,
        forks_count=80,
        updated_at=datetime.now() - timedelta(days=20),
        html_url=HttpUrl("https://github.com/test/repo2")
    )

    sorted_repos = service.sort_by_git_scores([repo1, repo2])
    assert len(sorted_repos) == 2
    assert sorted_repos[0].score >= sorted_repos[1].score


def test_calculate_score():
    service = GithubScoreService()

    repo = RepoSummary(
        id=1,
        language="python",
        name="repo-score-test",
        stargazers_count=100,
        forks_count=50,
        updated_at=datetime.now() - timedelta(days=15),
        html_url=HttpUrl("https://github.com/test/score-repo")
    )

    score = service.calculate_score(repo)
    assert isinstance(score, float)
    assert 0 <= score <= 100