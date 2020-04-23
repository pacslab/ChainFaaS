import subprocess
import pandas as pd
import docker

body = "ghaemisr/node-info"

client = docker.from_env()

image = client.images.pull(body)
print(image)

result = client.containers.run(body, name='provider_container_1')
print(result)
filters = {'name':'provider_container_1'}
container_id = client.containers.list(all=True, filters=filters)[0]
container_id.remove()

client.images.remove(body)