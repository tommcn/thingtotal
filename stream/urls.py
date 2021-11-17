from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import StreamView
from django.urls import include, path

urlpatterns = [
    path("stream", StreamView.as_view(), name="stream"),
]
