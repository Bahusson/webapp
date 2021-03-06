from django.urls import path
from . import views

urlpatterns = [
    path('', views.download, name='download'),
    path('progpage/<int:place>/', views.progpage, name='progpage'),
    path('pybrun/', views.pybrun, name='pybrun'),
    path('roll/', views.roll, name='roll'),
    path('launchme/<int:place>/', views.launchme, name='launchme')
]
