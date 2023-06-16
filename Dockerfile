FROM python:3.8-slim-buster

WORKDIR /app
# Copy the wkhtmltopdf Windows executable
# Copy the wkhtmltox installer
# Copy the wkhtmltox installer
RUN apt-get update && apt-get install -y wkhtmltopdf




COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host", "0.0.0.0"]