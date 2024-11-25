# Hope Horizon

## Introduction
Hope Horizon is a Django-based web application.

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
#### 4.1 Clear existing migration
If neccessary, you can clear existing migrations with this:
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
python manage.py test
```