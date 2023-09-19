from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('list', views.listLogsView, name='list'),
    path('print/<str:name>', views.filterInputView, name='print'),
    path('streamresp/<str:name>', views.stream_log_file, name="streamresp"),
    path('dynamic/<str:name>', views.dynamic_loading_page, name='dynamic'),
    path('delete/<str:name>', views.deleteLog, name='delete'),
    ]