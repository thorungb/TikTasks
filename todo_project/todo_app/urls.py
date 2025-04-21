from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('todo/<int:todo_id>/edit/', views.edit_todo, name='edit_todo'),
    path('todo/<int:todo_id>/update-status/', views.update_todo_status, name='update_todo_status'),
    path('todo/<int:todo_id>/delete/', views.delete_todo, name='delete_todo'),
]