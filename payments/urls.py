from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('<int:commission_id>/', views.payment, name='payment'),
    path(
        'success/<int:commission_id>/',
        views.payment_success, name='payment_success'),
    path('cache_commission/', views.cache_commission, name='cache_commission'),
    path('wh/', webhook, name='webhook')
]
