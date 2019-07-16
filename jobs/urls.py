from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('tricks/<int:tricks_id>/', views.books, name='books'),
    path('techs/<int:techs_id>/', views.skills, name='skills'),
]
