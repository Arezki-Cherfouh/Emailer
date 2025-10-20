#!/bin/bash
cd "$(dirname "$0")"
echo "Running run_email_activation..."
wine "run_email_activation" || ./"run_email_activation" "$@"
