FROM python:3.9.16-slim-buster as base

RUN apt-get update && apt-get install -y wget

ARG USERNAME=runpod-worker
ARG USER_UID=1001
ARG USER_GID=1001

ARG MODEL_URL
ARG TOKENIZER_URL
ENV MODEL_URL $MODEL_URL
ENV TOKENIZER_URL $TOKENIZER_URL


ARG STRATEGY="cuda fp16"
ENV STRATEGY=$STRATEGY

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

WORKDIR /runpod

RUN pip3 install poetry

COPY --chown=$USER_UID:$USER_GID ./poetry.lock ./pyproject.toml .
RUN poetry config installer.max-workers 10
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --only main -vvv

COPY ./download_model.sh .
RUN chmod +x ./download_model.sh && ~/download_model.sh

COPY --chown=$USER_UID:$USER_GID ./serverless_handler.py /runpod/
RUN chown -R $USER_UID:$USER_GID .

ENV STRATEGY $STRATEGY

USER $USERNAME

ENTRYPOINT ["python", "serverless_handler.py"]

