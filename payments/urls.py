from django.urls import path
from . import views

urlpatterns = [
    path('<int:commission_id>/', views.payment, name='payment')
]
