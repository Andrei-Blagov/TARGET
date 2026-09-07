#!/usr/bin/env bash
# ============================================================
# install-cron.sh
# Ставит hourly cron для update-containers.sh
#
# Меняйте:
#   SCRIPT_PATH — полный путь к update-containers.sh на сервере
#   CRON_SCHEDULE — расписание (по умолчанию каждый час)
# ============================================================

set -euo pipefail

# Путь к скрипту обновления на сервере
SCRIPT_PATH="${SCRIPT_PATH:-/opt/projects/target/update-containers.sh}"
# Каждый час, в минуту 5 (чтобы не совпасть с telegram-ботом на :00)
CRON_SCHEDULE="${CRON_SCHEDULE:-5 * * * *}"
CRON_MARKER="# target-update-containers"

if [[ ! -x "$SCRIPT_PATH" ]]; then
  chmod +x "$SCRIPT_PATH" || true
fi

if [[ ! -f "$SCRIPT_PATH" ]]; then
  echo "ERROR: не найден $SCRIPT_PATH"
  exit 1
fi

# Текущий crontab пользователя (или пустой)
CURRENT="$(crontab -l 2>/dev/null || true)"

# Удаляем старую запись с нашим маркером, если была
FILTERED="$(echo "$CURRENT" | grep -vF "$CRON_MARKER" || true)"

# Новая строка cron: запуск скрипта каждый час
NEW_LINE="${CRON_SCHEDULE} ${SCRIPT_PATH} ${CRON_MARKER}"

{
  echo "$FILTERED"
  echo "$NEW_LINE"
} | grep -v '^$' | crontab -

echo "Cron установлен:"
echo "  $NEW_LINE"
echo
echo "Проверка: crontab -l"
crontab -l
