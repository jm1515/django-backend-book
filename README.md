# Initialisation d'un projet Django REST Framework avec l'utilisation de la base de données PostgreSQL, JWT et Swagger

## Installation des packages

Installer le gestionnaire de paquets Python :
`sudo easy_install pip`

Il faut ensuite installer virtualenv à l'aide de pip, afin de créer un environnement de travail virtuel pour Python :
`sudo pip install virtualenv`

## Initialisation de Virtualenv

On crée notre répertoire de travail :
`mkdir <path>`

Et on se déplace dedans :
`cd <path>`

On crée ensuite un virtualenv :
`virtualenv -p python3 myvenv`

Il faut activer cet environnement virtuel :
`source myvenv/bin/activate`

## Installation de Django

On installe django dans notre environnement :
`pip install django==2.1.5`

Puis, on initialise notre projet django :
`django-admin startproject mysite`

On se rend dans le répertoire contenant le fichier manage.py :
`cd mysite`

Et on crée la structure de notre application :
`python manage.py startapp myapp`

## Ecriture de notre Vue

Nous pouvons créer notre première vue, en y associant tout d'abord un index dans le fichier myapp/views.py :
```python
from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello, world. You're at the 'myapp' index.")
```

Ensuite, pour appeler cette vue, nous devons créer un fichier urls.py dans le répertoire myapp et l'éditer avec ce code :

```python
from django.urls import path
from .views import *

urlpatterns = [
	path('', index, name='index'),
]
```

Enfin, il faut faire pointer la configuration d'URL racine vers le module que l'on vient de modifier, en insérant ce code dans le fichier mysite/urls.py :
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	path('myapp/', include('myapp.urls')),
	path('admin/', admin.site.urls),
]
```

## Lancement du serveur 

On va installer pylint, pour détecter les erreurs dans notre code :
`pip install pylint-django`

On initialise la base de données pour l'interface de gestion de Django :
`python3 manage.py migrate`

On créé un utilisateur admin, afin de s'authentifier sur cette interface :
`python manage.py createsuperuser --username=admin --email=admin@example.com`

On exécute cette commande pour lancer le serveur :
`python manage.py runserver`

Pour vérifier que notre application fonctionne, il faut saisir cet url :
`http://127.0.0.1:8000/myapp/`

On peut également accéder à l'interface de gestion de Django, où il sera nécessaire de saisir l'identifiant admin et le mot de passe :
`http://127.0.0.1:8000/admin/`

## Installation de Django Rest Framework

Installer les modules :
`sudo pip3 install djangorestframework`

Puis dans settings.py, ajouter :
```python
INSTALLED_APPS = [
   	...
   	'rest_framework',
   	...
]
```

## Lier l'application avec PostgreSQL

Installer la base sur le pc (Linux) :
`sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib`

Ou Mac :
`brew install postgresql`

Puis lancer le serveur :
`pg_ctl -D /usr/local/var/postgres start`

Et accéder au shell psql:
`psql postgres`

Entrer les commandes suivantes :
```sql
CREATE DATABASE mysite;
CREATE USER mysiteuser WITH PASSWORD 'user';
ALTER ROLE mysiteuser SET client_encoding TO 'utf8';
ALTER ROLE mysiteuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE mysiteuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mysite TO mysiteuser;
```

Installer l'adaptateur python pour PostgreSQL :
`sudo pip3 install django psycopg2`

Dans settings.py, configurer la base de données :
```python
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'mysite',
		'USER': 'mysiteuser',
		'PASSWORD': 'user',
		'HOST': 'localhost',
		'PORT': '',
	}
}
```

Migrer les données :
`python3 manage.py makemigrations`

Appliquer les modifications :
`python3 manage.py migrate`

## Ajout du model et d'un serializer

Dans myapp/models.py, configurer votre model en ajoutant le code suivant :

```python
from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    author = models.CharField(max_length=256, null=True, blank=True)
    year = models.PositiveIntegerField(default=0, null=True, blank=True)
    price= models.FloatField(default=-1.0, null=True, blank=True)
    description = models.TextField(max_length=256, null=True, blank=True)
    bestseller= models.BooleanField(default=False)
```

Puis ajouter un serializer à ce model, en créant un fichier serializers.py dans myapp/ :
```python	
from rest_framework import serializers

from .models import Book

class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = '__all__'
```

Dans views.py, définir les requêtes GET, POST, DELETE et PUT, comme ceci :

