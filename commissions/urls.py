from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.new_commission, name='new_commission')
]