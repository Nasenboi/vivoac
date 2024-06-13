FROM python:3.10

WORKDIR /vivoac

EXPOSE 8080

COPY . .

ENV SETTINGS_VARIATION_PATH="./project-settings-docker.json"

# Install piper as local TTS engine:
RUN apt-get update && \
    apt-get install -y \
    espeak-ng \
    git
RUN pip3 install --upgrade pip wheel setuptools
RUN git clone https://github.com/rhasspy/piper.git
RUN cd piper/src/python && pip install -e .
RUN mkdir -p piper/src/python/piper_train/vits/monotonic_align/monotonic_align
RUN cd piper/src/python/piper_train/vits/monotonic_align && cythonize -i core.pyx && mv core*.so monotonic_align/

RUN pip install -r requirements.txt

CMD ["python", "main.py"]