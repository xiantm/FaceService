#!/bin/bash

exec gunicorn -t 3600 --graceful-timeout 3600 -b :5000 --access-logfile - --error-logfile - face_service:app