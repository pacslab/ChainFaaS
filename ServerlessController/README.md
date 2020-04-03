# ChainFaaS Serverless Controller
 
 The format of the repository is very similar to any other Django project. All the configuration parameters are stored in the [MSc_Research_Django/settings.py](./MSc_Research_Django/settings.py) file. All the sensitive information such as usernames and passwords of the database and rabbitmq server should be stored in a file named *settings.ini* located at /etc/MSc_Research_Django in the following format:

 ``` bash
 [postgres]
POSTGRES_USER=
POSTGRES_PASS=

[rabbitmq]
RABBITMQ_USER=
RABBITMQ_PASS=
 ```

 This Django project has 4 apps:
 
 * profiles: Includes user models, login, registration, and user change info. 
 * controller_app: Includes all the functionalities of controller such as finding appropriate provider for each request.
 * providers_app: Includes everything related to providers such as rabbitmq queue communications, contribution, etc. 
 * developers_app: Includes everything related to developers such as creating, starting, stopping, deleting service, service model, etc. 
