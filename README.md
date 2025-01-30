# Hope Horizon

## Introduction
Hope Horizon is a Django and Angular based web application.

# Backend

## Prerequisites
- Python 3.x
- pip (Python package installer)
- Virtualenv (optional but recommended)

## Installation

### 1. Clone the repository
```sh
git clone https://github.com/himmler-cdev/hopeHorizon.git
cd hope_horizon
```

### 2. Create and activate a virtual environment (optional but recommended)
```sh
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install the dependencies
```sh
pip install -r requirements.txt
```

### 4. Apply migrations
```sh
python manage.py makemigrations
python manage.py migrate
```
#### 4.1 Clear existing database
If neccessary, you can clear the existing database with this:
```sh
rm db.sqlite3
```

### 5. Run the development server
```sh
python manage.py runserver
```

## Usage
Open your web browser and go to `http://localhost:8000/` to access the application.

## Running Tests
To run the tests, use the following command:
```sh
python manage.py test backend
```

### Running Tests with Code Coverage
To run the tests with code coverage, use the following command:
```sh
coverage run manage.py test backend
```

### Genrating Code Coverage report
To generate the code coverage report, use the following command:
```sh
coverage report -m
```

# Frontend

## Switch to correct directory
```sh
cd hopeHorizon/hope_horizon_frontend
```

## Install dependencies
```sh
npm install
```

## Start server
```sh
ng serve or npm start
```

## Usage
Open your web browser and go to `http://localhost:4200/` to access the application.
