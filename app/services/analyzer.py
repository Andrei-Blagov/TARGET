from __future__ import annotations

import re
from typing import Any

import httpx
from bs4 import BeautifulSoup

from app.services.llm_client import LLMClient

MAX_SITE_TEXT_CHARS = 12_000


class SiteFetchError(Exception):
    """Не удалось скачать или распарсить сайт."""


def fetch_site_text(url: str) -> str:
    try:
        response = httpx.get(
            url,
            follow_redirects=True,
            timeout=30.0,
            headers={"User-Agent": "Mozilla/5.0 (compatible; TargetAIBot/1.0)"},
        )
        response.raise_for_status()
    except Exception as exc:
        raise SiteFetchError(f"Не удалось скачать сайт: {exc}") from exc

    try:
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "noscript", "svg"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        text = re.sub(r"\s+", " ", text).strip()
    except Exception as exc:
        raise SiteFetchError(f"Не удалось распарсить HTML: {exc}") from exc

    if not text:
        raise SiteFetchError("На сайте не найден текстовый контент")

    return text[:MAX_SITE_TEXT_CHARS]


def _extract_steps(payload: dict[str, Any]) -> list[str]:
    for key in ("steps", "prompts", "шаги", "промпты"):
        value = payload.get(key)
        if isinstance(value, list) and value:
            return [str(item) for item in value]

    for value in payload.values():
        if isinstance(value, list) and value and all(isinstance(i, str) for i in value):
            return list(value)

    raise ValueError(f"Не удалось извлечь список шагов из ответа LLM: {payload}")


def analyze_site(url: str, llm: LLMClient | None = None) -> dict[str, Any]:
    client = llm or LLMClient()
    site_text = fetch_site_text(url)

    planning_system = (
        "Ты бот-анализатор сайтов. Вот текст сайта: "
        f"{site_text}. "
        "В ответе в формате JSON выдай список из 5-6 шагов (промптов), "
        "которые нужно выполнить для анализа этого сайта и выявления идей "
        "для таргетированной рекламы"
    )
    planning_result = client.chat_json(
        planning_system,
        "Сформируй план анализа.",
        json_standard='{"steps": ["строка-промпт", "..."]}',
    )
    steps = _extract_steps(planning_result)

    intermediate_results: list[dict[str, str]] = []
    for step in steps:
        answer = client.chat_with_system(step, site_text)
        intermediate_results.append({"step": step, "result": answer})

    answers_only = [item["result"] for item in intermediate_results]
    final_system = (
        "У тебя есть результаты промежуточного анализа: "
        f"{answers_only}. "
        "Объедини их и выдай итоговый анализ сайта. Ответ должен содержать: "
        "краткий анализ, инструкцию по созданию рекламных постов и три примера постов. "
        "Обязательно включи в анализ оригинальный текст сайта"
    )
    final_analysis = client.chat_json(
        final_system,
        f"Оригинальный текст сайта:\n{site_text}",
        json_standard=(
            '{"brief_analysis": "string", '
            '"ad_post_instruction": "string", '
            '"post_examples": ["string", "string", "string"], '
            '"site_text": "string"}'
        ),
    )

    return {
        "url": url,
        "steps": steps,
        "intermediate_results": intermediate_results,
        "final_analysis": final_analysis,
    }
