
FROM python:3.8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install  -r /code/requirements.txt

COPY ./nzhinuFarm /code/nzhinuFarm

#CMD ["uvicorn", "nzhinuFarm.main:app", "--host", "0.0.0.0", "--port", "15400","--reload"]