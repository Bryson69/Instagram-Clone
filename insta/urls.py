from django.urls import path, include
from .views import (
    PostListView,
    PostCreateView,
)

app_name = 'insta'

urlpatterns = [
    # Local : http://127.0.0.1:8000/admin
    path('', PostListView.as_view(), name='post_list'),
    path('new/', PostCreateView.as_view(), name = 'post_create'),
]