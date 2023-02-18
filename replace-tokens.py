import sys
file=sys.argv[1]
with open(file,'r') as f:
    data=f.read()
import os
data=data.replace("USERNAME",os.environ.get("USER")) 
with open(file+'.correct','w') as f:
    f.write(data)