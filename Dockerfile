FROM python:latest

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# RUN chmod a+x docker/*.sh

CMD ["alembic", "upgrade", "head"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 5500/tcp
EXPOSE 5500/udp
