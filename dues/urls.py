from django.urls import path
from . import views,api
from django.views.generic import TemplateView

urlpatterns = [
    path('view/',views.due_page,name="due"),

    path('due_user/',views.due_page_user,name="due_user"),

    path('due-sort/',views.due_page_sort,name="due_page_sort"),
    path('add-due/',views.add_due,name="add_due"),

    path('add-due-user/',views.add_due,name="add_due_user"),

    path('edit-due/<int:id>/',views.edit_due,name="edit_due"),
    path('delete-due/<int:id>/',views.delete_due,name="delete_due"),
    path('due-received/<int:id>/',views.due_received,name="due_received"),
    
    path('download-excel/<str:filter_by>',views.download_as_excel,name = 'due_download_as_excel'),
    path('download-csv/<str:filter_by>',views.download_as_csv,name = 'due_download_as_csv'),
    
    path('search',api.search_due,name="due_search"),

]
