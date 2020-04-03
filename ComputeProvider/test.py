import subprocess
import pandas as pd

name = "ghaemisr/node-info"

process = subprocess.Popen(['docker', 'ps', '-a'],
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
stdout, stderr = process.communicate()
if name in stdout:
    df = pd.DataFrame([x.split() for x in stdout.split('\n')])
    containers = list(df[df[1] == "ghaemisr/node-info"][0])
    process = subprocess.Popen(['docker', 'rm'] + containers,
                                stdout=subprocess.PIPE,
                                universal_newlines=True)
    stdout, stderr = process.communicate()
    print(stdout)

process = subprocess.Popen(['docker', 'images'],
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
stdout, stderr = process.communicate()

if name in stdout:
    df = pd.DataFrame([x.split() for x in stdout.split('\n')])
    image_id = df[df[0] == "ghaemisr/node-info"][2][1]
    process = subprocess.Popen(['docker', 'image', 'rm', image_id],
                                stdout=subprocess.PIPE,
                                universal_newlines=True)
    stdout, stderr = process.communicate()
    print(stdout)