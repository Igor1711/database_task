from django.conf.urls import url
from api import views

urlpatterns = [
	url(r'^clear/', views.clear, name="clear"),
	url(r'^status/', views.status, name="status"),
	url(r'^forum/create/', views.forumcreate, name="forumcreate"),
	url(r'^forum/details/',views.forumdetails, name="forumdetails"),
	
]
