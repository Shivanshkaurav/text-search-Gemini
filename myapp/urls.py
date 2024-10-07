from django.urls import path
from .views import *

urlpatterns = [
    path("file-upload/", SummaryView.as_view(), name="file-upload"),
    path("summaries/", SummaryList.as_view(), name="summaries"),
]