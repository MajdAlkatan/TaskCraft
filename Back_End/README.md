# Marouf.At:
## What did I do?
1. created virtualenv which is the Back_End folder itself
2. created the django project inside src foler
3. installed django, djangorestframework , and python-dotenv packages
4. created the .env file and excluded it using .gitignore
5. initialized .gitignore by the default .gitignore for django
6. created the requirements.txt file by running: ``` pip freeze > requirements.txt ```
7. edited the README.md that u r reading right now :)
----------------------------
## How to clone the project
1. first clone the repo
2. create ur own venv: inside the Back_End folder [ ```< Python 3.13 path > -m venv . ``` ]
3. instal the requirements: ``` pip install -r requirements.txt ```
4. create database (not now!, after we add the MYSQL configuration)
5. generate Secret Key using [Djecrety](https://djecrety.ir/) website
6. make migrations: ``` python manage.py makemigrations ``` then ``` python manage.py migrate ```
7. finally check if the project working: ``` python manage.py runserver ```
--------------------
The End :)