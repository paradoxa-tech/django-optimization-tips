# django-optimization-tips
Project for the workshop "Tips for Optimizing Django Database Queries"


# Prerequisites
Reference: [Install Python3 and virtualenv on Ubuntu](https://vitux.com/install-python3-on-ubuntu-and-set-up-a-virtual-programming-environment/)
## Python3
You can install Python3 through apt-get:
```
$ sudo apt-get update
$ sudo apt-get install python3
```

## Pip3
In order to install pip3, you have to install some prerequisites:
```
$ sudo apt-get install build-essential libssl-dev libffi-dev python-dev
```
Now check if pip is already installed:
```
$ pip3 --version
```

If the output suggests that pip is not installed on your system ru the
following commands:
```
$ sudo apt-get update
$ sudo apt install python3-pip
```

## Virtual Environment
### VirtualEnv installation:
First, install virtualenv:
```
$ sudo apt install -y python3-venv
```
### Setup the virtual environment to run the project
1. Create a new directory where you are going to clone the project.
    ```
    $ mkdir pydaybcn_best_workshop
    ```
1. Create a directory for the virtual environment.
    ```
    $ cd pydaybcn_best_workshop
    $ mkdir dot_venv
    ```
1. Create and activate the virtual environment:
    ```
    $ python3 -m venv dot_venv
    $ source dot_venv/bin/activate
    ```
## Download the project
Get the project from our public repo:
```
git clone https://github.com/paradoxa-tech/django-optimization-tips.git
```
## Install requirements
```
cd django-optimization-tips
pip3 install -r requirements.txt
```
## Run the server
```
$ python manage.py runserver 9000
```
## Load database
Load database
```
python manage.py shell

>>> from utils.database import load_database
>>> load_database()
```
## Access to the application
In your Internet browser go to http://127.0.0.1:9000/
