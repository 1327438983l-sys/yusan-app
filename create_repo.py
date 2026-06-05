import subprocess
import json
import urllib.request

# Get GitHub token from credential manager
result = subprocess.run(
    ['git', 'credential-manager', 'get'],
    input=b'host=github.com\nprotocol=https\n',
    capture_output=True
)
lines = result.stdout.decode().split('\n')
token = None
for line in lines:
    if line.startswith('password='):
        token = line.split('=', 1)[1]
        break

if not token:
    print("ERROR: No token found")
    exit(1)

print(f"Token found (length: {len(token)})")

# Create repo
data = json.dumps({
    "name": "yusan-app",
    "description": "三年级下册语文复习App - 部编版三年级下册语文复习清单+在线测试",
    "auto_init": False,
    "homepage": ""
}).encode()

req = urllib.request.Request(
    'https://api.github.com/user/repos',
    data=data,
    headers={
        'Authorization': f'token {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.github.v3+json'
    },
    method='POST'
)

try:
    resp = urllib.request.urlopen(req)
    repo = json.loads(resp.read())
    print(f"Repo created: {repo['html_url']}")
    print(f"Clone URL: {repo['clone_url']}")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"Error {e.code}: {body}")
    # If repo already exists, that's fine
    if e.code == 422:
        print("Repo already exists, continuing...")
