from django.shortcuts import render
from MSc_Research_Django.settings import CONTROLLER_TOKEN, PATH
import requests
import json

hf_server = "206.12.90.50"
# Remeber to change hf_server back to the one above
# when sending a pull request to the public repo
# hf_server = "162.246.156.104"
hf_port = "8880"
controller_token = CONTROLLER_TOKEN
controller_username = 'controller'
controller_org = 'Org1'
channel_name = 'mychannel'
monitoring_chaincode = 'monitoring'
monetary_chaincode = 'monetary'

def invoke_new_job(job_id, service, developer, provider, provider_org, server=None, port=None, token=None, ch_name=None):
    if token is None:
        token = controller_token
    if server is None:
        server = hf_server
    if port is None:
        port = hf_port
    if ch_name is None:
        ch_name = channel_name

    chaincode_name = monitoring_chaincode
    url = "http://{}:{}/channels/{}/chaincodes/{}".format(server, port, ch_name, chaincode_name)
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    data = {"peers": ["peer0.org1.example.com","peer0.org2.example.com"], 
        "fcn":"createJob",
        "args":[job_id, service, developer, provider, provider_org]}
    print("Creating new job")
    response = requests.post(url, headers=headers, json=data)
    print(response.text)
    return response

def invoke_new_monetary_account(name, balance, server=None, port=None, token=None, ch_name=None):
    if token is None:
        token = controller_token
    if server is None:
        server = hf_server
    if port is None:
        port = hf_port
    if ch_name is None:
        ch_name = channel_name

    chaincode_name = monetary_chaincode
    url = "http://{}:{}/channels/{}/chaincodes/{}".format(server, port, ch_name, chaincode_name)
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    data = {"peers": ["peer0.org1.example.com","peer0.org2.example.com"], 
        "fcn":"new_user",
        "args":[name, balance]}
    print("Adding new user")
    print(controller_token)
    print(token)
    response = requests.post(url, headers=headers, json=data)
    print(response.text)
    return response

def invoke_received_result(job_id, server=None, port=None, token=None, ch_name=None):
    if token is None:
        token = controller_token
    if server is None:
        server = hf_server
    if port is None:
        port = hf_port
    if ch_name is None:
        ch_name = channel_name

    chaincode_name = monitoring_chaincode
    url = "http://{}:{}/channels/{}/chaincodes/{}".format(server, port, ch_name, chaincode_name)
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    data = {"peers": ["peer0.org1.example.com","peer0.org2.example.com"], 
        "fcn":"receivedResult",
        "args":[job_id]}
    print("Setting the received result value")
    print(controller_token)
    print(token)
    response = requests.post(url, headers=headers, json=data)
    print(response.text)
    return response


def register_user(user_name=None, organization=controller_org, server=None, port=None):
    if user_name is None:
        user_name = controller_username
    if server is None:
        server = hf_server
    if port is None:
        port = hf_port
    if organization is None:
        organization = controller_org

    global controller_token
    url = "http://{}:{}/users".format(server, port)
    headers = {"content-type": "application/x-www-form-urlencoded"}
    data = {"username":user_name, "orgName": organization}
    print("Registering user")
    response = requests.post(url, headers=headers, data=data)
    print(response.text)
    controller_token = json.loads(response.text)['token']
    print(controller_token)
    return json.loads(response.text)['token']