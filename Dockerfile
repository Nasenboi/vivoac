FROM python:3.10

WORKDIR /vivoac

EXPOSE 8080

COPY . .

ENV SETTINGS_VARIATION_PATH="./project-settings-docker.json"

RUN pip install -r requirements.txt

CMD ["python", "main.py"]