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

## Flaws 

My project is a simple blog application where users can write their own blog posts. Instructions for running the application can be found in the repository.

### FLAW 1: Broken Access Control
Flaw locations:
https://github.com/valttteri/CyberSecurityBase/blob/ea7cc6870bdac257615c1ec82b1c6ab9a119fdb7/src/blogs/views.py#L224 
https://github.com/valttteri/CyberSecurityBase/blob/ea7cc6870bdac257615c1ec82b1c6ab9a119fdb7/src/blogs/views.py#L248 

Broken access control is the most common web application security risk covered in the 2021 OWASP list. Web applications with broken access control can be exploited by users in order to perform actions they do not have permission to do. These include bypassing access control checks by modifying the URL, API access from unauthorized origins and viewing or editing someone else’s account, to name a few.

The access control of my application is broken because it allows malicious acts by URL manipulation. Logged users can view anyone’s profile and also delete their account by manipulating the URL if they manage to brute force the victim’s ID. If a user’s id is 24, their profile can be found at <baseurl>/ownpage/24. Deleting the account works in a similar manner via <baseurl>/deleteuser/24. This issue can be fixed by blocking all requests that come from unauthorized users. Requests from logged users have a CSRF token that can be used to confirm their identity.

### FLAW 2: Cryptographic Failures
Flaw locations:
https://github.com/valttteri/CyberSecurityBase/blob/ea7cc6870bdac257615c1ec82b1c6ab9a119fdb7/src/blogs/views.py#L84 
https://github.com/valttteri/CyberSecurityBase/blob/ea7cc6870bdac257615c1ec82b1c6ab9a119fdb7/src/blogs/views.py#L96 
https://github.com/valttteri/CyberSecurityBase/blob/ea7cc6870bdac257615c1ec82b1c6ab9a119fdb7/src/blogs/models.py#L43 

Cryptographic failures is the second most common flaw mentioned in the OWASP list. A cryptographic failure happens when a web application does not provide required protection for sensitive data such as passwords and personal information. Some methods to prevent these issues include encrypting all sensitive data at rest, randomly generated access keys and hashing passwords with strong hashing algorithms.

My application has a cryptographic failure because it stores unhashed passwords into the database. If an attacker managed to hack the database, they would be able to take over every account stored in there. You might notice that the admin password is actually hashed. I was forced to do that because the Django admin page login system does not work if the admin account has an unhashed password. 

In order to fix this flaw, password hashing must be enabled in the application and the login system has to be slightly modified. Django has a built-in password hashing function called set_password, which is going to be used here. When password hashing is enabled, the login system must be changed in a way that when a user attempts to log in, the application will compare the raw password received as input to the hashed one stored in the database. If they match, the user will be granted access to the application.

### FLAW 3: Security misconfiguration
Flaw location:
https://github.com/valttteri/CyberSecurityBase/blob/main/src/db.sqlite3 

Number five on the OWASP list is security misconfiguration. Issues falling under this category include for example unnecessary features that are enabled or installed, leaked stack traces caused by error handling and default accounts and their passwords still enabled and unchanged.

My application has a major security misconfiguration because an admin account with the credentials “admin” and “ password” is stored in the database. An attacker could brute force the credentials instantly and gain access to the Django admin page. That is extremely harmful because the content of the database can be viewed and modified from the admin page. This issue can be fixed by entering the admin page and changing the password of the admin account.

### FLAW 4: Identification and authentication failures
Flaw location:
https://github.com/valttteri/CyberSecurityBase/blob/ea7cc6870bdac257615c1ec82b1c6ab9a119fdb7/src/blogs/views.py#L155 

Identification and authentication was number two in the 2017 OWASP top ten and it moved down to the seventh stop for the top ten of 2021. Issues in this category are related to faulty protection of users’ identity, authentication and session management. A web application is suffering from identification and authentication failures if it exposes the session identifier in the URL, has no multi-factor authentication or allows weak and common passwords, to name a few.

There is no password validation in my application so users are allowed to choose all kinds of weak and common passwords for their accounts. This exposes the users to cyber attacks. This problem can be fixed by adding password validation to the code. I wrote a custom function for password validation. The function makes sure that the passwords are strong enough. They must be at least 8 characters long and contain upper and lower case letters and special characters.

### FLAW 5: Security logging and monitoring failures
Flaw locations:
https://github.com/valttteri/CyberSecurityBase/blob/ea7cc6870bdac257615c1ec82b1c6ab9a119fdb7/src/blogs/views.py#L106 
https://github.com/valttteri/CyberSecurityBase/blob/ea7cc6870bdac257615c1ec82b1c6ab9a119fdb7/src/blogs/views.py#L126 

A software with strong security measures should be able to detect malicious activity coming from users. If user activity is not being logged and monitored, the admins might not notice any incoming cyber attacks. My application does not have any security logging or monitoring at the moment. For example, user login attempts are a significant event that should be monitored in order to reveal active cyber attacks. 

Let’s fix this flaw by creating a logging system that automatically generates a log entry every time someone tries to log in to the application. The log entries include the username and password received as input, the date and information on whether or not the attempt was successful. Admins can view the log entries on their profile.

