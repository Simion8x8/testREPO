#!/bin/bash
set -euo pipefail

DESIRED_RESP=200
STATUS=$(curl -i localhost:5000/health | grep HTTP | awk '{print $2}')
if [ "$STATUS" != "$DESIRED_RESP" ]; then
	echo "Response is not 200! Check service"
else
	echo "Service responded with 200"
fi  

