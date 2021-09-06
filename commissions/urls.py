from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.new_commission, name='new_commission'),
    path(
        'edit/<int:commission_id>/', views.edit_commission,
        name='edit_commission'),
    path(
        'delete/<int:commission_id>/', views.delete_commission,
        name='delete_commission'),
]
