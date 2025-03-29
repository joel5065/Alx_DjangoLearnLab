from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
    path('mark-as-read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
]