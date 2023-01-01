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
ENV DB_URL="postgresql://myuser:mypassword@postgres-server:5432/mydatabase" 
COPY --from=package_installer /usr/local/bin /usr/local/bin
COPY --from=package_installer /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY . .
CMD ["python", "./src/database/data_generator.py"]