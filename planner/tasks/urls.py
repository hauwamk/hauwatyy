from django.urls import path
from . import views



urlpatterns = [
    path('home/', views.home, name='home'), 
    path('add/',views.add_task, name='add_task'),


    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),

    path('toggle/<int:task_id>/', views.toggle_complete, name='toggle_complete'),

    path('signup/', views.signup_view, name='signup'),

    path('login/', views.login_view, name='login'),

    path('', views.index, name='index'),
    
    path('chat/', views.chat_page, name='chat_page'),
    path('ai-chat/', views.ai_chat, name='ai_chat'), 
]