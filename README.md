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
   git clone https://github.com/sangwookpark/redcare-github-popularity-scoring-service.git
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
4. **Run the service:**
    ```sh
    make run
    ```
## Testing
    To run tests, use:
    ```sh
    make test
    ```