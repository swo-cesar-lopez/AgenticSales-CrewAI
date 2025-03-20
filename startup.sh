#!/bin/bash
cd /home/site/wwwroot
gunicorn --workers 2 --timeout 600 --bind=0.0.0.0:8000 src.crew_ai_agents.app:app