from django.urls import path
from . import views
from django.views.generic import TemplateView
from . import api

urlpatterns = [
    path('view/',views.tasks_page,name="tasks_page"),
    path('closed-task/', views.closed_task_page, name="closed_task_page"), 

    path('view_user/',views.tasks_page,name="tasks_page_user"),

    path('create-task/', views.create_task, name='create_task'),

    path('view-task/<int:id>/', views.view_task, name= "view_task"),

    path('close-task/<int:id>/', views.view_close, name= "view_close"),

    path('delete-task/<int:id>/', views.delete_task, name= "delete_task"),

    path('search',api.search_task,name="task_search"),

    path('search-closed',api.search_task_closed,name="task_search_closed"),
    
]
