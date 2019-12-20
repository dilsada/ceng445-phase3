# phase3-chain

virtual environment stuff:  
virtualenv -p python3.6 script_env //create  
source script_env/bin/activate //activate  



django stuff:  
create project : django-admin startproject chainreaction .  
create(or update??) database: python manage.py migrate  
start web server: python manage.py runserver  
create application: python manage.py startapp chain  
  
update models:  
python manage.py makemigrations chain  
python manage.py migrate chain  

