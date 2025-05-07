# EndySoft

EndySoft is a Django-based multi-tenant application designed to manage customers, departments, organizations, and tenants. It provides a RESTful API for CRUD operations and enforces tenant-specific access using Django REST Framework (DRF).

## Features

- **Multi-Tenancy**: Tenant-specific access enforced via headers.
- **Authentication**: Token-based authentication using Django REST Framework.
- **Modular Design**: Separate apps for customers, departments, organizations, and tenants.
- **REST API**: Endpoints for managing customers, departments, organizations, and tenants.
- **Comprehensive Testing**: Unit tests for all major functionalities.

## Project Structure

```
EndySoft/
├── core/
│   ├── customer/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── tests/
│   │       └── test_customer.py
│   ├── department/
│   ├── organization/
│   ├── tenant/
│   └── settings.py
├── env/
│   └── Virtual environment files
└── requirements.txt
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd EndySoft
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Customers
- **List Customers**: `GET /api/customer/`
- **Create Customer**: `POST /api/customer/`
- **Retrieve Customer**: `GET /api/customer/<id>/`

### Departments
- **List Departments**: `GET /api/department/`
- **Create Department**: `POST /api/department/`
- **Retrieve departments Details**: `GET /api/department/<id>/`

### Organizations
- **List Organizations**: `GET /api/organization/`
- **Create Organization**: `POST /api/organization/`
- **Retrieve Organization Details**: `GET /api/organization/<id>/`

### Tenants
- **List Tenants**: `GET /api/tenant/`
- **Create Tenant**: `POST /api/tenant/`
- **Retrieve Tenant Details**: `GET /api/tenant/<id>/`


## Running Tests

To run the unit tests, use the following command:
```bash
python manage.py test
```

## Requirements

The project dependencies are listed in the `requirements.txt` file:
```plaintext
Django
psycopg2-binary==2.9.10
asgiref==3.8.1
djangorestframework==3.16.0
sqlparse==0.5.3
typing_extensions==4.13.2
tzdata==2025.2
```