# Leads Manager Server

Django REST API server for Email Leads Manager application. This is a Python/Django port of the Node.js email-leads-manager-server.

## Features

- User authentication with JWT tokens
- Lead management with CSV upload support
- Account management
- Email management
- Message and Subject template management
- RESTful API endpoints
- CORS support

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file (optional):
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
JWT_SECRET=your-jwt-secret-key-here
FRONTEND_URL=http://localhost:3000
MONGODB_URI=mongodb://localhost:27017/
MONGODB_NAME=email-leads-manager
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

The server will run on `http://localhost:8000` by default.

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user

### Leads
- `GET /api/leads/` - Get all leads (with pagination, search, status, assignedTo filters)
- `POST /api/leads/` - Create a new lead
- `POST /api/leads/upload/` - Upload leads from CSV file
- `GET /api/leads/{id}/` - Get a specific lead
- `PUT /api/leads/{id}/` - Update a lead
- `DELETE /api/leads/{id}/` - Delete a lead

### Accounts
- `GET /api/accounts/` - Get all accounts (with pagination)
- `POST /api/accounts/` - Create a new account
- `GET /api/accounts/{id}/` - Get a specific account
- `PUT /api/accounts/{id}/` - Update an account
- `DELETE /api/accounts/{id}/` - Delete an account

### Emails
- `GET /api/emails/` - Get all emails (with pagination and search)
- `POST /api/emails/` - Create a new email

### Message Templates
- `GET /api/message-templates/` - Get all message templates (with pagination, search, industry filters)

### Subject Templates
- `GET /api/subject-templates/` - Get all subject templates (with pagination and search)

### Health Check
- `GET /health` - Server health check

## Database

By default, the project uses SQLite. To use MongoDB, you'll need to:
1. Install `djongo` or `mongoengine`
2. Update the `DATABASES` configuration in `settings.py`

## Project Structure

```
leads-manager-server/
├── leads_manager/          # Django project settings
│   ├── settings.py         # Project settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── api/                    # Main application
│   ├── models.py          # Database models
│   ├── views.py           # API views/controllers
│   ├── serializers.py     # DRF serializers
│   ├── urls.py            # API URL routes
│   ├── authentication.py  # JWT authentication
│   └── admin.py           # Django admin configuration
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Development

The project uses Django REST Framework for API endpoints. Authentication is handled via JWT tokens stored in cookies or Authorization headers.

## Notes

- The authentication middleware is configured but can be enabled/disabled per route
- CSV upload supports flexible column naming (email, Email, firstname, first_name, etc.)
- All timestamps are automatically managed by Django
- The API follows RESTful conventions with pagination support

