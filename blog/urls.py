from django.urls import path
from . import views



urlpatterns = [
    path('', views.index.as_view(), name='starting-page'),
    path('posts', views.all_posts.as_view(), name='posts-page'),
    path('save', views.SavedPosts.as_view(), name='saved'),
    path('posts/<slug:slug>', views.view_a_post.as_view(), name='post-a-page'),
    path('clear', views.ClearSavedPosts.as_view(), name='clear')
]