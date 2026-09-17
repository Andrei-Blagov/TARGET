# TARGET — LLM Site Analyzer

Веб-приложение для анализа сайтов и генерации идей для таргетированной рекламы.
Стек: **FastAPI + Vue 3 (Vite) + Docker**.

## Возможности

- Чат с LLM (`/llm/chat`, `/llm/chat-with-system`, `/llm/chat-json`)
- Анализ сайта по URL (`POST /llm/analyze-site`): скачивание HTML → план шагов → промежуточный анализ → итоговый отчёт и примеры постов
- Frontend с лоадером и анимированным отображением результата

## Структура

```
app/                  # FastAPI backend
  main.py
  routers/llm.py
  services/llm_client.py
  services/analyzer.py
frontend/             # Vue 3 + Vite + Tailwind
Backend-Dockerfile    # production-образ backend
docker-compose.yml    # production (образы с Docker Hub)
docker-compose.dev.yml# локальная разработка
update-containers.sh  # автообновление с Docker Hub
install-cron.sh       # hourly cron
push-images.sh        # сборка и push в Docker Hub
```

## Быстрый старт (локально)

1. Скопируйте `.env.example` → `.env` и заполните:

```env
BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=sk-...
```

2. Запуск в режиме разработки:

```bash
docker compose -f docker-compose.dev.yml up --build
```

- Frontend: http://localhost:5173  
- Backend / docs: http://localhost:8000/docs  

Без Docker:

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

cd frontend && npm install && npm run dev
```

## Production (Docker Hub)

Образы:

- `andreiblagov/backend:latest`
- `andreiblagov/frontend:latest`

Сборка и публикация:

```bash
docker login
./push-images.sh
```

На сервере:

```bash
# каталог по умолчанию: /opt/projects/target
docker compose up -d
chmod +x update-containers.sh install-cron.sh
./install-cron.sh   # проверка Hub каждый час
```

Автообновление (`update-containers.sh`):

1. `docker pull` backend/frontend  
2. Сравнение ID образов  
3. При изменениях — `docker compose down && up -d`  
4. Лог: какие сервисы обновлены / без изменений  

## API

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/` | Статус API |
| GET | `/health` | Health check |
| POST | `/llm/chat` | Простой чат |
| POST | `/llm/chat-with-system` | Чат с system prompt |
| POST | `/llm/chat-json` | JSON-ответ |
| POST | `/llm/analyze-site` | Полный анализ сайта |

Пример:

```bash
curl -X POST http://localhost:8000/llm/analyze-site \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

## Переменные окружения

| Переменная | Описание |
|------------|----------|
| `BASE_URL` | OpenAI-совместимый endpoint |
| `OPENAI_API_KEY` | API-ключ |
| `BOT_TOKEN` | (опционально) Telegram |

`.env` не коммитится — используйте `.env.example`.
