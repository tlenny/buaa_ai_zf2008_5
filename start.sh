#!/bin/bash

source venv/bin/activate
nohup uvicorn main:app --host 0.0.0.0 --port 8080 > system.log 2>&1 &
deactivate