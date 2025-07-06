import pytest
import respx
from httpx import Response
from datetime import date
from app.clients.github_client import GitHubClient
from app.core.exceptions import GitHubAPIError

@pytest.mark.asyncio
@respx.mock
async def test_search_repositories_success():
    fake_response = {
        "total_count": 1,
        "incomplete_results": False,
        "items": [
            {   
                "id": "12345",
                "language": "python",
                "name": "example-repo",
                "html_url": "https://github.com/user/example-repo",
                "description": "A test repo",
                "stargazers_count": 123,
                "forks_count": 10,
                "updated_at": "2023-01-01T00:00:00Z"
            }
        ]
    }

    route = respx.get("https://api.github.com/search/repositories").mock(
        return_value=Response(200, json=fake_response)
    )

    client = GitHubClient()
    result = await client.search_repositories(language="python", created_date=date(2023, 1, 1))

    assert result.total_count == 1
    assert len(result.items) == 1
    assert result.items[0].name == "example-repo"
    assert route.called

@pytest.mark.asyncio
@respx.mock
async def test_search_repositories_invalid_query_raises():
    route = respx.get("https://api.github.com/search/repositories").mock(
        return_value=Response(422, json={"message": "Validation Failed"})
    )

    client = GitHubClient()
    
    with pytest.raises(GitHubAPIError) as exc_info:
        await client.search_repositories(language="bad!", created_date=date(2023, 1, 1))

    assert exc_info.value.status_code == 422
    assert "Validation Failed" in str(exc_info.value)

@pytest.mark.asyncio
@respx.mock
async def test_search_repositories_retries_on_5xx():
    call_count = 0

    def handler(request):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            return Response(500, json={"message": "Server Error"})
        return Response(200, json={
            "total_count": 0,
            "incomplete_results": False,
            "items": []
        })

    respx.get("https://api.github.com/search/repositories").mock(side_effect=handler)

    client = GitHubClient()
    result = await client.search_repositories(language="python", created_date=date(2023, 1, 1))

    assert result.total_count == 0
    assert call_count == 3