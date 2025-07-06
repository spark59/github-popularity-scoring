# Redcare GitHub Popularity Scoring Service

This service fetches repositories from GitHub, scores them based on popularity metrics (stars, forks, recency), and returns a sorted list in descending order.

## Features

- Fetches repositories using the GitHub API
- Applies rate limiting and retry logic
- Scores repositories based on stars, forks, and last update
- Asynchronous and production-ready

## Requirements

- Python 3.9+
- [pip](https://pip.pypa.io/en/stable/)

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/spark59/github-popularity-scoring.git
   cd redcare-github-popularity-scoring-service
   ```
2. **Install dependencies:**
   ```sh
   make install
   make install-dev
   ```
3. **Set environment variables:**
   Create a `.env` file in the root directory with the following content:
   ```env
   GITHUB_TOKEN=your_github_token
    ```
## **Run the service:**
    ```sh
    make run
    ```
## Testing
    To run tests, use:
    ```sh
    make test
    ```

## Usage
You can use the service by sending a GET request to the `/search` endpoint with the following
query parameters:
- `language`: The programming language to filter repositories (e.g., `python`, `javascript`)
- `earliest_created_date`: The date from which to filter repositories (format: `YYYY-MM-DD`)
- `page`: The page number for pagination (default: `1`)
- `per_page`: The number of repositories per page (default: `100`)

Example request:
```sh
curl "http://localhost:8000/search?language=python&earliest_created_date=2023-01-01&page=1&per_page=10"
```