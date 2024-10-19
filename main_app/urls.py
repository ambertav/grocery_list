from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    

    path('household/select', views.HouseholdSelect.as_view(), name = 'household_select'),
    path('household/create', views.HouseholdCreate.as_view(), name = 'household_create'),

    path('member/select', views.MemberSelect.as_view(), name = 'member_select'),
    path('member/create', views.MemberCreate.as_view(), name = 'member_create'),

    path('stores', views.StoreList.as_view(), name = 'store_list'),
    path('stores/create', views.StoreCreate.as_view(), name = 'store_create'),

    path('stores/<int:store_id>', views.StoreItemList.as_view(), name = 'item_list'),
    path('stores/<int:store_id>/create-item', views.ItemCreate.as_view(), name = 'item_create'),
]