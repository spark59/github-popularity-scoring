import pytest
from datetime import datetime
from httpx import AsyncClient
from fastapi import FastAPI
from pydantic import HttpUrl

from app.api.routes import router
from app.services.github_score_service import GithubScoreService
from app.models.scored_repo_summary import ScoredRepoSummary

app = FastAPI()
app.include_router(router)

@pytest.mark.asyncio
async def test_search_route_success():
    class MockService:
        async def get_and_score_repositories(self, language, created_date, page, per_page):
            assert language == "python"
            assert page == 1
            assert per_page == 50
            return [
                ScoredRepoSummary(
                    name="python",
                    stars_count=100,
                    forks_count=50,
                    updated_at=datetime.fromisoformat("2024-01-01T00:00:00"),
                    score=0.0,
                    url=HttpUrl("https://github.com/example/repo")
                )
            ]

    app.dependency_overrides[GithubScoreService] = lambda: MockService()

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/search",
            params={"language": "python", "earliest_created_date": "2024-01-01", "page": 1, "per_page": 50}
        )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "python"

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_search_route_invalid_page():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/search",
            params={"language": "python", "earliest_created_date": "2024-01-01", "page": 0}
        )
    assert response.status_code == 422
    assert "page" in response.text

@pytest.mark.asyncio
async def test_search_route_invalid_per_page():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/search",
            params={"language": "python", "earliest_created_date": "2024-01-01", "per_page": 101}
        )
    assert response.status_code == 422
    assert "per_page" in response.text