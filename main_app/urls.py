from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    

    path('household/create', views.HouseholdCreate.as_view(), name = 'household_create')
]