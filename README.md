# Luaa

# Flight Management System

| <a href="#run-the-project">Installation & Run</a> | <a href="#demo-and-screenshots">Demo & Screenshots </a> |
| :-------- | :-------------------------------- |

##### Live Demo : <a href="https://luaafms.pythonanywhere.com/">https://luaafms.pythonanywhere.com</a>

## Run the project:


1. Install python dependencies

```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory and paste the following:

```python
# Payment Gateway Config
export RAZOR_KEY_ID = RAZORPAY_API_KEY
export RAZOR_KEY_SECRET = RAZORPAY_API_SECRET

# Email Config
export EMAIL_HOST = YOUR_EMAIL_HOST
export EMAIL_HOST_USER = YOUR_EMAIL_ADDRESS
export EMAIL_HOST_PASSWORD = YOUR_EMAIL_PASSWORD
export EMAIL_PORT = 587
export EMAIL_USE_TLS = True

# DB Config
export DATABASE_NAME = DB_NAME
export DATABASE_USER = DB_USER
export DATABASE_PASSWORD = DB_PASS
export DATABASE_HOST = DB_HOST

# Redis Sever URL
export REDIS_SERVER_URL = REDIS_SERVER_URL

# Django SECRET_KEY
export SECRET_KEY = GENERATE_A_DJANGO_SECRET_KEY


``` 

3. Run the migrations:
```bash
python manage.py makemigrations
```

4. Migrate the changes to the DB:
```bash
python manage.py migrate
```

5. Create a superuser for the project
```bash
python manage.py createsuperuser
```

6. Start the celery:
```bash
celery -A fms worker --pool=solo -l info 
```

7. Start the django server [use ngnix/gunicorn for production]
```bash
python manage.py runserver
```

#### Notes
**Make sure to run `python manage.py collectstatic` for static files generation**


## Demo and Screenshots

### Airline App Demo

### User App Demo



Telegram : <a href="https://t.me/hitkolkata" title="Telegram ID">@hitkolkata</a>
