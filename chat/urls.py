from django.urls import path
from . import views

urlpatterns = [
    path('', views.support_user, name="user_support"),
    path('m/', views.all_latest_chat_only, name="all_latest_chat_only"),
    path('m/group/', views.manage_chat_group, name="manage_chat_group"),
    path('m/<str:profile_id>/', views.support_chat, name="support_chat"),
    path('both/older-message/', views.older_message, name="older_message"),
]
