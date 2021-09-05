from django.urls import path
from . import views

urlpatterns = [
    path('<int:commission_id>/', views.payment, name='payment'),
    path(
        'success/<int:commission_id>/',
        views.payment_success, name='payment_success')
]
