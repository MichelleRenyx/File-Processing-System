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
FROM python:3.12

#Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

#Copy Django project to the container
COPY ./backend/fileprocessor/ /code/backend/fileprocessor/

RUN pip install -r ./backend/fileprocessor/requirements.txt

#Copy the frontend build to the container
COPY --from=build-stage /code/frontend/dist /code/backend/fileprocessor/static/
COPY --from=build-stage /code/frontend/dist/assets /code/backend/fileprocessor/static/
COPY --from=build-stage /code/frontend/dist/index.html /code/backend/fileprocessor/backend/templates/index.html

# Use ARG to pass the environment variable for OpenAI API key
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}


#Run Django Migration Commands
RUN python3 ./backend/fileprocessor/manage.py migrate

#Run Django Collectstatic Command
RUN python3 ./backend/fileprocessor/manage.py collectstatic --noinput

#Export the port
EXPOSE 80

WORKDIR /code/backend/fileprocessor

#Run the Django server
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]