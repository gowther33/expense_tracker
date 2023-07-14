from django.urls import path
from . import views,api
from django.views.generic import TemplateView

urlpatterns = [
    path('view/',views.due_page,name="due"),

    path('due_user/',views.due_page_user,name="due_user"),

    path('due-sort/',views.due_page_sort,name="due_page_sort"),
    path('add-due/',views.add_due,name="add_due"),

    path('add-due-user/',views.add_due,name="add_due_user"),
    
    # path('add-source/',views.add_income_source,name="add_due_source"),
    # path('edit-source/<int:id>/',views.edit_due_source,name="edit_due_source"),    
    # path('delete-income-source/<int:id>/',views.delete_income_source,name="delete_due_source"),

    path('edit-due/<int:id>/',views.edit_due,name="edit_due"),
    path('delete-due/<int:id>/',views.delete_due,name="delete_due"),
    path('due-received/<int:id>/',views.due_received,name="due_received"),
    
    path('download-excel/<str:filter_by>',views.download_as_excel,name = 'due_download_as_excel'),
    path('download-csv/<str:filter_by>',views.download_as_csv,name = 'due_download_as_csv'),
    path('search',api.search_due,name="due_search"),
    
    # To be changed
    path('income-summary-data',api.due_summary,name="income_summary_data"),
    path('income-summary/',TemplateView.as_view(template_name="income_app/income_summary.html"),name="income_summary"),
    path('import/',views.import_income,name="import_income"),
    path('income-import-from-csv',views.upload_csv,name="income_import_from_csv"),
    path('income-import-from-excel',views.upload_excel,name="income_import_from_excel")
]
