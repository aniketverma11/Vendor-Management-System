# vendorManagement

## Version Requirements
    $ python -> 3.11
    $ Django -> 4.2
    $ Database -> SQLite

## Basic Commands

### create a virtual env and activate it...

    $ python -m venv env
    $ source env/bin/activate

### First step is install all requirements

    $ pip install -r requirements/local.txt

### Do migrations

To create migrations:

    $ python manage.py makemigrations
    $ python manage.py migrate


### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Run the server

To Run the server:

    $ python manage.py runserver


## Admin URL
    $ http://127.0.0.1:8000/admin/

## swagger Docc URL
    $ http://127.0.0.1:8000

### Type checks

Running type checks with mypy:

    $ mypy vendormanagement

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.
