# Preamble

The application is developed with **python3.11.2** on a Debian Linux 12 (bookworm) system

I have not included a script to install this version of python3 and its dependencies on your computer as it may make adverse changes to your system you do not want.

I assume you already have installed a more recent version of python3 on your own system

Library and dependency installation is with **pip**, not anaconda

---

administration accounts:

username: admin
password: admin

username: ra
password: admin

# dummy user accounts for testing and presentations

username: drSimpson

password: goldsmiths123

drsimpson@example.com

username: drGriffin

password: goldsmiths456

drgriffin@example.com

username: nurseChappel

chappel@example.com

password: goldsmiths789

username: nurseGollum

gollum@example.com

password: goldsmiths321

---

# the postgres database

name: skin

userID: derm

password: derm

------------------

# Loading the app

create a virtual environment then run:

**pip install -r requirements.txt**

to install the necessary libraries and dependencies

---

# Running the app


**python3 manage.py runserver**

this convenient script:

**start.sh**

is a short bash script which sequentially runs these three commands:

1. python3 manage.py makemigratons
2. python3 manage.py migrate
3. python3 manage.py runserver

runs as: _./start.sh_

As you know, the bash script must be enabled by you first before running it:

**chmod +x ./share.sh**

is a command which will do this on a POSIX system (Linux, MacOS)

---

# Using the app

## superuser

username: **advw**

password: **advw** (same as user name)

## the registrants (dummy data/users)

| userID | username                 | email   | password      |

| 6      | nurseGollum------------- | ------- | goldsmiths321 |
| 4      | drGriffin--------------- | ------- | goldsmiths123 |
| 3      | drSimpson--------------- | ------- | goldsmiths456 |
| 5      | nurseChappel------------ | ------- | goldsmiths789 |

This represents the current state of the userIDs as they match up to the different user profiles. Changes to the database, running a copy of the app, and possibly other abstruse procedures may change the userIDs of the users from the ones listed above, usually by a shift of one.

---

# Logging in

To login two different users for a chat session, best to do so from two different browsers (i.e; Chrome and Firefox) or two different windows for the same browser, not two tabs on the same browser window.

---

# Using the chat app

Two-way communication tends to fail if trying to login two different accounts with two tabs on the same browser window.

---

# Accessing the APIs

APIs are developed for user profiles, friend requests, posts, comments and endorsements.

Here is the consolidated list of API URL path extensions:

- api/profile/<int:pk>
- api/profiles/
- api/colleaguerequest/<int:pk>
- api/colleaguerequests/
- api/post/<int:pk>
- api/posts/
- api/comment/<int:pk>
- api/comments/
- api/endorse/<int:pk>
- api/endorses/

where the primary key **pk** is a numeral

for swagger-UI:
- api/schema/swagger-ui/

---

# Testing the app PLEASE READ


## 1) testing skin_support app and users

**pytest** (as you know pytest will run python unittests as well as its own unit tests)

## 2) testing the chat app

**python3 manage.py test chat.tests**

---

## render.com

Hostname:

Port: 5432

Database: skin

Username: skin_user

### password:

### internal database URL:
postgres://skin_user:6TneHW2w5HZSh0MoFs8E9Oyye8eK10F7@dpg-cn237ogcmk4c73ddic8g-a/skin

### External Database URL:
postgres://skin_user:6TneHW2w5HZSh0MoFs8E9Oyye8eK10F7@dpg-cn237ogcmk4c73ddic8g-a.oregon-postgres.render.com/skin

### PSQL command:




