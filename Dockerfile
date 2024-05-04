FROM python:3.12

WORKDIR /vivoac

COPY project-settings-docker.json project-settings.json

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "./main.py"]