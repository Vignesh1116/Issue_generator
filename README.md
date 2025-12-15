Issue Box Integration – Quiz Application

This project adds an in-app Issue Box to a Quiz Application, allowing users to report problems directly from the UI.
Submitted issues are automatically created in a GitHub repository using the GitHub REST API.
 Features

Floating Issue Box UI (bottom-right corner)

Secure FastAPI backend

Automatic GitHub Issue creation

Deployed frontend and backend

Production-like feedback workflow

 Tech Stack

Frontend: React (Deployed on Vercel)

Backend: FastAPI (Deployed on Render)

API: GitHub REST API

 Environment Variables

For security reasons, the .env file has been intentionally removed from this repository.

To run this project locally or use your own GitHub repository, you must create a .env file inside the backend directory and add the following variables:

GITHUB_OWNER=your_github_username
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPO=your_repository_name

 Variable Explanation

GITHUB_OWNER – Your GitHub username or organization name

GITHUB_TOKEN – A GitHub Personal Access Token with repo permissions

GITHUB_REPO – The repository where issues should be created
