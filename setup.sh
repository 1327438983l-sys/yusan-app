#!/bin/bash
# Create GitHub repo and push
cd /c/Users/13274/语文复习App

# Get token
TOKEN=$(git credential-manager get <<< $'host=github.com\nprotocol=https\n' 2>/dev/null | grep "^password=" | sed 's/^password=//')

# Create repo
echo '{"name":"yusan-app","description":"三年级下册语文复习App","auto_init":false}' > /tmp/repo.json
curl -s -X POST https://api.github.com/user/repos \
  -H "Authorization: token $TOKEN" \
  -H "Content-Type: application/json" \
  -d @/tmp/repo.json

rm /tmp/repo.json
