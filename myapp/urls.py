from .views import *
from django.contrib import admin
from django.urls import include,path
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from rest_framework_simplejwt import views as jwt_views

schema_view = get_swagger_view(title='Book API')

urlpatterns = [
    path('', index, name='index'),

    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-details'),

    url('swagger/', schema_view),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]