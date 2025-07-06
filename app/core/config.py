from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    github_token: str = ""
    github_api_url: str = "https://api.github.com/search/repositories"
    github_user_agent: str = "FastAPI-GitHub-Client"

    class Config:
        env_file = ".env"

settings = Settings()