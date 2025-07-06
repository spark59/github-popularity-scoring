from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import date
from app.services.github_score_service import GithubScoreService
from app.core.exceptions import GitHubAPIError

router = APIRouter()

@router.get("/search")
async def root(
    language: str,
    earliest_created_date: date,
    page: int = Query(1, ge=1, description="Page number (must be ≥ 1)"),
    per_page: int = Query(100, ge=1, le=100, description="Results per page (1-100)"),
    service: GithubScoreService = Depends(GithubScoreService)
):
    try:
        return await service.get_and_score_repositories(language, earliest_created_date, page, per_page)
    except GitHubAPIError as e:
        raise HTTPException(status_code=422, detail=str(e))