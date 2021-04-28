#!/usr/bin/env bash

export $(egrep -v '^#' .env | xargs)

# run api server
uvicorn server:APP --host 0.0.0.0 --port 8105 --reload