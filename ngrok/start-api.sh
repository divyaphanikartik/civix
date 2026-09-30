#!/bin/sh
set -eu
exec ngrok http backend:8000 --url "$NGROK_API_DOMAIN"
