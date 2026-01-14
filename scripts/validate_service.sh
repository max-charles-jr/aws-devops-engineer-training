#!/bin/bash
sleep 5
curl -f http://localhost:8000/health || exit 1