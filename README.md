# phase3-chain

virtual environment stuff:  
    ~/phase3-chain/

        virtualenv -p python3.6 script_env //create  
        source script_env/bin/activate //activate  


django stuff:  
        create project : django-admin startproject chainreaction .  
        create(or update??) database: python manage.py migrate    
        create application: python manage.py startapp chain  

    ~/phase3-chain/chain_reaction
        pip install django
        pip install django-matplotlib
        pip install pymunk 
        pip install matplotlib
        
        start web server: python manage.py runserver
  

update models:  
        python manage.py makemigrations chain  
        python manage.py migrate chain  

