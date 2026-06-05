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

# Check pages deployment status
req = urllib.request.Request(
    'https://api.github.com/repos/1327438983l-sys/yusan-app/pages/builds',
    headers={
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
)

try:
    resp = urllib.request.urlopen(req)
    builds = json.loads(resp.read())
    for b in builds.get('workflow_runs', builds.get('builds', []))[:3]:
        print(f"Status: {b.get('status')}, Conclusion: {b.get('conclusion')}, Updated: {b.get('updated_at')}")
except urllib.error.HTTPError as e:
    print(f"Error {e.code}: {e.read().decode()[:200]}")
