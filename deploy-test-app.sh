#!/usr/bin/env bash
set -Eeuo pipefail

APP_DIR="/home/ec2-user/test-app"
BRANCH="${1:-main}"

cd "$APP_DIR"

if [ ! -f ".env" ]; then
  echo "Missing $APP_DIR/.env"
  exit 1
fi

sudo chmod 600 .env

echo "Deploying branch: $BRANCH"

docker compose -f docker-compose.ec2.yml build api #build API docker image
docker compose -f docker-compose.ec2.yml run --rm api python  -m app.scripts.init_db #initialise/verify DB
docker compose -f docker-compose.ec2.yml up -d --remove-orphans api

echo "Waiting to check health..."
for i in {1..30}; do
  if curl -fsS http://127.0.0.1/health >/dev/null && \
     curl -fsS http://127.0.0.1/health/db >/dev/null; then 
    echo "Passed health checks"
    docker compose -f docker-compose.ec2.yml ps
    docker image prune -f
    exit 0
  fi

  echo "Attempt $i/30: API not up yet"
  sleep 5
done

echo "Failed health checks"
docker compose -f docker-compose.ec2.yml ps
docker compose -f docker-compose.ec2.yml logs --tail=200
exit 1

