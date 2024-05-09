FROM python:3.10

WORKDIR /vivoac

EXPOSE 8080

COPY project-settings-docker.json project-settings.json

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]