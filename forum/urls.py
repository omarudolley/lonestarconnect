from django.urls import path
from forum import views


urlpatterns = [
    path('',views.home, name ='forum-home'),
    path('section/<pk>', views.topic, name = 'forum-topic'),
    path('section/<pk>/new/', views.new_topic, name = 'forum-new-topic'),
    path('section/<pk>/thread/<thread_pk>', views.topics_post, name = 'thread_post'),
    path('section/<pk>/thread/<thread_pk>/reply', views.reply_post, name = 'reply_post'),
    path('section/<pk>/thread/<thread_pk>/post/<post_pk>/edit', views.edit_post, name = 'edit_post'),
    path('section/<pk>/thread/<thread_pk>/post/<post_pk>/delete', views.delete_post, name = 'delete_post'),
    path('about', views.about, name = 'forum-about')
]
