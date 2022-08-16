import subprocess
import os
import time

wd = os.getcwd()
os.chdir("/home/jawad/betts/connect-recommendation-engine/ml")
process2 = subprocess.Popen(["./run_ml_main.sh"],shell=True)
process2.wait()
print("Completed!")
