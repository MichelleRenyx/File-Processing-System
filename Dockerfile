#Stage 1: Building frontend
FROM node:18 as build-stage

WORKDIR /code

COPY ./frontend/ /code/frontend/

WORKDIR /code/frontend

#Installing Packages
RUN npm install

#Building the frontend
RUN npm run build

#Stage 2: Building backend
FROM python:12.4

#Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

#Copy Django project to the container
COPY ./backend/fileprocessor/ /code/backend/fileprocessor/

RUN pip install -r ./backend/fileprocessor/requirements.txt

#Copy the frontend build to the container
COPY --from=build-stage /code/frontend/build /code/backend/fileprocessor/static/
COPY --from=build-stage /code/frontend/build/static /code/backend/fileprocessor/static/
COPY --from=build-stage /code/frontend/build/index.html /code/backend/fileprocessor/backend/templates/index.html

#Run Django Migration Commands
RUN python3 ./backend/fileprocessor/manage.py migrate

#Run Django Collectstatic Command
RUN python3 ./backend/fileprocessor/manage.py collectstatic --noinput

#Export the port
EXPOSE 80

WORKDIR /code/backend/fileprocessor

#Run the Django server
CMD ["gunicorn", "backend/wsgi.application", "--bind", "0.0.0.0:8000"]