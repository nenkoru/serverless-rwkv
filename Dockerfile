FROM python:3.9.16-slim-buster

ARG USERNAME=runpod-worker
ARG USER_UID=1001
ARG USER_GID=1001
ARG STRATEGY=cuda fp16
ARG MODEL_URL=https://huggingface.co/BlinkDL/rwkv-4-raven/resolve/main/RWKV-4-Raven-14B-v9-Eng99%25-Other1%25-20230412-ctx8192.pth
ARG TOKENIZER_URL=https://huggingface.co/spaces/BlinkDL/Raven-RWKV-7B/resolve/main/20B_tokenizer.json

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

RUN apt-get update && apt-get install -y wget

WORKDIR /runpod

RUN pip3 install poetry

COPY --chown=$USER_UID:$USER_GID ./poetry.lock ./pyproject.toml /runpod/
RUN poetry config installer.max-workers 10
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --only main -vvv

RUN wget $MODEL_URL -O model.pth
RUN wget $TOKENIZER_URL -O tokenizer.json

COPY --chown=$USER_UID:$USER_GID ./serverless_handler.py /runpod/

ENV STRATEGY $STRATEGY

USER $USERNAME

ENTRYPOINT ["python", "serverless_handler.py"]

