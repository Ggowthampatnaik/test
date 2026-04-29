from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import base64
import sys

load_dotenv()

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    if request.method == "POST":
        body = await request.body()
        print(f"REQUEST BODY: {body.decode()}", file=sys.stderr)
    response = await call_next(request)
    return response

GITHUB_TOKEN = "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"
USERNAME = "Ggowthampatnaik"

class LandingPage(BaseModel):
    repo_name: str
    html: str
    css: str
    js: str

def push_file(repo, path, content):
    url = f"https://api.github.com/repos/{USERNAME}/{repo}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    res = requests.get(url, headers=headers)
    sha = None
    if res.status_code == 200:
        sha = res.json()["sha"]

    encoded = base64.b64encode(content.encode()).decode()
    data = {"message": f"Update {path}", "content": encoded}
    if sha:
        data["sha"] = sha

    res = requests.put(url, json=data, headers=headers)
    if res.status_code not in [200, 201]:
        raise Exception(res.json())

@app.post("/upload")
def upload(page: LandingPage):
    try:
        repo_name = "ClaudeTest"
        push_file(repo_name, "index.html", page.html)
        push_file(repo_name, "styles.css", page.css)
        push_file(repo_name, "script.js", page.js)
        return {
            "status": "success",
            "repo_url": f"https://github.com/{USERNAME}/{repo_name}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
