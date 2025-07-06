import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception
from app.core.config import settings
from app.models.repo_summary import RepoSummary
from datetime import date
from app.core.exceptions import GitHubAPIError
from app.models.repo_search_result import RepoSearchResult
from aiolimiter import AsyncLimiter

github_search_rate_limiter = AsyncLimiter(max_rate=30, time_period=60)

def is_5xx_error(exc):
    return isinstance(exc, httpx.HTTPStatusError) and 500 <= exc.response.status_code < 600

class GitHubClient:
    def __init__(self, token: str = settings.github_token, api_url: str = settings.github_api_url):
        self.token = token
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }
        self.timeout = httpx.Timeout(10.0, connect=5.0)
    
    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception(is_5xx_error)
    )
    async def search_repositories(self, language: str, created_date: date, page: int = 10, per_page: int = 100) -> RepoSearchResult:

        query = f"language:{language} created:>={created_date.isoformat()}"

        async with github_search_rate_limiter:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    self.api_url,
                    params={"q": query, "page": page, "per_page": per_page},
                    headers=self.headers
                )
                
                if response.status_code == 422:
                    try:
                        error_data = response.json()
                        message = (
                            error_data.get("errors", [{}])[0].get("message")
                            or error_data.get("message")
                            or "Invalid query to GitHub API."
                        )
                    except Exception:
                        message = "Invalid query to GitHub API."

                    raise GitHubAPIError(status_code=422, message=message)    

                response.raise_for_status()
                data = response.json()

                return RepoSearchResult(
                    total_count = data.get("total_count", 0),
                    items = [RepoSummary(**item) for item in data.get("items",[])],
                    incomplete_results = data.get("incomplete_results", False)
                )
