import requests
import sys
import json
import urllib.parse

server = "206.12.90.50"
port = "8880"

# Register and enroll new user in organization
def register_user(user_name, organization):
    url = "http://{}:{}/users".format(server, port)
    headers = {"content-type": "application/x-www-form-urlencoded"}
    data = {"username":user_name, "orgName": organization}
    print("Registering user")
    response = requests.post(url, headers=headers, data=data)
    print(json.loads(response.text))
    print(json.loads(response.text)['success'] == True)
    return json.loads(response.text)['token']

# Create channel request
def create_channel(token, channel_name):
    url = "http://{}:{}/channels".format(server, port)
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    data = {"channelName": channel_name,
            "channelConfigPath":"../artifacts/channel/{}.tx".format(channel_name)}
    print("Creating channel")
    response = requests.post(url, headers=headers, json=data)
    print(response.text)

# Join channel request
def join_channel(token, organization_lower, channel_name):
    url = "http://{}:{}/channels/{}/peers".format(server, port, channel_name)
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    data = {"peers": ["peer0.{}.example.com".format(organization_lower),"peer1.{}.example.com".format(organization_lower)]}
    print("Joining channel")
    response = requests.post(url, headers=headers, json=data)
    print(response.text)

# Install chaincode
def install_chaincode(token, organization_lower ,chaincode_name, chaincode_path, chaincode_lang):
    url = "http://{}:{}/chaincodes".format(server, port)
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    data = {"peers": ["peer0.{}.example.com".format(organization_lower),"peer1.{}.example.com".format(organization_lower)], 
            "chaincodeName": chaincode_name,
            "chaincodePath": chaincode_path,
            "chaincodeType": chaincode_lang,
            "chaincodeVersion":"v0"}
    print("Installing chaincode")
    response = requests.post(url, headers=headers, json=data)
    print(response.text)


# Instantiate chaincode
def instantiate_chaincode(token, organization_lower, channel_name, chaincode_name, chaincode_lang):
    url = "http://{}:{}/channels/{}/chaincodes".format(server, port, channel_name)
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    data = {
            "chaincodeName": chaincode_name,
            "chaincodeType": chaincode_lang,
            "chaincodeVersion":"v0", 
            "args":["a","100","b","200"]
            }
    print("Instantiating chaincode")
    response = requests.post(url, headers=headers, json=data)
    print(response.text)

def get_installed_chaincodes(token, org):
    url = "http://{}:{}/chaincodes?peer=peer0.{}.example.com&type=installed".format(server, port, org)
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    print("Getting installed chaincodes")
    response = requests.get(url, headers=headers)
    print(response.text)

def get_instantiated_chaincodes(token, org):
    url = "http://{}:{}/chaincodes?peer=peer0.{}.example.com&type=instantiated".format(server, port, org)
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    print("Getting instantiated chaincodes")
    response = requests.get(url, headers=headers)
    print(response.text)

def query_job(token, channel_name, chaincode_name, org, job_name):
    query_set = str([job_name]) 
    url = "http://{}:{}/channels/{}/chaincodes/{}?peer=peer0.{}.example.com&fcn=queryJob&args={}".format(server, port,
         channel_name, chaincode_name, org, urllib.parse.quote(query_set))
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    print("Querying job")
    response = requests.get(url, headers=headers)
    print(response.text)

def invoke_new_job(token, channel_name, chaincode_name, org, job_id, service, developer, provider, provider_org):
    url = "http://{}:{}/channels/{}/chaincodes/{}".format(server, port, channel_name, chaincode_name)
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    data = {"peers": ["peer0.org1.example.com","peer0.org2.example.com"], 
        "fcn":"createJob",
        "args":[job_id, service, developer, provider, provider_org]}
    print("Creating new job")
    response = requests.post(url, headers=headers, json=data)
    print(response.text)

