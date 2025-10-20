#!/bin/bash
cd "$(dirname "$0")"
echo "Running run_emailer..."
wine "run_emailer" || ./"run_emailer" "$@"
