# Civix deployment

## Production topology

Internet / WhatsApp
        |
        v
   ngrok cloud
     /      \
    v        v
API endpoint  App endpoint
    |            |
    v            v
 FastAPI       React
    |
    v
PostgreSQL

A dedicated worker consumes persisted WhatsApp audio messages from PostgreSQL. The webhook never waits for Gemini processing.

## 1. Create stable ngrok endpoints

Reserve/assign stable ngrok domains for the API and app. Do not use an ephemeral URL for a deployed Twilio webhook. ngrok supports custom/reserved endpoint URLs and Docker agents.

Set:

NGROK_API_DOMAIN=api.your-domain
NGROK_APP_DOMAIN=app.your-domain
PUBLIC_API_URL=https://api.your-domain
PUBLIC_APP_URL=https://app.your-domain

## 2. Configure secrets

Copy `.env.production.example` to `.env` and fill in all values. Never commit `.env`.

## 3. Start

`docker compose up -d --build`

## 4. Verify

`docker compose ps`

`docker compose logs -f backend worker ngrok-api`

The API readiness endpoint is:

`https://api.your-domain/health/ready`

The React application is:

`https://app.your-domain`

## 5. Twilio Sandbox

In Twilio Sandbox settings, configure the incoming-message webhook as:

`https://api.your-domain/api/webhooks/whatsapp`

Use HTTP POST.

The backend validates the `X-Twilio-Signature` in production.

## 6. Important production notes

- Keep PostgreSQL private; it is not exposed to the internet.
- Keep FastAPI and React private; ngrok is the public ingress.
- Use stable ngrok domains so the Twilio webhook does not change after restarts.
- Use a strong random PostgreSQL password.
- Keep Twilio/Gemini/ngrok credentials only in environment/secrets storage.
- The current grievance/MCDA code still contains prototype TODOs; deployment infrastructure does not make those business rules production-ready.
- For larger workloads, replace the polling worker with a durable queue such as Redis/Celery or a managed queue.