def invoke_set_time(token, channel_name, chaincode_name, org, job_id, time):
    url = "http://{}:{}/channels/{}/chaincodes/{}".format(server, port, channel_name, chaincode_name)
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    data = {"peers": ["peer0.org1.example.com","peer0.org2.example.com"], 
        "fcn":"setTime",
        "args":[job_id, time]}
    print("Setting the time")
    response = requests.post(url, headers=headers, json=data)
    print(response.text)
    return response


def invoke_received_result(token, channel_name, chaincode_name, org, job_id):
    url = "http://{}:{}/channels/{}/chaincodes/{}".format(server, port, channel_name, chaincode_name)
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    data = {"peers": ["peer0.org1.example.com","peer0.org2.example.com"], 
        "fcn":"receivedResult",
        "args":[job_id]}
    print("Setting the received result value")
    response = requests.post(url, headers=headers, json=data)
    print(response.text)

def invoke_balance_transfer_from_fabcar(token, channel_name, chaincode_name, org):
    url = "http://{}:{}/channels/{}/chaincodes/{}".format(server, port, channel_name, chaincode_name)
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    data = {"peers": ["peer0.org1.example.com","peer0.org2.example.com"], 
        "fcn":"my_cc",
        "args":["move", "b", "a", "hi"]}
    print("Invoke balance transfer")
    response = requests.post(url, headers=headers, json=data)
    print(response.text)



def invoke_balance_transfer(token, channel_name, chaincode_name, org):
    url = "http://{}:{}/channels/{}/chaincodes/{}".format(server, port, channel_name, chaincode_name)
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    data = {"peers": ["peer0.org1.example.com","peer0.org2.example.com"], 
        "fcn":"move",
        "args":["a", "b", "1"]}
    print("Invoke balance transfer")
    response = requests.post(url, headers=headers, json=data)
    print(response.text)

def invoke_balance_transfer_new_user(token, channel_name, chaincode_name, org, name, balance):
    url = "http://{}:{}/channels/{}/chaincodes/{}".format(server, port, channel_name, chaincode_name)
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    data = {"peers": ["peer0.org1.example.com","peer0.org2.example.com"], 
        "fcn":"new_user",
        "args":[name, balance]}
    print("Adding new user")
    response = requests.post(url, headers=headers, json=data)
    print(response.text)

def query_account(token, channel_name, chaincode_name, org, job_name):
    query_set = str([job_name]) 
    url = "http://{}:{}/channels/{}/chaincodes/{}?peer=peer0.{}.example.com&fcn=query&args={}".format(server, port,
         channel_name, chaincode_name, org, urllib.parse.quote(query_set))
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    print("Querying account")
    response = requests.get(url, headers=headers)
    print(response.text)

def get_logs(token):
    url = "http://{}:{}/logs".format(server, port)
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    print("Getting logs")
    response = requests.get(url, headers=headers)
    print(response.text)

hf_server = "162.246.156.104"
controller_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzkwNzAyNTAsInVzZXJuYW1lIjoiY29udHJvbGxlciIsIm9yZ05hbWUiOiJPcmcxIiwiaWF0IjoxNTc5MDM0MjUwfQ.obBKth1-52rSVz02df9AXLRMqvEGXVMLZJnFM3UGtvY"
channel_name="mychannel"
def invoke_received_result2(job_id, server=hf_server, token=controller_token, channel_name=channel_name):
    chaincode_name = "monitoring"
    url = "http://{}:{}/channels/{}/chaincodes/{}".format(server, port, channel_name, chaincode_name)
    auth = "Bearer " + token
    headers = {"authorization": auth, "content-type": "application/json"}
    data = {"peers": ["peer0.org1.example.com","peer0.org2.example.com"], 
        "fcn":"receivedResult",
        "args":[job_id]}
    print("Setting the received result value")
    response = requests.post(url, headers=headers, json=data)
    print(response.text)

