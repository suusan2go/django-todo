from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('sign_up', views.create, name='create'),
    path('current', views.show, name='show'),
    path('confirmation', views.confirm, name='confirm'),
]