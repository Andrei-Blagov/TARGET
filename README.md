# TARGET AI — анализ сайтов для таргетированной рекламы

<p align="center">
  <strong>Вставьте URL — получите структурированный маркетинговый разбор сайта, инсайты о целевой аудитории и готовые идеи рекламных постов.</strong>
</p>

<p align="center">
  <a href="https://github.com/Andrei-Blagov/TARGET">Repository</a>
  ·
  <a href="http://localhost:8000/docs">API Docs</a>
</p>

---

## О проекте

**TARGET AI** — full-stack приложение, которое превращает содержимое сайта в практический бриф для рекламной кампании. Система загружает HTML по переданному URL, извлекает текстовый контент, с помощью LLM строит индивидуальный план исследования, выполняет серию промежуточных запросов и собирает результаты в единый JSON-отчёт.

Проект демонстрирует прикладное использование LLM в продуктовой задаче: от сбора и нормализации внешних данных до многошагового reasoning pipeline и отображения результата в удобном веб-интерфейсе.

### Что получает пользователь

- краткое позиционирование и анализ сайта;
- предполагаемые сегменты целевой аудитории и рекламные инсайты;
- автоматически сформированный план анализа;
- промежуточные результаты каждого шага;
- инструкцию по подготовке рекламных публикаций;
- три готовых примера рекламных постов;
- исходный извлечённый текст сайта для проверки контекста.

## Демонстрационный сценарий

```text
URL сайта
   │
   ▼
Загрузка HTML через httpx
   │
   ▼
Очистка контента BeautifulSoup
   │
   ▼
LLM формирует 5–6 шагов исследования
   │
   ▼
Отдельный LLM-запрос для каждого шага
   │
   ▼
LLM собирает итоговый структурированный JSON
   │
   ▼
Vue-интерфейс показывает план, детали и финальные карточки
```

## Основные возможности

### AI-анализ сайта

`POST /llm/analyze-site` запускает полный pipeline:

1. принимает URL сайта;
2. следует редиректам и скачивает страницу с timeout 30 секунд;
3. удаляет `script`, `style`, `noscript` и `svg` перед извлечением текста;
4. нормализует пробелы и ограничивает контекст первичной страницы 12 000 символами;
5. запрашивает у LLM план из 5–6 аналитических шагов в JSON-формате;
6. выполняет каждый шаг над содержимым сайта;
7. объединяет ответы в финальный JSON-отчёт.

### Универсальный LLM-клиент

`app/services/llm_client.py` инкапсулирует работу с OpenAI-compatible API и поддерживает:

- обычный chat-запрос;
- запрос с явным system prompt;
- JSON mode с дополнительным описанием ожидаемого формата;
- настраиваемый `BASE_URL`, поэтому клиент можно подключить не только к OpenAI API.

### Интерфейс результата

Vue-приложение показывает результат по уровням:

- URL проанализированного сайта;
- последовательность шагов исследования;
- раскрывающиеся промежуточные результаты;
- финальный анализ в динамических карточках;
- отдельное отображение массива примеров рекламных постов;
- loader и понятные сообщения об ошибках для долгих LLM-запросов.

## Технологический стек

### Backend

- **Python 3.11**
- **FastAPI** — HTTP API, Pydantic-модели и OpenAPI-документация
- **Uvicorn** — ASGI-сервер
- **OpenAI Python SDK** — доступ к OpenAI-compatible API
- **httpx** — загрузка внешних сайтов
- **BeautifulSoup4** — очистка и извлечение текста из HTML
- **python-dotenv** — конфигурация через `.env`

### Frontend

- **Vue 3** с `<script setup>`
- **Vite** — dev server и production build
- **Axios** — HTTP-клиент
- **Tailwind CSS 4** — utility-first стилизация
- **Motion for Vue** — анимации интерфейса и состояний загрузки

### Deployment

- Docker Compose для development и production-сценариев
- Multi-stage Docker image для frontend
- Nginx для раздачи SPA и reverse proxy к backend
- Docker Hub для публикации образов
- Bash-скрипты для сборки, публикации и автоматического обновления контейнеров через cron

## Архитектура проекта

