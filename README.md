# Cyber Security Base 2024 - Course Project I

## Description

This is the CSB Course Project I with flaws from the OWASP 2021 top 10 list. It is a simple blog application where users can write their own blog posts.
In order to use the application, users must log in first. Logged users can access the front page of the
application where writing and viewing blog posts is possible. Users can observe their own information at the profile page.
Deleting an account is also possible.

## Instuctions

Start by cloning the project to your machine.
```
git clone https://github.com/valttteri/CyberSecurityBase.git
```

Make sure you have installed Django
```
pip install Django
```

The project already has a database. If something goes wrong, delete the current database and initialize a new one.
```
~\src> python manage.py makemigrations
~\src> python manage.py migrate
```

Start the application
```
~\src> python manage.py runserver
```

Now you must log in at http://127.0.0.1:8000/. There are three users stored in the database - one admin and two regular users. Credentials:

admin - password \
johnny1 - 1234 \
mr.tommy - 1234

You can also create other accounts. Note that if you want to login to the Django admin page located at <baseurl>/admin, you must use the admin email account admin@gmail.com.
