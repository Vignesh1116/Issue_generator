from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import httpx
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request body
class IssueRequest(BaseModel):
    issueText: str
    pageUrl: str | None = None

# API Routes
@app.post("/create-issue")
async def create_issue(issue_request: IssueRequest):
    if not issue_request.issueText:
        raise HTTPException(status_code=400, detail="Issue text required")

    owner = os.getenv("GITHUB_OWNER")
    repo = os.getenv("GITHUB_REPO")
    token = os.getenv("GITHUB_TOKEN")

    if not all([owner, repo, token]):
        # Fallback to checking if the token is stored as GITHUB_URL (based on your current .env)
        # But ideally, you should update .env to match the expected keys
        raise HTTPException(status_code=500, detail="GitHub configuration missing in .env")

    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    
    payload = {
        "title": "Issue from Quiz App",
        "body": f"{issue_request.issueText}\n\nPage URL: {issue_request.pageUrl}"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return {"success": True, "issueUrl": data.get("html_url")}
        except httpx.HTTPStatusError as e:
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Failed to create issue",
                    "details": e.response.json() if e.response.content else str(e)
                }
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"error": "Failed to create issue", "details": str(e)}
            )

# Serve Static Files
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")

if os.path.exists(frontend_path):
    # Mount the frontend directory at the root
    # html=True allows serving index.html automatically at /
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    print(f"Warning: Frontend path {frontend_path} does not exist")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
