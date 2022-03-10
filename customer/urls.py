from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('about/', views.About.as_view(), name='about'),
    path('order/', views.Order.as_view(), name='order'),
    path('confirmation/<int:pk>/', views.OrderConfirmation.as_view(), name='confirmation'),
    path('payment/', views.OrderPayConfirmation.as_view(), name='payment-confirmation')
]
