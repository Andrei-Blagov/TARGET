import json
import os
from typing import Any, Optional

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMClient:
    """Клиент для общения с LLM через OpenAI-совместимый API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
    ) -> None:
        self.base_url = base_url or os.getenv("BASE_URL")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.system_prompt: Optional[str] = None
        self.max_tokens: Optional[int] = None

        if not self.base_url:
            raise ValueError("base_url is required (pass it or set BASE_URL in .env)")
        if not self.api_key:
            raise ValueError("api_key is required (pass it or set OPENAI_API_KEY in .env)")

        self._client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            default_headers={"Authorization": f"Bearer {self.api_key}"},
        )

    def _complete(
        self,
        messages: list[dict[str, str]],
        *,
        json_mode: bool = False,
    ) -> str:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }
        if self.max_tokens is not None:
            kwargs["max_tokens"] = self.max_tokens
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = self._client.chat.completions.create(**kwargs)
        return response.choices[0].message.content or ""

    def chat(self, prompt: str) -> str:
        """Простой запрос; при заданном self.system_prompt добавляет его в сообщения."""
        messages: list[dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})
        return self._complete(messages)

    def chat_with_system(self, system_prompt: str, user_prompt: str) -> str:
        """Запрос с явным системным промптом."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self._complete(messages)

    def chat_json(
        self,
        system_prompt: str,
        user_prompt: str,
        json_standard: str = "",
    ) -> dict:
        """Запрос со структурированным JSON-ответом, парсится в dict."""
        full_system = system_prompt
        if json_standard:
            full_system = (
                f"{system_prompt}\n\n"
                f"Ответ должен быть валидным JSON по стандарту:\n{json_standard}"
            )
        messages = [
            {"role": "system", "content": full_system},
            {"role": "user", "content": user_prompt},
        ]
        content = self._complete(messages, json_mode=True)
        return json.loads(content)


if __name__ == "__main__":
    client = LLMClient()
    client.max_tokens = 100
    client.system_prompt = "Отвечай кратко."

    print("=== chat ===")
    print(client.chat("Скажи одним словом: pong"))

    print("\n=== chat_with_system ===")
    print(client.chat_with_system("Отвечай одним словом.", "Сколько будет 2+2?"))

    print("\n=== chat_json ===")
    result = client.chat_json(
        "Верни только JSON.",
        "Столица Франции?",
        json_standard='{"answer": string, "confidence": number 0-1}',
    )
    print(result)
