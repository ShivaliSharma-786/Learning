import subprocess
from datetime import datetime, timedelta
import os
import sys

today = datetime.now().strftime("%Y.%m.%d")

dc_name=os.uname()[1][1:4].upper()
scriptpath=os.path.dirname(sys.argv[0])
if scriptpath== '':
    scriptpath='./'
os.chdir(scriptpath)
data=dc_name + "helm_data"
data= subprocess.getoutput('/usr/local/bin/helm list -A > helm_{0}.csv'.format(dc_name))

