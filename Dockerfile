# --------------------------------------------
# Firstly create a base image installing the dependencies and the piper TTS engine
FROM python:3.10 as base

WORKDIR /vivoac

EXPOSE 8080

COPY requirements.txt .

# Install piper as local TTS engine:
RUN apt-get update && \
    apt-get install -y \
    espeak-ng \
    git \
    ffmpeg 
RUN pip3 install --upgrade pip wheel setuptools
RUN git clone https://github.com/rhasspy/piper.git /piper
# To save some time there is a copy of piper in the project under data/external/piper
# RUN mv data/external/piper /piper
RUN cd /piper/src/python && pip install -e .
RUN mkdir -p /piper/src/python/piper_train/vits/monotonic_align/monotonic_align
RUN cd /piper/src/python/piper_train/vits/monotonic_align && cythonize -i core.pyx && mv core*.so monotonic_align/

RUN pip install -r requirements.txt
# The base image is done!

# --------------------------------------------
# create one deployment image for the main.py file
FROM base as deploy
WORKDIR /vivoac
ENV SETTINGS_VARIATION_PATH="./project-settings-docker.json"
EXPOSE 8080
COPY . .
CMD ["python", "main.py"]

# --------------------------------------------
# create one image for the testing
FROM base as test
WORKDIR /vivoac
ENV SETTINGS_VARIATION_PATH="./project-settings-docker.json"
COPY . .
RUN cp ./project-settings-docker.json ./project-settings-test.json
CMD ["python", "test_main.py"]