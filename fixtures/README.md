# Database Fixtures

This folder contains backup copies of the database data for Dave's World of Music.

## Files

- `all_data.json` - Complete database backup including all models
- `categories.json` - Product categories only
- `instruments.json` - All instruments data

## How to Use

### Loading Data on Deployment

To load all the data into a fresh database:

```bash
python manage.py loaddata fixtures/all_data.json
```

Or load specific fixtures:

```bash
python manage.py loaddata fixtures/categories.json
python manage.py loaddata fixtures/instruments.json
```

### Creating a Fresh Backup

To update these fixtures with current database data:

```bash
# Backup everything
python manage.py dumpdata --indent 2 --output fixtures/all_data.json

# Backup specific models
python manage.py dumpdata store.Category --indent 2 --output fixtures/categories.json
python manage.py dumpdata store.Instrument --indent 2 --output fixtures/instruments.json
```

### Excluding Sensitive Data

To backup without sessions or user data:

```bash
python manage.py dumpdata --indent 2 --exclude auth.permission --exclude contenttypes --exclude admin.logentry --exclude sessions.session --output fixtures/all_data.json
```

## Deployment Steps

### Standard Deployment

1. Set up your production environment
2. Run migrations: `python manage.py migrate`
3. Load fixtures: `python manage.py load_initial_data`
4. Create superuser: `python manage.py createsuperuser`
5. Collect static files: `python manage.py collectstatic`

### Docker Deployment

The fixtures are automatically loaded during Docker container initialization:

```bash
# Build and run with docker-compose
docker-compose up --build

# Or run the deployment script manually
docker exec -it <container_name> python deploy_init.py
```

### Quick Deployment Script

Use the provided deployment scripts:

```bash
# Bash (Linux/Mac)
./deploy_init.sh

# Python (Cross-platform)
python deploy_init.py
```

## Management Commands

Custom management command for loading fixtures:

```bash
# Load initial data (safe - won't reload if data exists)
python manage.py load_initial_data

# Force reload even if data exists
python manage.py load_initial_data --force
```

## Notes

- Fixtures are in JSON format
- Image files are referenced but not included - make sure to copy the `media/` folder separately
- Cart data is session-based and doesn't need to be backed up
- The `load_initial_data` command automatically loads fixtures in the correct order
- Deployment scripts handle migrations, fixtures, and static files automatically
- These fixtures were created on: November 14, 2025
