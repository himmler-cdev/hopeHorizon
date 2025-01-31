# Hope Horizon

## Introduction
Hope Horizon is a Django and Angular based web application.

## Clone the repository
```sh
git clone https://github.com/himmler-cdev/hopeHorizon.git
```

# Backend

## Prerequisites
- Python 3.x
- pip (Python package installer)
- Virtualenv (optional but recommended)

## Installation

### 1. Create and activate a virtual environment (optional but recommended)
```sh
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install the dependencies
```sh
pip install -r requirements.txt
```

### 3. Apply migrations
```sh
python manage.py makemigrations
python manage.py migrate
```
#### 3.1 Clear existing database
If neccessary, you can clear the existing database with this:
```sh
rm db.sqlite3
```

### 4. Run the development server
```sh
python manage.py runserver
```

## Usage
Open your web browser and go to `http://localhost:8000/` to access the application.

## Test Data
To add test data to the system as well as the quotes perform the following commands

### Add Test Data
The following command creates a defined set of users and for theses users the following is created:
* UserTracker (all enabled)
* UserStatuses filled with random data (random amount)
* BlogPosts filled with random data (random amount)
* Comments filled with random data (random amount), only for public BlogPosts

To fill these objects instances with text we used the ***random-word-api*** with does not require an API-Key.

Created Users:
| Username     | Password       |
|--------------|----------------|
| admin        | topsecret      |
| therapist    | password123    |
| moderator    | password123    |
| user1        | password123    |
| user2        | password123    |
| user3        | password123    |
| user4        | password123    |
| user5        | password123    |

```sh
python managa.py import_test_data
```

### Add Quotes
```sh
python managa.py import_quotes .\data.csv
```

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
ng serve
```
or
```sh
npm start
```

## Usage
Open your web browser and go to `http://localhost:4200/` to access the application.