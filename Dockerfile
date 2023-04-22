FROM python:3.9.16-slim-buster

ARG USERNAME=runpod-worker
ARG USER_UID=1001
ARG USER_GID=1001

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

WORKDIR /runpod

RUN pip3 install poetry

COPY --chown=$USER_UID:$USER_GID ./poetry.lock ./pyproject.toml /runpod
RUN poetry install --no-interaction --no-ansi --only main

COPY --chown=$USER_UID:$USER_GID ./serverless_handler.py /runpod

USER $USERNAME

ENTRYPOINT ["python", "serverless_handler.py"]

