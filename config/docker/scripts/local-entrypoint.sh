#!/bin/bash
set -eu

cd app/
poetry install
mkdir -p /logs

exec "$@"
