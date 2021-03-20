FROM python:3.9.2-alpine

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN apk add --no-cache gcc musl-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY src .
CMD ["python", "main.py"]

