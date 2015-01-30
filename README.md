felicity-threads-base
=====================

This is the core base to be used on in felicity (iiit-h)

Required Dependencies
---------------------
+ Django 1.7.1 (pip install Django==1.7.1)
+ python-mysqldb (apt-get)
+ Pillow (pip install Pillow)
+ django-countries (pip install django-countries)
+ django-cas (from ssh://hg@bitbucket.org/ParthKolekar/django-cas, pypi is too old to be relevent in Django >=1.7)
+ longerusername (pip install longerusername)
+ virtualenv (pip install virtualenv) ### ONLY IF VITRUAL ENVIRONMENT NECESSARY. DON'T IF ALREADY ON A VIRTUALENV. ###
+ redis (apt-get install redis-server)
+ celery (pip install celery[redis])
+ djcelery (pip install django-celery)

Setting Up The Virtual Env
--------------------------
If not on some virtual environment already
------------------------------------------
Execute these:
+ virtualenv venv --distribute
+ source venv/bin/activate


Notes
-----

+ The checker script should have a python function named 'check' returning an integer between 0 to 100.


QuickStart
----------

+ Copy the app folder which is most similar to your usage with the contest name
+ Also copy the Templates accordingly.
+ `grep -ir old-name` and then `sed -i 's/old-name/new-name/g' *`
+ Register app in settings.py
+ Make Appropriate changes in views.py, tasks.py and templates.
+ Have fun. :)
