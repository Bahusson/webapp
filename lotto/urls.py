from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.download, name='download'),
    path('<int:lotto_id>/', views.progpage, name='progpage'),
    path('lotto/pybrun/', views.pybrun, name='pybrun'),
#    path('lotto/roll/', views.roll, name='roll'),
    path('lotto/pybrun/<int:lotto_id>/', views.progpage, name='progpage'),
]
