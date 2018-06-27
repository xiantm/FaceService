#!/bin/bash
exec gunicorn -k gevent -w 1 -t 3600 --graceful-timeout 3600 -b :5000 --access-logfile - --error-logfile - manage:app