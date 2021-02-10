FROM python:3
# Set application working directory
WORKDIR /usr/src/app
# Install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Install application
COPY ./ ./
# Run application
CMD python manage.py runserver 0.0.0.0:8000

