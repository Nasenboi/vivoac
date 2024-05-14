# vivoac
 **Vi**rtual **Vo**ice **Ac**tor  
 The goal of this project is, to seamlessly integrate AI-Voice-Cloning Services into dubbing Studio environments for an easy and authentical on-the-fly text-to-speech generation of dialogue script lines.

## Table of Contents

- [Description](#description)
- [Getting Started](#getting-started)
    - [Dependencies](#dependencies)
    - [Installing](#installing)
    - [Deployment](#deployment)
    - [Testing](#testing)
- [Help](#help)
- [Contributors](#contributors)
- [License](#license)
- [Acknoledgements](#acknowledgments)
    - [Notes of Thanks](#notes-of-thanks)
    - [Honorable Code(ers)](#honorable-codeers)

## Description
This project will bring the power of AI Voice Cloning right to the hands of any dubbing studio!  
It will embed any possible Voice Cloning service into its API using a custom built module. Then users can upload IDs of scriptlines, or the text itself and watch as the API does the rest of the work until they recieve an audio file of the spoken text from the automatically trained Voice Clone.  

The user has all the power over the API, choosing which AI-Service to use, what text to generate and which files to use as a voice reference, and maybe even changing the script text or the audio file, if the generated output was not as required.  

## Getting Started
In this chapter you will learn how to set up this code, what dependencies you need to install and how to deploy the API-Server.
### Dependencies
Here ist just a fancy list of dependencies, check, if you have everything you need:
The code is tested using the listed verions, others may work, or not you may dare to try!

| Name  | Version | Link |
| ------------- | ------------- |------------- |
| Python  | 3.10.x  | [here](https://www.python.org/downloads/) |
| Docker  | 24.x | [here](https://docs.docker.com/get-docker/) |
| Git | 2.44.x | [here](https://git-scm.com/downloads) |
| GitHub Desktop (recommendation) | 3.3.x | [here](https://desktop.github.com/) |
| | | [here]() |

### Installing
When you have installed all the dependencies open up a terminal and create a new python environment:  
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
One way is to do it locally, on you machine.
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

### Testing

## Help

To get more informations about this repository, I would recomment you to read the [documentation](./documentation/documentation.md).




## Contributors 

- [Christian Böndgen - Nasenboi](https://github.com/Nasenboi)


<!---## License-->


## Acknowledgments

### Notes of Thanks
- A huge thanks goes out to the amazing team of the **rain productions** studio in cologne!\
Only with their help, it was possible for me to write my first own software solution with an authentic goal and an open and friendly environment to develop such project.
    - :globe_with_meridians: https://rain-productions.de/
    - :arrow_forward: [youtube](https://www.youtube.com/@rainproductionsDE)
    - :camera: [instagram](https://www.instagram.com/rain_cologne)

- Also I want to thank my university **HSD - Hochschule Düsseldorf**\
 \- not only for the opportunity of this memorable final bachelor project,\
 but also for the educational, multifaceted and most importantly fun seven semesters on my way to this bachelor thesis.
    - :globe_with_meridians: https://www.hs-duesseldorf.de/
    - :arrow_forward: [youtube](https://www.youtube.com/@hsduesseldorfhsd)
    - :camera: [instagram](https://www.instagram.com/hsduesseldorf)


### Honorable Code(ers)

- [DomPizzie](https://github.com/DomPizzie) aka Dominique Pizzie for [A simple README.md template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)

- [KernelA](https://github.com/KernelA) aka Alexander Kryuchkov for [.dockerignore example for Python projects](https://gist.github.com/KernelA/04b4d7691f28e264f72e76cfd724d448)