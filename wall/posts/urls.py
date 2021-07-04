from django.urls import path

from .views import (
    PostsList,
    PostDetails
)

urlpatterns = [
    path('', PostsList.as_view(), name='posts-list'),
    path('<int:pk>', PostDetails.as_view())
]