def initialize_network():
    monetaryChaincode = 'monetary'
    monetaryPath = "./artifacts/src/monetary"
    monitoringChaincode = 'monitoring'
    monitoringPath= "./artifacts/src/monitoring"
    chaincodeLang = "node"
    user_list = ['sghaemi', 'admin', 'controller', 'provider_test', 'provider_test2', 'provider_test3']

    token1 = register_user('temp', 'Org1')
    token2 = register_user('temp', 'Org2')
    create_channel(token1, channelName)
    join_channel(token1, 'org1', channelName)
    join_channel(token2, 'org2', channelName)

    install_chaincode(token1, 'org1', monetaryChaincode, monetaryPath, chaincodeLang)
    install_chaincode(token2, 'org2', monetaryChaincode, monetaryPath, chaincodeLang)
    install_chaincode(token1, 'org1', monitoringChaincode, monitoringPath, chaincodeLang)
    install_chaincode(token2, 'org2', monitoringChaincode, monitoringPath, chaincodeLang)

    instantiate_chaincode(token1, 'org1', channelName, monetaryChaincode, chaincodeLang)
    instantiate_chaincode(token2, 'org2', channelName, monitoringChaincode, chaincodeLang)

    for user in user_list:
        invoke_balance_transfer_new_user(token1, channelName, monetaryChaincode, 'org1', user, "600")
    
    return token1, token2

if __name__ == "__main__":
    username = sys.argv[1]
    org = sys.argv[2]
    orgLower = org.lower()
    channelName = "mychannel"

    # chaincodePath = "./artifacts/src/monetary"
    # chaincodeName = "monetary"
    chaincodePath = "./artifacts/src/monitoring"
    chaincodeName = "monitoring"

    chaincodeLang = "node"

    token_org2 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzkyNTQxNDksInVzZXJuYW1lIjoidGVtcCIsIm9yZ05hbWUiOiJPcmcxIiwiaWF0IjoxNTc5MjE4MTQ5fQ.cbk3ayZfJWa4GD_piamhKuBGOmxbYwSns_iBnRGRRi0"
    token_org1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1ODM5MTQxNzgsInVzZXJuYW1lIjoiY29udHJvbGxlciIsIm9yZ05hbWUiOiJPcmcxIiwiaWF0IjoxNTgzODc4MTc4fQ.Zkeny5RFsGMOIUabquR7_LZI8U1QgoUyr_zqflAAcPI"
    


    token_org1, token_org2 = initialize_network()
    if org == "Org1":
        token = token_org1
    elif org == "Org2":
        token = token_org2

    # token = register_user(username, org)
    # print(get_logs(token))
    # invoke_balance_transfer_new_user(token, channelName, "monetary", 'org1', 'controller', "600")
    # create_channel(token, channelName)
    # join_channel(token, orgLower, channelName)
    # install_chaincode(token, orgLower, chaincodeName, chaincodePath, chaincodeLang)
    # instantiate_chaincode(token, orgLower, channelName, chaincodeName, chaincodeLang)
    # query_job(token, channelName, chaincodeName, orgLower, "90")
    # invoke_new_job(token, channelName, chaincodeName, orgLower, "-1", "10", "admin", "sghaemi", "Org2")
    # r = invoke_set_time(token, channelName, chaincodeName, orgLower, "-1", "100")
    # print('User was not found' in r.text)
    # invoke_received_result(token, channelName, chaincodeName, orgLower, "16")
    # invoke_received_result2("97")
    # query_job(token, channelName, chaincodeName, orgLower, "100")
    # invoke_balance_transfer_from_fabcar(token, channelName, chaincodeName, orgLower)
    # invoke_balance_transfer(token, channelName, chaincodeName, orgLower)
    # query_account(token, channelName, 'monetary', orgLower, 'controller')
    # query_account(token, channelName, "monetary", orgLower, 'admin')
    # invoke_balance_transfer_new_user(token, channelName, "monetary", orgLower, "controller", "600")
    # invoke_balance_transfer_new_user(token, channelName, "monetary", orgLower, "admin", "600")
    # invoke_balance_transfer_new_user(token, channelName, "monetary", orgLower, "sghaemi", "600")


    # get_installed_chaincodes(token, orgLower)
    # get_instantiated_chaincodes(token, orgLower)