from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class RepoSummary(BaseModel):
    id: int
    name: str
    language: Optional[str]
    updated_at: datetime
    forks_count: int
    stargazers_count: int
    html_url: HttpUrl