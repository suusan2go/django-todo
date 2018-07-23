FROM python:3.6-alpine
RUN pip install pipenv
RUN mkdir -p /app/backend
COPY ./Pipfile /app/backend
COPY ./Pipfile.lock /app/backend
WORKDIR /app/backend
RUN pipenv install
COPY . /myapp/backend
CMD ["python", "manage.py", "runserver"]
