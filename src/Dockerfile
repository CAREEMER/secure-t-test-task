FROM python:3.10.5

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update \
  && apt install netcat -y  \
  && pip install --upgrade pip \
  && pip install poetry==1.1.6 \
  && apt install -yq tzdata \
  && ln -fs /usr/share/zoneinfo/Russia/Moscow /etc/localtime \
  && dpkg-reconfigure -f noninteractive tzdata

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY . .

RUN chmod 777 /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
