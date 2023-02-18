import sys
import json

try:
    with open("/tmp/system-stats-server-data.json",'r') as f:
        data=json.loads(f.read())
except:
    print("0")
    exit(0)

arg=sys.argv[1]
if arg not in data.keys():
    print("0")
    exit(0)
print(data[arg])