# Marouf.At:
## What did I do?
1. created virtualenv which is the Back_End folder itself
2. created the django project inside src folder
3. installed django, djangorestframework , and python-dotenv packages
4. created the .env file and excluded it using .gitignore
5. initialized .gitignore by the default .gitignore for django
6. created the requirements.txt file by running: ``` pip freeze > requirements.txt ```
7. edited the README.md that u r reading right now :)
----------------------------
## How to clone the project ( getting/configuring the project for the Back_End first time )
1. first clone the repo
2. create ur own venv: inside the Back_End folder [ ```< Python 3.13 path > -m venv venv ``` ]
3. instal the requirements: ``` pip install -r requirements.txt ```
4. create database
5. copy .env.example to .env file on ur device using terminal: ``` cp .env.example .env ``` (Note: use powershell instead of cmd on windows and 'cp' will work)
6. configure data base settings in .env file (follow the .env.example file instructions)
7. generate Secret Key using [Djecrety](https://djecrety.ir/) website, and place it in .env file
8. Do migrate: ``` python manage.py migrate ```
9. finally check if the project working: ``` python manage.py runserver ```
--------------------
## What to do after pulling the Back_End changes:
1. Do migrate: ``` python manage.py migrate ```
2. make sure the project working: ``` python manage.py runserver ```
--------------------
The End :)