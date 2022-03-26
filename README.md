# Campus-Portal

```
                 ____   ____ ____   
                / ___| / ___/ ___|  
                \___ \| |   \___ \  
                 ___) | |___ ___) | 
                |____/ \____|____/  
```

### To Run the project

+ Download the project
+ Make Sure you have python3 installed
+ download Django using ``` pip install Django``` in CMD
+ move to the Directory
+ Run the following Commands to Run the Django migrations to set up your models and assets

```shell
python manage.py makemigrations
```
```shell
python manage.py migrate
```
```shell
python manage.py sqlmigrate campus_portal 0001
```
#### Then Create a user using the bellow Command
```shell
python manage.py createsuperuser
```
then Enter your username, Email AND password

### Last Step
#### Start the Django web server

```shell
python manage.py runserver
```

+ In your browser, go to http://localhost:8000.

# if You want to visit a live Version, GO to this [Link](https://noureldin.pythonanywhere.com/campus_portal/) 

# our Model

![model_1](./images/models-1.png)

![model_2](./images/models-2.png)
