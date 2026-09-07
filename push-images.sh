#!/usr/bin/env bash
# ============================================================
# push-images.sh
# Сборка и публикация образов в Docker Hub (ник: andreiblagov)
#
# Перед запуском: docker login
# Меняйте DOCKERHUB_USER / теги при необходимости.
# ============================================================

set -euo pipefail

DOCKERHUB_USER="${DOCKERHUB_USER:-andreiblagov}"
BACKEND_TAG="${BACKEND_TAG:-latest}"
FRONTEND_TAG="${FRONTEND_TAG:-latest}"
BACKEND_IMAGE="${DOCKERHUB_USER}/backend:${BACKEND_TAG}"
FRONTEND_IMAGE="${DOCKERHUB_USER}/frontend:${FRONTEND_TAG}"

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "==> Build backend: $BACKEND_IMAGE"
docker build -f "$ROOT_DIR/Backend-Dockerfile" -t "$BACKEND_IMAGE" "$ROOT_DIR"

echo "==> Build frontend: $FRONTEND_IMAGE"
docker build -f "$ROOT_DIR/frontend/Dockerfile" -t "$FRONTEND_IMAGE" "$ROOT_DIR/frontend"

echo "==> Push $BACKEND_IMAGE"
docker push "$BACKEND_IMAGE"

echo "==> Push $FRONTEND_IMAGE"
docker push "$FRONTEND_IMAGE"

echo "Готово. На сервере: ./update-containers.sh или дождитесь cron."
