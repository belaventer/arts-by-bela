from django.urls import path
from . import views

urlpatterns = [
    path('', views.showcase, name='showcase')
]
