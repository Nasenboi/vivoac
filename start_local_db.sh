docker run -itd --name vivoac_mongo -p 27017:27017 -v "./data/docker_files/mongo:/data/db" mongo:7.0 --auth