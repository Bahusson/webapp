from django.urls import path
from . import views

urlpatterns = [
    path('', views.download, name='download'),
    path('progpage/<int:myprogram_id>/', views.progpage, name='progpage'),
    path('pybrun/', views.pybrun, name='pybrun'),
    path('launchme/<int:myprogram_id>/', views.launchme, name='launchme')
    # path('myprograms/roll/', views.roll, name='roll'),
]
