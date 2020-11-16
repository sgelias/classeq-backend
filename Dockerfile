FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

COPY ./lepiota/requirements.txt /code/requirements.txt
RUN pip install --upgrade pip && pip install -r /code/requirements.txt

COPY repDNA-1.1.4/ repDNA-1.1.4/
RUN cd repDNA-1.1.4 && python setup.py install

COPY . /code/
WORKDIR /code/
EXPOSE 8001
