from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('create_post/', views.create_post, name='create_post'),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('edit_profile/',
         views.edit_profile, name='edit_profile'),
    path('posts/<int:id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:id>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:id>/comment/', views.add_comment, name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:com_id>/',
         views.edit_comment, name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:com_id>/',
         views.delete_comment, name='delete_comment'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'),
    path('', views.index, name='index')
]
