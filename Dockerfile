FROM amd64/python:3.10-slim as base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    postgresql-client \
    curl \
    build-essential 
ENV PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=$PYTHONPATH:. \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME=$HOME/.poetry \
    POETRY_VERSION=1.3.1 \
    WORKDIR=/workspace 
ENV PATH="$POETRY_HOME/bin:$PATH" 
WORKDIR $WORKDIR

FROM base as poetry_installer
RUN curl -sSL https://install.python-poetry.org | python3 -

FROM base as package_installer
COPY --from=poetry_installer $POETRY_HOME $POETRY_HOME
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-root --without dev 

FROM base as data_generator
COPY --from=package_installer /usr/local/bin /usr/local/bin
COPY --from=package_installer /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY . .
ENTRYPOINT ["python", "./src/database/data_generator.py", "--db-host"]
CMD ["localhost"]

FROM base as mlflow_server
RUN apt-get update && apt-get install -y \
    wget
RUN wget https://dl.min.io/client/mc/release/linux-amd64/mc && \
    chmod +x mc && \
    mv mc /usr/bin/mc
ENV PATH="$PATH:$HOME/minio-binaries/"
COPY --from=package_installer /usr/local/bin /usr/local/bin
COPY --from=package_installer /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY . .

FROM base as fastapi_server
COPY --from=package_installer /usr/local/bin /usr/local/bin
COPY --from=package_installer /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY . .
ENTRYPOINT ["uvicorn"]
CMD ["--app-dir", "src/fastapi_tutorial", "--host", "0.0.0.0", "crud_pydantic:app", "--reload"]