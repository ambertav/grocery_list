from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    

    path('household/select', views.HouseholdSelect.as_view(), name = 'household_select'),
    path('household/create', views.HouseholdCreate.as_view(), name = 'household_create'),

    path('member/select', views.MemberSelection.as_view(), name = 'member_selection'),
]