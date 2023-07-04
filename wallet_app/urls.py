from django.urls import path

from . import views

app_name = 'wallet_app'

urlpatterns = [
    path('api/manage-user', views.UsersManager.as_view(), name='manage_user'),
    path('api/manage-transactions', views.TransactionsManager.as_view(), name='manage_transations'),
    path('api/ratings', views.get_ratings, name='ratings'),
]