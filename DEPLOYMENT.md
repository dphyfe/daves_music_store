# Deployment Guide - Dave's World of Music

## Quick Start

The easiest way to deploy is using the automated scripts:

```bash
# Python deployment script (recommended for Docker)
python deploy_init.py

# Or use the bash script (Linux/Mac)
chmod +x deploy_init.sh
./deploy_init.sh
```

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Access the application
# http://localhost:8000
```

### Using Dockerfile Only

```bash
# Build the image
docker build -t daves-music-store .

# Run the container
docker run -p 8000:8000 -v $(pwd)/media:/app/media daves-music-store
```

## Manual Deployment Steps

If you prefer to deploy manually:

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export DJANGO_SETTINGS_MODULE=daves_music_store.settings
export DEBUG=False
export SECRET_KEY='your-secret-key-here'
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Load Initial Data

```bash
# This will load categories and instruments from fixtures
python manage.py load_initial_data

# Force reload if needed
python manage.py load_initial_data --force
```

### 5. Copy Media Files

Make sure to copy the `media/` folder to your deployment server:

```bash
# The fixtures reference images in media/instruments/
# These files must be present for images to display
rsync -av media/ user@server:/path/to/app/media/
```

### 6. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 8. Run the Server

**Development:**
```bash
python manage.py runserver
```

**Production (with gunicorn):**
```bash
gunicorn --bind 0.0.0.0:8000 --workers 3 daves_music_store.wsgi:application
```

## What Gets Loaded

The `load_initial_data` command automatically loads:

- ✅ All product categories (Guitars, Basses, Drums, etc.)
- ✅ All instruments with prices and details
- ✅ Featured instruments settings
- ✅ Product images references (you must copy actual image files)

## Important Files for Deployment

- `fixtures/categories.json` - Product categories
- `fixtures/instruments.json` - All instruments
- `fixtures/all_data.json` - Complete backup
- `deploy_init.py` - Automated deployment script
- `deploy_init.sh` - Bash deployment script
- `Dockerfile` - Docker container configuration
- `docker-compose.yml` - Multi-container orchestration

## Troubleshooting

### Fixtures Won't Load

```bash
# Check if data already exists
python manage.py load_initial_data

# Force reload
python manage.py load_initial_data --force
```

### Images Not Showing

Make sure the `media/` folder is copied to your deployment:
```bash
# Check if images exist
ls media/instruments/
```

### Database Connection Issues

For Docker deployments, ensure the database service is ready:
```bash
# Wait for database
docker-compose up db
# Then start web service
docker-compose up web
```

## Production Checklist

- [ ] Set `DEBUG=False` in settings
- [ ] Set a secure `SECRET_KEY`
- [ ] Configure allowed hosts in `ALLOWED_HOSTS`
- [ ] Run migrations
- [ ] Load fixtures
- [ ] Copy media files
- [ ] Collect static files
- [ ] Set up HTTPS/SSL
- [ ] Configure domain name
- [ ] Set up backups
- [ ] Create superuser account

## Support

For deployment issues, check:
1. Django logs
2. Database connection
3. File permissions
4. Static/media file paths
5. Environment variables
