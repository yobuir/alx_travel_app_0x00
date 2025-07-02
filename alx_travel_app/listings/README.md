# ALX Travel App

A Django-based travel booking application that allows users to browse, book, and review travel listings.

## Features

- **Listings Management**: Browse and manage travel accommodations
- **Booking System**: Make reservations for available dates
- **Review System**: Rate and review accommodations
- **REST API**: RESTful API endpoints using Django REST Framework

## Models

### Listing
- Title, description, and location information
- Price per night
- Availability date range

### Booking
- Links users to specific listings
- Date range and total price tracking
- User booking history

### Review
- User ratings and comments
- Timestamp tracking
- Linked to specific listings

## Technology Stack

- **Backend**: Django 5.2.1
- **API**: Django REST Framework 3.16.0
- **Database**: MySQL (MySQLdb)
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **CORS**: django-cors-headers
- **Task Queue**: Celery with RabbitMQ
- **Environment Management**: django-environ

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```
4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

Once the server is running, visit:
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## Project Structure

```
alx_travel_app/
├── manage.py
├── requirement.txt
├── alx_travel_app/
│   ├── settings.py
│   ├── urls.py
│   └── listings/
│       ├── models.py      # Data models
│       ├── serializers.py # API serializers
│       ├── views.py       # API views
│       └── admin.py       # Admin interface
└── env/                   # Virtual environment
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is part of the ALX Software Engineering program.