```text
.
├── app/
│   ├── main.py                    # FastAPI-приложение, CORS, health endpoints
│   ├── routers/
│   │   └── llm.py                 # HTTP-контракты и LLM endpoints
│   └── services/
│       ├── analyzer.py            # загрузка сайта и многошаговый анализ
│       └── llm_client.py          # OpenAI-compatible LLM client
│
├── frontend/
│   ├── src/
│   │   ├── App.vue                # основной экран и состояние запроса
│   │   ├── api.js                 # frontend API layer
│   │   ├── components/
│   │   │   ├── AnalysisResult.vue # шаги и промежуточные результаты
│   │   │   ├── FinalAnalysisCards.vue
│   │   │   └── Loader.vue
│   │   └── style.css              # Tailwind theme и базовые стили
│   ├── Dockerfile                  # production: Vite build → Nginx
│   ├── Dockerfile.dev              # development image с Vite HMR
│   └── nginx.conf                  # SPA fallback и proxy /llm → backend
│
├── Backend-Dockerfile              # production image для FastAPI
├── docker-compose.dev.yml          # разработка с hot reload
├── docker-compose.yml              # запуск готовых образов
├── final_analyse_example.json      # пример структуры результата анализа
├── push-images.sh                  # build + push образов в Docker Hub
├── update-containers.sh            # pull образов и безопасный restart
├── install-cron.sh                 # установка hourly cron-задачи
├── requirements.txt
└── .env.example
```

### Как проходит запрос

1. `frontend/src/api.js` отправляет URL на `/llm/analyze-site`.
2. FastAPI router `app/routers/llm.py` валидирует тело запроса через `AnalyzeRequest`.
3. `analyzer.py` получает страницу, очищает HTML и передаёт текст в `LLMClient`.
4. LLM сначала возвращает план, затем результаты отдельных шагов, затем финальный отчёт.
5. Backend возвращает единый объект с полями `url`, `steps`, `intermediate_results` и `final_analysis`.
6. Vue-компоненты преобразуют ответ в интерактивный, читаемый отчёт.

## Быстрый старт через Docker

### 1. Подготовить конфигурацию

```bash
cp .env.example .env
```

Заполните `.env`:

```dotenv
BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=your-api-key
# Опционально: BOT_TOKEN=your-telegram-token
```

> `.env` содержит секреты и не должен коммититься в репозиторий.

### 2. Запустить development-окружение

```bash
docker compose -f docker-compose.dev.yml up --build
```

После запуска:

- Frontend: <http://localhost:5173>
- Backend API: <http://localhost:8000>
- Swagger UI: <http://localhost:8000/docs>
- Health check: <http://localhost:8000/health>

Development compose монтирует `app/` и `frontend/` как volumes, поэтому изменения в коде доступны без пересборки образов.

## Запуск без Docker

### Backend

```bash
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

В отдельном терминале:

```bash
cd frontend
npm install
npm run dev
```

Для frontend можно задать адрес backend через переменную Vite:

```bash
VITE_API_URL=http://localhost:8000 npm run dev
```

В production `VITE_API_URL` остаётся пустым: браузер использует тот же origin, а Nginx проксирует API-запросы в контейнер `backend`.

## Production через Docker Compose

Production compose запускает опубликованные образы:

- `andreiblagov/backend:latest`
- `andreiblagov/frontend:latest`

```bash
cp .env.example .env
# заполните OPENAI_API_KEY и остальные параметры

