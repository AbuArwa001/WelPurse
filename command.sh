#!/usr/bin/env bash
gunicorn --reload --bind 0.0.0.0:5001 'api.v1.app:app'