from typing import List
from app.models.repo_summary import RepoSummary
from pydantic import BaseModel

class RepoSearchResult(BaseModel):
    total_count: int
    items: List[RepoSummary]
    incomplete_results: bool