from django.urls import path
from .views import HomeView, ListLogsView, FilterInputView, StreamLogView, LoadingPageView, DeleteLogView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('list', ListLogsView.as_view(), name='list'),
    path('print/<str:name>', FilterInputView.as_view(), name='print'),
    path('streamresp/<str:name>', StreamLogView.as_view(), name="streamresp"),
    path('dynamic/<str:name>', LoadingPageView.as_view(), name='dynamic'),
    path('delete/<str:name>', DeleteLogView.as_view(), name='delete'),
    ]