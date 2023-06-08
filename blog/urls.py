from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='home'),
  path('register/', views.register, name='register'),
  path('login/', views.signin, name='login'),
  path('logout/', views.signout, name='logout'),
  path('posts/<int:id>', views.post_details, name='post_details'),
  path('posts/comment/<int:id>', views.create_comment, name='create_comment'),
  path('posts/create', views.create_post, name='create_post'),
  path('posts/update/<int:id>', views.update_post, name='update_post'),
  path('posts/delete/<int:id>', views.delete_post, name='delete_post'),
  path('dashboard/', views.dashboard, name='dashboard'),
]
