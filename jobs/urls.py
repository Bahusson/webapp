from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('<int:jobs_id>/', views.books, name='books'),
]
