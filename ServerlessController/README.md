# ChainFaaS Serverless Controller
 
 Testing pull request from private repo.
 
 This Django project has 5 apps:
 
 * profiles: Includes user models, login, registration, and user change info. 
 * controller_app: Includes all the functionalities of controller such as finding appropriate provider for each request.
 * providers_app: Includes everything related to providers such as rabbitmq queue communications, contribution, etc. 
 * developers_app: Includes everything related to developers such as creating, starting, stopping, deleting service, service model, etc. 
 * fabric: Contains the Hyperledger Fabric communication details.

## To run a serverless controller

### Step 1: Clone the repository

In this step, you need to install git, clone the ChainFaaS repository and go to the correct directory. 

```bash
sudo apt install git
git clone https://github.com/pacslab/ChainFaaS
cd ChainFaaS/ServerlessController
```

### Step 2: Add the necessary configuration files.
 The format of the repository is very similar to any other Django project. All the configuration parameters are stored in the [MSc_Research_Django/settings.py](./MSc_Research_Django/settings.py) file. All the sensitive information such as usernames and passwords of the database, rabbitmq server, and fabric token, should be stored in a file named *settings.ini* located at the root of the Django project in the following format:

 ``` bash
 [postgres]
POSTGRES_USER:
POSTGRES_PASS:

[rabbitmq]
RABBITMQ_USER:
RABBITMQ_PASS:

[fabric]
CONTROLLER_TOKEN:
 ```

Also, the database and RabbitMQ settings should be added to file named *.env.prod.db* located at the root of the Django project in the following format:
```bash
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
RABBITMQ_DEFAULT_USER=
RABBITMQ_DEFAULT_PASS=
```

### Step 3: Run the server_setup.sh file.

By running the server_setup.sh file, all the prerequisites are installed. 

```bash
sudo ./server_setup.sh
```

### Step 4: run the docker-compose
```bash
docker-compose up -d --build
```
