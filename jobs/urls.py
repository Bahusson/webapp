from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('tricks/<int:tricks_id>/', views.books, name='books'),
    path('techs/<int:techs_id>/', views.skills, name='skills'),
    path('register/', views.register, name='register'),
    path('logger/', views.logger, name='logger'),
]
