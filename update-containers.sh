#!/usr/bin/env bash
# ============================================================
# update-containers.sh
# Автообновление backend/frontend с Docker Hub.
#
# Что менять под свой сервер:
#   COMPOSE_FILE   — путь к docker-compose.yml
#   COMPOSE_DIR    — каталог проекта (где лежит compose и .env)
#   BACKEND_IMAGE  — образ backend на Docker Hub
#   FRONTEND_IMAGE — образ frontend на Docker Hub
#   LOG_FILE       — куда писать лог
# ============================================================

set -euo pipefail

# --- Настройки (правьте здесь) ---
COMPOSE_DIR="${COMPOSE_DIR:-/opt/projects/target}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yml}"
BACKEND_IMAGE="${BACKEND_IMAGE:-andreiblagov/backend:latest}"
FRONTEND_IMAGE="${FRONTEND_IMAGE:-andreiblagov/frontend:latest}"
LOG_FILE="${LOG_FILE:-/home/andrei/logs/target-update.log}"
LOCK_FILE="${LOCK_FILE:-/tmp/update-target-containers.lock}"

# docker compose (plugin) или docker-compose (legacy)
if docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD=(docker compose)
else
  COMPOSE_CMD=(docker-compose)
fi

timestamp() { date '+%Y-%m-%d %H:%M:%S'; }

log() {
  local msg="[$(timestamp)] $*"
  mkdir -p "$(dirname "$LOG_FILE")"
  echo "$msg" | tee -a "$LOG_FILE"
}

# --- Шаг 0: не допускаем параллельный запуск из cron ---
exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  log "Skip: другой update уже выполняется"
  exit 0
fi

# --- Шаг 1: перейти в каталог проекта ---
cd "$COMPOSE_DIR"

# --- Шаг 2: получить локальный ID образа (или "missing", если образа ещё нет) ---
image_id() {
  local image="$1"
  docker image inspect --format='{{.Id}}' "$image" 2>/dev/null || echo "missing"
}

log "=== Проверка обновлений на Docker Hub ==="
log "Каталог: $COMPOSE_DIR"
log "Compose:  $COMPOSE_FILE"
log "Образы:   $BACKEND_IMAGE , $FRONTEND_IMAGE"

BACKEND_BEFORE="$(image_id "$BACKEND_IMAGE")"
FRONTEND_BEFORE="$(image_id "$FRONTEND_IMAGE")"

# --- Шаг 3: скачать свежие теги с Docker Hub ---
log "Pull: $BACKEND_IMAGE"
docker pull "$BACKEND_IMAGE"

log "Pull: $FRONTEND_IMAGE"
docker pull "$FRONTEND_IMAGE"

BACKEND_AFTER="$(image_id "$BACKEND_IMAGE")"
FRONTEND_AFTER="$(image_id "$FRONTEND_IMAGE")"

# --- Шаг 4: сравнить ID до/после pull ---
BACKEND_UPDATED=0
FRONTEND_UPDATED=0

if [[ "$BACKEND_BEFORE" != "$BACKEND_AFTER" ]]; then
  BACKEND_UPDATED=1
  log "backend: НАЙДЕНО обновление ($BACKEND_BEFORE → $BACKEND_AFTER)"
else
  log "backend: без изменений ($BACKEND_AFTER)"
fi

if [[ "$FRONTEND_BEFORE" != "$FRONTEND_AFTER" ]]; then
  FRONTEND_UPDATED=1
  log "frontend: НАЙДЕНО обновление ($FRONTEND_BEFORE → $FRONTEND_AFTER)"
else
  log "frontend: без изменений ($FRONTEND_AFTER)"
fi

# --- Шаг 5: если есть новые версии — пересоздать контейнеры через compose ---
if [[ "$BACKEND_UPDATED" -eq 1 || "$FRONTEND_UPDATED" -eq 1 ]]; then
  log "Останавливаем текущие контейнеры и поднимаем новые версии..."
  # down убирает старые контейнеры; up -d поднимает в фоне из актуальных образов
  "${COMPOSE_CMD[@]}" -f "$COMPOSE_FILE" down
  "${COMPOSE_CMD[@]}" -f "$COMPOSE_FILE" up -d
  log "Контейнеры перезапущены (docker compose up -d)."
else
  log "Новых версий нет — контейнеры оставлены без изменений."
  # На всякий случай убеждаемся, что сервисы запущены
  "${COMPOSE_CMD[@]}" -f "$COMPOSE_FILE" up -d
fi

# --- Шаг 6: итоговый отчёт ---
log "=== Итог ==="
if [[ "$BACKEND_UPDATED" -eq 1 ]]; then
  log "Обновлён:  target-backend ($BACKEND_IMAGE)"
else
  log "Без изменений: target-backend ($BACKEND_IMAGE)"
fi
if [[ "$FRONTEND_UPDATED" -eq 1 ]]; then
  log "Обновлён:  target-frontend ($FRONTEND_IMAGE)"
else
  log "Без изменений: target-frontend ($FRONTEND_IMAGE)"
fi
log "=== Готово ==="
