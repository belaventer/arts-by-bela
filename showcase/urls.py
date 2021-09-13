from django.urls import path
from . import views

urlpatterns = [
    path('', views.showcase, name='showcase'),
    path('add/', views.personal_work, name='personal_work')
]
