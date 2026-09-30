#!/bin/sh
set -eu
exec ngrok http frontend:5173 --url "$NGROK_APP_DOMAIN"
