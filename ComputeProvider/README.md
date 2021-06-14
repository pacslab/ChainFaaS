# ChainFaaS Compute Providers


Follow the steps bellow to add a new provider:

## Step 1: Register in website

Go to [registration page of ChainFaaS website](http://www.chainfaas.com/profiles/register/) and register as a new user. You will 
later use the username and password created in this step to run the provider code. 

## Step 2: Install git

``` bash
sudo apt install git
```

## Step 3: Clone this repository and go to its directory

``` bash
git clone https://github.com/pacslab/ChainFaaS

cd ChainFaaS/ComputeProvider
```

## Step 4: Run setup.sh file

``` bash
sudo ./setup.sh
```

## Step 5: Run provider.py code

``` bash
python3 provider.py {username} {password} {CPU} {RAM}
```
