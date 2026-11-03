#!/usr/bin/env bash
set -e

cleanup() {
  trap '' EXIT
  (cd core_3pl/docker/local && docker compose down)
  (cd mock_storefront && docker compose down)
  kill 0
}
trap cleanup EXIT

(cd core_3pl/docker/local && docker compose up --build -d && echo "core docker is up !!!!")
(cd mock_storefront && docker compose up --build -d && echo "store docker is up !!!")

(cd core_3pl && python manage.py runserver 127.0.0.1:8000) &
(cd mock_storefront && python manage.py runserver 127.0.0.1:8080) &

wait