```python
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from .models import Book
from .serializers import BookSerializer

# Create your views here.

def index(request):
    return HttpResponse("Hello world. You're at the 'myapp' index.")

class BookList(APIView):
    """
    List all books, or create a new book.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """ List all books """
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        """ Create new book """
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

class BookDetail(APIView):
    """
    Retrieve, update or delete a book instance.
    """

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """ Retrieve a book instance """
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return JsonResponse(serializer.data, safe=False)
    
    def put(self, request, pk, format=None):
        """ Update a book instance """
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """ Delete a book instance """
        book = self.get_object(pk)
        book.delete()
        return JsonResponse({}, safe=False, status=status.HTTP_204_NO_CONTENT)   
```

Et ajouter les urls dans myapp/urls.py :
```python
from django.contrib import admin
from django.urls import include,path
from django.conf.urls import url
from myapp import views

urlpatterns = [
    path('books/', views.BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetail.as_view(), name='book-details'),
]
```

Appliquer ces modifications dans la base de données :
```
python manage.py makemigrations myapp
python manage.py migrate
```

## Test dans Postman

Installer postman, et tester une requête de type GET en sélectionnant ce type dans la liste déroulante, puis saisir l'url et un code 200 devrait apparaître :
`http://127.0.0.1:8000/myapp/books/`

Pour une requête de type POST, créer une méthode dans views.py, puis sélectionner ce type, dans BODY, choisir RAW, le format de la donnée, et ajouter par exemple :

	{
		"id": 3,
		"title": "Test2",
		"author": "Jm",
		"year": 1998
	}

Saisir de nouveau la même url, et un code 201 devrait apparaître

On peut également accéder à nos données avec l'accès admin. Il faut ajouter ce code dans `myapp/admin.py` :
```python
from django.contrib import admin

# Register your models here.

from .models import Book

admin.site.register(Book)
```

Il faut ensuite saisir l'url suivante, puis l'identifiant et le mot de passe créé précedemment :
`http://127.0.0.1:8000/admin/`

Sélectionner Books ou saisir l'url suivante pour effectuer les mêmes opérations que dans Postman :
`http://127.0.0.1:8000/admin/myapp/book/`

## Ajout et test de Swagger

Installer Swagger :
`sudo pip3 install django-rest-swagger==2.1.0`

Dans settings.py, ajouter :

```python
INSTALLED_APPS = [
    ...
    'rest_framework_swagger',
    ...
]
```

Et dans myapp/urls.py, ajouter swagger dans les urls :

```python
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Book API')

urlpatterns = [
    ...
    url('swagger', schema_view),
    ...
]
```

Saisir l'url suivante :
`http://127.0.0.1:8000/myapp/swagger/`

Sélectionner un type de requête, puis "Try it out" pour l'exécuter

## Ajout et test de JWT

Installer JWT :
`sudo pip3 install djangorestframework_simplejwt==3.3`

Puis dans settings.py, ajouter :
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
}
```

Dans myapp/urls.py, ajouter les urls :
```python
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
```

Dans mysite/views.py :
```python
from rest_framework.permissions import IsAuthenticated
```

Puis dans chaque classe, ajouter :
```python
permission_classes = (IsAuthenticated,)
```

Il faut générer un token pour accéder aux requêtes, et pour cela, il faut saisir l'url suivante :
`http://127.0.0.1:8000/myapp/api/token/`

Saisir le username et le password définit plus tôt, puis cliquer sur POST, et un résultat de ce type devrait apparaître :

	HTTP 200 OK
	Allow: POST, OPTIONS
	Content-Type: application/json
	Vary: Accept

	{
		"refresh": "...",
		"access": "..."
	}

Copier la clé générée dans access, puis dans swagger,
cliquer sur Authorize, et saisir :

	Bearer <la clé access>

Les accès aux requêtes seront de nouveau disponibles.

## Autres configurations (gitignore, requirements.txt)

Créer un fichier .gitignore pour ne pas envoyer les fichiers inutiles de cette application sur le repository git :
```
__pycache__/
*.py[cod]
migrations/
.vscode/
db.sqlite3
```

Saisir ces commandes pour supprimer les fichiers qui sont déjà sur le repo :
```
git rm -r .vscode/ --cache
git rm db.sqlite3 --cache
git rm -r myapp/migrations --cache
git rm -r myapp/_pycache_ --cache
git rm -r mysite/_pycache_ --cache
```

Le requirements.txt permet d'installer tous les packages nécessaires au bon fonctionnement de l'application. Lancer la commande suivante dans l'environnement virtuel pour récupérer tous les packages installés :
```
pip freeze > requirements.txt
```