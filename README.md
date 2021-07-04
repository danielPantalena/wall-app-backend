# Wall App - Backend

## Setup

First, clone the repo and change to the created directory:

```bash
git clone git@github.com:danielPantalena/wall-app-backend.git
cd wall-app-backend
```
Create a virtual environment to install dependencies in and activate it:
```bash
$ python3 -m venv env
$ source env/bin/activate
```
Then install the dependencies:
```bash
(env)$ pip install -r requirements.txt
```
Once `pip` has finished downloading the dependencies, it will necessary to create a `.env` file with these keys:
```env
SECRET_KEY=
SENDGRID_API_KEY=
EMAIL_SENDER=
```
Now we have to execute migrate and then the app will be ready to run:
```sh
(env)$ cd wall
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```

Navigate to `http://127.0.0.1:8000/admin`, `http://127.0.0.1:8000/users` or `http://127.0.0.1:8000/posts`.

## Tests

To run the tests, `cd` into the directory where `manage.py` is:
```sh
(env)$ python manage.py test
```
