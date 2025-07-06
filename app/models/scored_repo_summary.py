from pydantic import BaseModel, HttpUrl
from datetime import datetime

class ScoredRepoSummary(BaseModel):
    name: str
    stars_count: int
    forks_count: int
    updated_at: datetime
    score: float
    url: HttpUrl