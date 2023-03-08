from django.urls import path

from . import views

app_name = "feed"

urlpatterns = [
    path("", views.HomePage.as_view(), name='index'),
    path("selected-posts/", views.FriendsPostView.as_view(), name='friends_posts'),
    path("my-posts/", views.MyPostView.as_view(), name='my_posts'),
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("new/", views.CreateNewPost.as_view(), name="new_post"),
]
