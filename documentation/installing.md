<!---         
    Hier kommt rein:
    Wie der code installiert wird!


      -->

### Installing
When you have installed all the dependencies (see [readme.md](../README.md)) open up a terminal and create a new python environment:  
**unix:**
```sh
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```
**windows**
```sh
python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt
```
Wait a minute until all the packages are installed . . .

### Deployment
Here are the two options to deploy the API-Server.
One way is to do it locally, on your machine.
The other uses the Dockerfile, to create a Docker Image, so that you can containerize this application.

#### Local
Be sure to activate the Python env:
**unix**
```sh
source venv/bin/activate
``` 
**windows**
```sh
venv\Scripts\activate
```
And then just run the main.py file and the server will (should) start up.
```sh
python main.py
```
#### Docker Image
To run the server as a Docker container you first have to build the docker image:  
_Be sure the docker daemon is running, open up your console and then type_
```sh
docker build -t <cool_name:tag> . 
```
_. . . wait a second . . ._  
And then run the container on a computer or server of your choice:
```sh
docker run -itd -p 8080:<8080> --name <cool_container_name> <cool_name:tag>
```

If you want local access to the log files you can append a volume mapping:
```sh
docker run -itd -p 8080:<8080> --name <cool_container_name> -v <your_log_foler>:/var/logs/vivoac <cool_name:tag>
```
The same goes for the settings, if you want to edit them later on, just mount the DOCKER settings file to the running container:
_Keep in mind, that you need to resart the docker container for the changes to apply!_
```sh
docker run -itd -p 8080:<8080>  --name <cool_container_name> -v <cwd>/project-settings-docker.json:/vivoac/project-settings.json <cool_name:tag>
```