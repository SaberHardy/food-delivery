from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('order/<int:pk>/', views.OrderDetails.as_view(), name='detail'),
]
