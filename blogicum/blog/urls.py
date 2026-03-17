from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('create_post/', views.PostCreateView.as_view(), name='create_post'),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('edit_profile/',
         views.edit_profile, name='edit_profile'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'),
    path('', views.index, name='index')
]
