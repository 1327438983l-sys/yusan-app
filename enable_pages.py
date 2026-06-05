import subprocess
import json
import urllib.request

# Get token
result = subprocess.run(
    ['git', 'credential-manager', 'get'],
    input=b'host=github.com\nprotocol=https\n',
    capture_output=True
)
token = None
for line in result.stdout.decode().split('\n'):
    if line.startswith('password='):
        token = line.split('=', 1)[1]
        break

# Enable GitHub Pages - use /docs folder
data = json.dumps({
    "source": {
        "branch": "main",
        "path": "/docs"
    }
}).encode()

req = urllib.request.Request(
    'https://api.github.com/repos/1327438983l-sys/yusan-app/pages',
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
    result = json.loads(resp.read())
    print(f"Pages enabled: {result.get('html_url', 'checking...')}")
    print(f"URL: https://1327438983l-sys.github.io/yusan-app/")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"Error {e.code}: {body}")
    # Try to get current pages config
    req2 = urllib.request.Request(
        'https://api.github.com/repos/1327438983l-sys/yusan-app/pages',
        headers={
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    )
    try:
        resp2 = urllib.request.urlopen(req2)
        print("Current pages config:", json.loads(resp2.read()))
    except:
        pass
