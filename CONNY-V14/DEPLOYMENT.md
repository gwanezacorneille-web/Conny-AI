# CONNY AI V14 Production Deployment

## API

Start:

`uvicorn api.main:app --host 0.0.0.0 --port 8000`

## Health

`GET /api/health`

`GET /api/production/health`

## Authentication

`POST /auth/register`

`POST /auth/login`

`POST /auth/guest`

`GET /auth/session`

`POST /auth/logout`

## Sync

`POST /sync/push`

`GET /sync/pull`

## VIP

Set:

`CONNY_VIP_USERNAME`

`CONNY_VIP_SECRET`

Never commit VIP credentials.

## Production note

The deployment must provide persistent storage for SQLite databases,
or the database layer must be migrated to a managed production
database before operating at scale.

The deployment is not considered LIVE until the public health endpoint
has been tested successfully.
