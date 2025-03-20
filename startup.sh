#!/bin/bash
cd /home/site/wwwroot
gunicorn -w 2 -k uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 src.crew_ai_agents.app:app