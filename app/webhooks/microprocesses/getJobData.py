import sys
import json
import requests
from xytech import Xytech

if __name__=="__main__":
    args = sys.argv[1:]
    job = int(args[0])
    xy = Xytech()
    JOB = xy.getJob(job)
    # r = requests.get(url=JOB, auth=(xy.UN, xy.PW))
    # res = r.json()
    print(JOB)