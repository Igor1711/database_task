from django.conf.urls import url

from . import views

urlpatterns= [
	url(r'^$forum', views.forum, name="forum"),
	url(r'^$post', views.user, name="user"),
	url(r'^$post', views.post, name="post"),
	url(r'^$thread', views.thread, name="thread"),
]
