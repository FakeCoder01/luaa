# Luaa

# Flight Tikcet Booking & Management System

| <a href="#run-the-project">Installation & Run</a> | <a href="#demo-and-screenshots">Demo & Screenshots </a> |
| :-------- | :-------------------------------- |

##### Live Demo (User app) : <a href="https://luaafms.pythonanywhere.com/">https://luaafms.pythonanywhere.com</a>
##### Live Demo (Admin app) : <a href="https://luaafms.pythonanywhere.com/manage">https://luaafms.pythonanywhere.com/manage</a>

##### About

This is a web-app made with django consisting of two separate apps. One is for users and the other one is for admin. The admin application can be accessed at <a href="https://luaafms.pythonanywhere.com/manage">/manage</a>.


> The users can perform the following operations

    - Registration and Login/Logout
    - Profile creation & update
    - Search flights between two airports
    - Filter the search by date, time
    - Select between different seat types (economy, business, first)
    - Option to find both direct and connecting flights
    - Sort the results by price, travel time
    - Book a flight ticket by providing passenger info (autofills from profile)
    - Handles seat availability for each seat category
    - Pay using any card/UPI or other methods
    - See all the bookings and issued tickets
    - Tickets are issued automaticaly which can be downloaded
    - See all the payment History
    - Chat with customer support in real-time (Websocket)
    - Update Login credentials


> The admin can perform the following operations

    - Login/Logout (more admin accounts can be created from django admin panel)
    - Add/Remove/Modify Airports and its details
    - Add/Remove/Modity Flights
    - Manage seating configuration for each flight with different seat category
    - Manage price for each flight for each seat category
    - See/Modify all the users and passengers in the system and see their bookings
    - See all the payment details, status of payment
    - See all the bookings made and tickets issued
    - Search flight for a particular date/time or after/before for any flight number
    - Global full-text search for all the users, bookings, tickets, payments, flights, airports
    - See all the bookings for a flight
    - See Analytics and Stats for each flight such as revenue, seat booking percentage etc.
    - Admin dashboard with analytics such as current sale, flights, bookings and users
    - Real time chat with all customers (Websocket)
    - Send newsletter emails


> Technical deatils

    - Frameowk : Django, Django Rest Framework, Django channels for web socket
    - ASGI server : Daphne
    - Worker : Celery
    - Broker : Redis
    - Database : PostgreSQL (for test : sqlite)
    - Front-end : HTML, JavaScript, CSS, TailwindCSS


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

### User Demo
![A video showing the demo of the user application. Compression made teh video quality a little bad :))](ref/user.webm)

### Admin App Demo



Telegram : <a href="https://t.me/hitkolkata" title="Telegram ID">@hitkolkata</a>
