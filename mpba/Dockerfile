FROM python:3.8

ARG GIT_COMMIT=unspecified
ENV GIT_COMMIT=${GIT_COMMIT}

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY mpba mpba
COPY setup.py .
COPY README.md .

RUN python setup.py install
