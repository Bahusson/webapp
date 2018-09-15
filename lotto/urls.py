from django.urls import path

from . import views

urlpatterns = [
    path('', views.download, name='download'),
    path('<int:lotto_id>/', views.progpage, name='progpage'),
]
