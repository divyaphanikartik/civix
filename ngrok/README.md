# Civix ngrok ingress

Civix uses two ngrok endpoints in deployment:

- `NGROK_API_DOMAIN` -> FastAPI (`backend:8000`)
- `NGROK_APP_DOMAIN` -> React (`frontend:5173`)

Use stable/reserved ngrok domains for a deployed environment. Do not use an ephemeral URL for the Twilio webhook.

The ngrok containers are intentionally part of the production compose stack so the public ingress starts/stops with Civix.
