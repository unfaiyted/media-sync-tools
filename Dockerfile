FROM python:3.10

WORKDIR /

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./src ./src

# todo: could disable the reload flag for production
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80","--reload"]









