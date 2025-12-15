# Dockerfile for Dave's World of Music
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=daves_music_store.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . /app/

# Create directories for media and static files
RUN mkdir -p /app/media /app/staticfiles

# Run deployment initialization
RUN python deploy_init.py

# Collect static files (if not done in deploy_init.py)
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 80

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "3", "daves_music_store.wsgi:application"]
