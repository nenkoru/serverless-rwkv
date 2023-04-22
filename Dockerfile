FROM python:3.9.16-slim-buster as base

FROM base as model_downloading

ARG MODEL_URL $MODEL_URL
ARG TOKENIZER_URL $TOKENIZER_URL

ENV MODEL_URL $MODEL_URL
ENV TOKENIZER_URL $TOKENIZER_URL

RUN apt-get update && apt-get install -y wget

COPY ./download_model.sh .
RUN ./download_model.sh

FROM base as production_build

ARG USERNAME=runpod-worker
ARG USER_UID=1001
ARG USER_GID=1001
ARG STRATEGY=cuda fp16

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

WORKDIR /runpod

RUN pip3 install poetry

COPY --chown=$USER_UID:$USER_GID ./poetry.lock ./pyproject.toml /runpod/
RUN poetry config installer.max-workers 10
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --only main -vvv

COPY --from=model_downloading --chown=$USER_UID:$USER_GID ./tokenizer.json /runpod/
COPY --from=model_downloading --chown=$USER_UID:$USER_GID ./model.pth /runpod/

COPY --chown=$USER_UID:$USER_GID ./serverless_handler.py /runpod/

ENV STRATEGY $STRATEGY

USER $USERNAME

ENTRYPOINT ["python", "serverless_handler.py"]