docker compose up -d
```

Порты по умолчанию:

- backend API: `8000`
- frontend через Nginx: `8080`

### Сборка и публикация образов

Перед первым запуском выполните `docker login`:

```bash
./push-images.sh
```

Скрипт собирает backend из `Backend-Dockerfile`, frontend — из `frontend/Dockerfile`, затем публикует оба образа в Docker Hub.

### Автоматическое обновление на сервере

```bash
chmod +x update-containers.sh install-cron.sh
./install-cron.sh
```

По умолчанию обновление запускается каждый час в `05` минут. `update-containers.sh`:

1. блокирует параллельные запуски через `flock`;
2. делает `docker pull` для backend и frontend;
3. сравнивает ID образов до и после загрузки;
4. перезапускает Compose только при наличии изменений;
5. пишет результат в `/home/andrei/logs/target-update.log`.

Пути, образы и расписание можно переопределить переменными окружения `COMPOSE_DIR`, `COMPOSE_FILE`, `BACKEND_IMAGE`, `FRONTEND_IMAGE`, `LOG_FILE`, `SCRIPT_PATH` и `CRON_SCHEDULE`.

## API

Все LLM-маршруты находятся под префиксом `/llm`.

| Метод | Endpoint | Назначение |
|---|---|---|
| `GET` | `/` | Проверка, что API запущен |
| `GET` | `/health` | Health check |
| `POST` | `/llm/chat` | Простой запрос к LLM |
| `POST` | `/llm/chat-with-system` | Запрос с system prompt |
| `POST` | `/llm/chat-json` | Запрос с JSON-ответом |
| `POST` | `/llm/analyze-site` | Полный анализ сайта |

### Пример полного анализа

```bash
curl -X POST http://localhost:8000/llm/analyze-site \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

Ответ имеет следующую структуру:

```json
{
  "url": "https://example.com",
  "steps": ["..."],
  "intermediate_results": [
    {
      "step": "...",
      "result": "..."
    }
  ],
  "final_analysis": {
    "brief_analysis": "...",
    "ad_post_instruction": "...",
    "post_examples": ["...", "...", "..."],
    "site_text": "..."
  }
}
```

Полная интерактивная схема доступна в Swagger UI по адресу `/docs` после запуска backend.

## Конфигурация

| Переменная | Обязательность | Описание |
|---|---:|---|
| `BASE_URL` | Да | OpenAI-compatible API endpoint |
| `OPENAI_API_KEY` | Да | Ключ доступа к LLM-провайдеру |
| `BOT_TOKEN` | Нет | Зарезервированный параметр для интеграции с Telegram |
| `VITE_API_URL` | Нет | Адрес backend для frontend в development |

По умолчанию используется модель `gpt-4o-mini`, заданная в `LLMClient`.

## Обработка ошибок и ограничения

- Ошибки загр��зки или парсинга сайта преобразуются в HTTP `400`.
- Ошибки LLM и внутренние ошибки API возвращаются как HTTP `500`.
- Для внешнего сайта установлен timeout загрузки 30 секунд.
- Из исходного HTML удаляются технические теги, не содержащие полезного контента.
- Текст страницы ограничивается 12 000 символами, чтобы контролировать размер контекста.
- Frontend ожидает длительный ответ и использует timeout 300 секунд.
- Nginx настроен на `proxy_read_timeout` и `proxy_send_timeout` 300 секунд.

Для публичного production-развёртывания рекомендуется дополнительно ограничить CORS конкретными origin, добавить rate limiting, SSRF-защиту для URL и аутентификацию API.

## Пример результата

В репозитории есть [final_analyse_example.json](./final_analyse_example.json), демонстрирующий фактический формат многошагового результата: план, промежуточные ответы и итоговые рекламные рекомендации.

## Текущее состояние проекта

### Реализовано

- [x] FastAPI backend с OpenAPI-документацией
- [x] OpenAI-compatible LLM client
- [x] JSON mode для структурированных ответов
- [x] Многошаговый анализ сайта
- [x] Vue-интерфейс с loader, анимациями и обработкой ошибок
- [x] Development и production Docker Compose
- [x] Production frontend image на базе Nginx
- [x] Публикация образов в Docker Hub
- [x] Автоматическое обновление контейнеров через cron

### Возможные направления развития

- потоковая выдача прогресса через SSE или WebSocket;
- очередь фоновых задач для длинных анализов;
- сохранение истории анализов и пользовательских проектов;
- авторизация и разграничение доступа;
- проверка URL и SSRF-защита перед server-side fetch;
- rate limiting и observability для production-нагрузки;
- автоматические тесты для analyzer, API-контрактов и LLM-моков;
- поддержка sitemap и анализа нескольких страниц сайта.

## Лицензия

Лицензия в репозитории пока не указана. Перед публичным использованием и переиспользованием кода определите подходящую лицензию.
