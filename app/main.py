from util.log_config import get_logger
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict, Union, Optional
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from util.summariser import summariser

app = FastAPI()

logger = get_logger(__name__)

# Mount static files (for UI)
app.mount("/static", StaticFiles(directory="static"), name="static")

class ConversationRequest(BaseModel):
    conversation: Union[str, List[Dict[str, str]]]
    max_n_character: Optional[int] = None
    min_n_character: Optional[int] = None

# Serve the UI (index.html)
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    return FileResponse("static/index.html")

# API endpoint to call Python function
@app.post("/summarise", response_class=JSONResponse)
async def summarise(req: ConversationRequest, request: Request = None):
    summary_result = summariser(req.conversation, req.max_n_character, req.min_n_character)
    
    client_host = request.client.host
    method = request.method
    url = request.url.path + ("?" + request.url.query if request.url.query else "")
    protocol = request.scope.get("http_version", "1.1")
    logger.info(f'"{method} {url} HTTP/{protocol}" - {client_host}')
    return JSONResponse(summary_result)
