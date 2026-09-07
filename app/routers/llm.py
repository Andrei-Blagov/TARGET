from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.analyzer import SiteFetchError
from app.services.analyzer import analyze_site as run_site_analysis
from app.services.llm_client import LLMClient

router = APIRouter(tags=["LLM"])
client = LLMClient()


class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    response: str


class ChatWithSystemRequest(BaseModel):
    system_prompt: str
    user_prompt: str


class ChatJsonRequest(BaseModel):
    system_prompt: str
    user_prompt: str
    jsonStandard: str = ""


class ChatJsonResponse(BaseModel):
    data: dict[str, Any]


class AnalyzeRequest(BaseModel):
    url: str


@router.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest) -> ChatResponse:
    try:
        return ChatResponse(response=client.chat(body.prompt))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/chat-with-system", response_model=ChatResponse)
def chat_with_system(body: ChatWithSystemRequest) -> ChatResponse:
    try:
        return ChatResponse(
            response=client.chat_with_system(body.system_prompt, body.user_prompt)
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/chat-json", response_model=ChatJsonResponse)
def chat_json(body: ChatJsonRequest) -> ChatJsonResponse:
    try:
        result = client.chat_json(
            body.system_prompt,
            body.user_prompt,
            json_standard=body.jsonStandard,
        )
        return ChatJsonResponse(data=result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/analyze-site")
async def analyze_site(request: AnalyzeRequest) -> dict:
    try:
        return run_site_analysis(request.url, llm=client)
    except SiteFetchError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
