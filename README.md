# LookingGlass
Context based image recommendation system

to start the app, pip install django, django-haystack, django-jquery, elasticsearch
1. python manage.py makemigrations lookingglass_app
2. python manage.py migrate auth{, admin}
2. open admin site : python manage.py createsuperuser
3. Add you controllers in views.py and html files in templates/lookingglass_app
4. Never commit your local files like db.sqllite3 to git.
5. pip install google-api-python-client
6. pip install flickrapi
7. brew install elasticsearch, start elasticsearch
