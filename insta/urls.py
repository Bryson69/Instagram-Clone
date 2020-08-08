from django.urls import path, include
from .views import (
    PostListView
)

app_name = 'insta'

urlpatterns = [
    # Local : http://127.0.0.1:8000/admin
    path('', PostListView.as_view(), name='post_list'),
]