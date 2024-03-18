# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies including the ODBC driver
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgl1-mesa-glx \
        vim \
        curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code/

# Install dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Expose the port that Django runs on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
