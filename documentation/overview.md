<!---         
    Hier kommt rein:
    Wie der code aufgebaut ist!


      -->

# Overview

In this overview you will learn how the code is structured.
The code is divided into two main parts: the [frontend](./frontends/frontends.md) and the [backend](./backend/backend.md).
The frontend vould have multiple forms, currently only one kind is implemented, a JUCE audio [plugin](./frontends/plugin/plugin.md).
The backend is a Python Webserver running that is supposed to run on a Docker Container on a server.  

This code project has additional features, besides the front- and backend code. Test scripts are built to ensure the proper functionality of the code. The [Dockerfile](../Dockerfile) ensures the containerisation of the backend. For individual convigurations of different runs, there are multiple settings files!  

