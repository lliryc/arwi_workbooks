FROM python:3.11 as base

# install poetry
RUN pip install poetry

COPY . /app

WORKDIR /app/

RUN poetry env use python3.11

RUN poetry install

# Write python commands to download the models

CMD ["poetry", "run", "uvicorn", "arwi_workbooks.workbooks_service:arwi_app", "--host", "0.0.0.0", "--port", "9995"]
