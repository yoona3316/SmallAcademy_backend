from django.urls import path

from . import views

urlpatterns = [
    path('send/', views.SendMessage.as_view(), name='send_message'),
    path('box/', views.GetMessageBox.as_view(), name='message_box'),
    path('box/sent/', views.GetSentMessageBox.as_view(), name='sent_message_box'),
    path('box/received/', views.GetReceivedMessageBox.as_view(), name='received_message_box'),
    path('<int:message_id>/', views.GetMessage.as_view(), name='get_message'),
    path('delete/<int:message_id>/', views.DeleteMessage.as_view(), name='delete_message'),
    path('unread/num/<int:user_id>/', views.GetUnreadMessageNum, name='unread_num'),
]
