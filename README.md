# ceng445-phase3

A chain reaction simulator for CENG445 Software Development with Scripting Languages

virtual environment stuff:  
    ~/ceng445-phase3/

        virtualenv -p python3.6 script_env //create  
        source script_env/bin/activate //activate  


django stuff:  
        create project : django-admin startproject chainreaction .  
        create(or update??) database: python manage.py migrate    
        create application: python manage.py startapp chain  

    ~/ceng445-phase3/chain_reaction
        pip install django
        pip install django-matplotlib
        pip install pymunk 
        pip install matplotlib
        
        start web server: python manage.py runserver
  

update models:  
        python manage.py makemigrations chain  
        python manage.py migrate chain  

