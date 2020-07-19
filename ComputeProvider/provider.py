import requests
from requests import ConnectionError
import pika
import re
import sys
import time
import json
import HFRequests
import os
import math
import pandas as pd
import docker

ready_response_text = 'Done!'
# controller = 'chainfaas.com'
controller = 'chainfaas.sara-dev.com'
controller_temp = 'chainfaas.sara-dev.com'
# controller = 'localhost'
# controller_temp = 'localhost:8080'
# controller_short = '127.0.0.1'

username = sys.argv[1]
password = sys.argv[2]

CPU = sys.argv[3]
RAM = sys.argv[4]

LOGIN_URL = 'http://' + controller_temp + "/profiles/user_login/"
PROVIDER_URL = 'http://' + controller_temp + "/provider/"
READY_URL = 'http://' + controller_temp + "/provider/ready"
NOT_READY_URL = 'http://' + controller_temp + "/provider/not_ready"
ACK_URL = 'http://' + controller_temp + "/provider/job_ack?job="

rabbitmq_password = username + '_mqtt'

channelName = "mychannel"
chaincodeName = "monitoring"
token = ""

client = docker.from_env()
container_name = 'provider_container_1'

def run_docker(body):
    start_pull_time = time.time()
    image = client.images.pull(body)
    print("Pull done!")
    pull_time = int((time.time() - start_pull_time) *1000)

    start_run_time = time.time()
    result = client.containers.run(body, name=container_name)
    result = result.decode("utf-8")
    print("Run done!")

    print(result)
    run_time = int((time.time() - start_run_time)*1000)
    return result, pull_time, run_time

def delete_container_and_image(body):

    filters = {'name': container_name}
    container_id = client.containers.list(all=True, filters=filters)[0]
    container_id.remove()

    client.images.remove(body)

def HF_set_time(job_code, t_time):
    global token
    response = HFRequests.invoke_set_time(token, channelName, chaincodeName, 'org2', job_code, t_time)
    if 'jwt expired' in response.text or 'jwt malformed' in response.text or 'User was not found' in response.text or 'UnauthorizedError' in response.text:
        token = HFRequests.register_user(username, 'Org2')
        response = HFRequests.invoke_set_time(token, channelName, chaincodeName, 'org2', job_code, t_time)
    return response

def on_request(ch, method, props, body):
    global token
    print(body)

    if body.decode("utf-8") == '"Stop"':
        ch.basic_ack(delivery_tag=method.delivery_tag)
        ch.queue_purge(username)
        ch.close()
        return
    print("Received a request, running docker file.")
    body_dict = json.loads(body.decode("utf-8"))
    print((ACK_URL + str(body_dict['job'])))
    s.get(ACK_URL + str(body_dict['job']))
    s.get(NOT_READY_URL)
    print("Before run docker")
    r, pull_time, run_time = run_docker(body_dict['task'])
    total_time = math.ceil(((pull_time + run_time)/100.0))*100
    print(pull_time, run_time, total_time)
    temp = {'Result': r, 'pull_time': pull_time, 'run_time': run_time, 'total_time': total_time}
    mqtt_response = json.dumps(temp)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(mqtt_response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print('sent back the results')
    time.sleep(3)
    # HF_resp = HF_set_time(str(body_dict['job']), str(total_time))
    # while (json.loads(HF_resp.text)['success'] == False):
    #     HF_resp = HF_set_time(str(body_dict['job']), str(total_time))
    #     if "The time for this job is already set and can't be changed." in json.loads(HF_resp.text)['message']:
    #         break
    delete_container_and_image(body_dict['task'])

s = requests.Session()

print(username)

data = {'username': username,
        'password': password}
response = s.post(url=LOGIN_URL, data=data)
print('Login response status', response.status_code)

response = s.get(PROVIDER_URL)
if re.search('stop', response.text) is None:
    data = {'ram': RAM, 'cpu': CPU}
    response = s.post(url=PROVIDER_URL, data=data)
    print('Ready response status', response.status_code)

credentials = pika.PlainCredentials(username, rabbitmq_password)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(controller, 5672, credentials=credentials))

print("You logged in to RabbitMQ!")

channel = connection.channel()

channel.queue_declare(queue=username)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=username, on_message_callback=on_request)

while channel.is_open:
    # with requests.Session() as session:
    try:
        print(" [x] Awaiting RPC requests")
        channel._impl._raise_if_not_open()
        while channel._consumer_infos:
            # This will raise ChannelClosed if channel is closed by broker
            r = s.get(READY_URL)
            channel._process_data_events(time_limit=30)
            print(" [x] Awaiting RPC requests")
    except ConnectionError:
        continue
